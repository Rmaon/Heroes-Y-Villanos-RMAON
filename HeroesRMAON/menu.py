import sys
import json
from os import path, makedirs
from clases.heroe import Heroe
from clases.villano import Villano
from datetime import datetime
import os
from log import nombre_fichero, log

DATA_FILE = path.join(path.dirname(__file__), 'data.json')
heroes = []
villanos = []


def clear_screen():
    """Limpia la pantalla de la terminal de forma portable."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def pause_and_clear(prompt='Pulsa Enter para continuar...'):
    try:
        input(prompt)
    except EOFError:
        # cuando no hay stdin disponible
        return
    clear_screen()


def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    nacimiento = parse_fecha(fecha_nacimiento)
    return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))


def parse_fecha(fecha_str):
    """Intentar parsear fecha en formatos DD/MM/YYYY o YYYY-MM-DD.
    Devuelve un datetime.date"""
    for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(fecha_str, fmt)
        except ValueError:
            continue
    raise ValueError('Formato de fecha inválido')


def load_data():
    global heroes, villanos
    if path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        # Aceptar fechas guardadas en formatos antiguos (YYYY-MM-DD) o nuevo (DD/MM/YYYY)
        raw_heroes = data.get('heroes', [])
        raw_villanos = data.get('villanos', [])
        # normalizar fecha usando parse_fecha si es necesario
        for d in raw_heroes:
            if 'fecha_nacimiento' in d:
                try:
                    dt = parse_fecha(d['fecha_nacimiento'])
                    d['fecha_nacimiento'] = dt.strftime('%d/%m/%Y')
                except ValueError:
                    pass
        for d in raw_villanos:
            if 'fecha_nacimiento' in d:
                try:
                    dt = parse_fecha(d['fecha_nacimiento'])
                    d['fecha_nacimiento'] = dt.strftime('%d/%m/%Y')
                except ValueError:
                    pass
        heroes = [Heroe.from_dict(d) for d in raw_heroes]
        villanos = [Villano.from_dict(d) for d in raw_villanos]
    log('Datos cargados desde data.json')


def save_data():
    data = {
        # Guardar fechas en formato DD/MM/YYYY
        'heroes': [h.to_dict() for h in heroes],
        'villanos': [v.to_dict() for v in villanos]
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log('Datos guardados en data.json')

def crear_personaje(tipo):
    nombre = input('Nombre: ')
    print()
    apellidos = input('Apellidos: ')
    print()
    # Validar formato de fecha DD/MM/YYYY (acepta también YYYY-MM-DD por compatibilidad)
    while True:
        fecha_nacimiento = input('Fecha de nacimiento (DD/MM/YYYY): ')
        try:
            dt = parse_fecha(fecha_nacimiento)
            # normalizar al formato DD/MM/YYYY para almacenamiento
            fecha_nacimiento = dt.strftime('%d/%m/%Y')
            break
        except ValueError:
            print('Formato de fecha inválido. Por favor usa DD/MM/YYYY.')
            print()
            
    if tipo == 'heroe':
        h = Heroe(nombre, apellidos, fecha_nacimiento)
        heroes.append(h)
        print(f"Héroe creado: {h.nombre} {h.apellidos}")
        log(f"Creado Heroe {h.nombre} {h.apellidos} id={h.identificador}")
        print()
        
        save_data()
    else:
        v = Villano(nombre, apellidos, fecha_nacimiento)
        villanos.append(v)
        print(f"Villano creado: {v.nombre} {v.apellidos}")
        log(f"Creado Villano {v.nombre} {v.apellidos} id={v.identificador}")
        print()
        
        save_data()

def buscar_personajes():
    # Pedir tipo usando (h/v)
    while True:
        tipo_in = input('¿Buscar héroe o villano? (h/v): ').strip().lower()
        if tipo_in in ('h', 'v'):
            break
        print("Introduce 'h' para héroe o 'v' para villano.")
    lista = heroes if tipo_in == 'h' else villanos
    tipo_label = 'Héroe' if tipo_in == 'h' else 'Villano'
    consulta = input('Ejemplo "GITGod > 50" o "nombre = Fernando" (enter para listar todos): ').strip()
    resultado = []
    if consulta == '':
        # Mostrar todos los personajes del tipo seleccionado
        if lista:
            for p in lista:
                imprimir_personaje(p)
                print()

        else:
            print('No hay personajes registrados de este tipo.')
            print()

        return
    # parse simple expressions: atributo [operador] valor
    import re
    m = re.match(r"^(\w+)\s*(>=|<=|>|<|=)\s*(.+)$", consulta)
    if not m:
        print('Consulta no válida. Usa formato: atributo operador valor')
        return
    atributo_raw, operador, valor_raw = m.group(1), m.group(2), m.group(3)
    atributo = atributo_raw.lower()
    # intentar resolver atributo a un atributo real del objeto (insensible a mayúsculas y guiones bajos)
    def resolve_attr(obj, name):
        name = name.lower()
        for a in dir(obj):
            if a.lower() == name:
                return a
        # permitir coincidencias parciales (startswith)
        for a in dir(obj):
            if a.lower().startswith(name):
                return a
        return None

    # normalizar valor
    valor = valor_raw.strip()
    for p in lista:
        real_attr = resolve_attr(p, atributo)
        if not real_attr:
            continue
        val = getattr(p, real_attr)
        matched = False
        # intentar comparar como número
        try:
            val_num = float(val)
            valor_num = float(valor)
            if operador == '>':
                matched = val_num > valor_num
            elif operador == '<':
                matched = val_num < valor_num
            elif operador == '>=':
                matched = val_num >= valor_num
            elif operador == '<=':
                matched = val_num <= valor_num
            elif operador == '=':
                matched = val_num == valor_num
        except Exception:
            # comparar como texto: '=' significa contains (parcial) o igualdad exacta según prefieras
            if operador == '=':
                if valor.lower() in str(val).lower():
                    matched = True
        if matched:
            resultado.append(p)
    if resultado:
        for p in resultado:
            imprimir_personaje(p)
    else:
        print('No se encontraron coincidencias.')

def mostrar_edades():
    print('Edades de héroes:')
    for h in heroes:
        print(f"{h.nombre} {h.apellidos}: {calcular_edad(h.fecha_nacimiento)} años")
    print('Edades de villanos:')
    for v in villanos:
        print(f"{v.nombre} {v.apellidos}: {calcular_edad(v.fecha_nacimiento)} años")


def elegir_personaje(lista, tipo_label):
    if not lista:
        print(f'No hay {tipo_label}s disponibles.')
        return None
    print(f"Selecciona un {tipo_label}:")
    for i, p in enumerate(lista, start=1):
        print(f"{i}. {p.nombre} {p.apellidos} - Puntuación: {p.puntuacion_total}")
    sel = input(f"Introduce número del {tipo_label} (enter para cancelar): ").strip()
    if sel == '':
        return None
    # intentar por índice
    if sel.isdigit():
        idx = int(sel)
        if 1 <= idx <= len(lista):
            return lista[idx-1]
        else:
            print('Índice fuera de rango.')
            return None
    # intentar por id
    for p in lista:
        if p.identificador == sel:
            return p
    print('No se encontró personaje con ese ID.')
    return None


def enfrentar_personajes():
    # elegir héroe
    her = elegir_personaje(heroes, 'héroe')
    if her is None:
        print('Enfrentamiento cancelado (no se seleccionó héroe).')
        return
    # elegir villano
    vil = elegir_personaje(villanos, 'villano')
    if vil is None:
        print('Enfrentamiento cancelado (no se seleccionó villano).')
        return

    print(f"Enfrentamiento: {her.nombre} {her.apellidos} (puntuación {her.puntuacion_total}) vs {vil.nombre} {vil.apellidos} (puntuación {vil.puntuacion_total})")
    # comparar puntuaciones
    if her.puntuacion_total > vil.puntuacion_total:
        ganador = her
        tipo_ganador = 'Héroe'
    elif her.puntuacion_total < vil.puntuacion_total:
        ganador = vil
        tipo_ganador = 'Villano'
    else:
        ganador = None

    if ganador:
        print(f'Ganador: {tipo_ganador} {ganador.nombre} {ganador.apellidos})')
        log(f'Enfrentamiento: {her.identificador} vs {vil.identificador} -> Ganador: {tipo_ganador} {ganador.identificador}')
    else:
        print('Empate técnico entre ambos personajes.')
        log(f'Enfrentamiento: {her.identificador} vs {vil.identificador} -> Empate')


def imprimir_personaje(p):
    try:
        data = p.to_dict()
    except Exception:
        # fallback: usar __dict__
        data = {k: v for k, v in vars(p).items()}
    data.pop('identificador', None)
    # Imprimir encabezado con nombre
    header = f"{data.get('nombre', '')} {data.get('apellidos', '')}".strip()
    print('---')
    print(header)
    for k, v in data.items():
        if k in ('nombre', 'apellidos'):
            continue
        label = k.replace('_', ' ').capitalize()
        print(f"{label}: {v}")
    print('---')

def menu():
    while True:
        print('\n--- Menú ---')
        print('1. Crear héroe')
        print('2. Crear villano')
        print('3. Buscar personajes por atributo/cualidad')
        print('4. Mostrar edad de héroes y villanos')
        print('5. Enfrentar héroe vs villano')
        print('6. Salir')
        opcion = input('Elige una opción: ')
        if opcion == '1':
            crear_personaje('heroe')
        elif opcion == '2':
            crear_personaje('villano')
        elif opcion == '3':
            buscar_personajes()
        elif opcion == '4':
            mostrar_edades()
        elif opcion == '5':
            enfrentar_personajes()
        elif opcion == '6':
            print('Saliendo...')
            sys.exit()
        else:
            print('Opción no válida.')
        # Pausa y limpia la pantalla tras cada interacción (excepto al salir)
        pause_and_clear()

if __name__ == '__main__':
    load_data()
    try:
        menu()
    except KeyboardInterrupt:
        print('\nSaliendo...')
        save_data()