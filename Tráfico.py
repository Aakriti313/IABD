import pandas as pd
import random
import PySimpleGUI as sg
from datetime import timedelta


ciudades = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia", "Palma", "Bilbao", "Las Palmas de Gran Canaria",
    "Granada", "Valladolid", "Córdoba", "Alicante", "Cádiz", "Oviedo", "San Sebastián", "Donostia", "La Coruña", "Tarragona",
    "Toledo", "Salamanca", "Burgos", "Almería", "Huelva", "Gijón", "Lérida", "Jaén", "Cáceres", "Santiago de Compostela",
    "León", "Badajoz", "Albacete", "Pamplona", "Algeciras", "Benidorm", "Getafe", "Reus", "Mataró", "Alcorcón",
    "Castellón de la Plana", "Lugo", "Guadalajara", "Torrejón de Ardoz", "Marbella", "San Fernando", "Alcalá de Henares",
    "Huesca", "Santander", "Sabadell", "Cartagena", "Córdoba", "San Cristóbal de La Laguna", "La Línea de la Concepción",
    "Ronda", "Boadilla del Monte", "Arganda del Rey", "Fuenlabrada", "Alcorcón", "Torrevieja", "Cerdanyola del Vallès",
    "Pontevedra", "Martorell", "Colmenar Viejo", "Santiago de Calatrava", "Algeciras", "Dos Hermanas", "Manresa", "Pinto",
    "Almendralejo", "Segovia", "Vigo", "Elda", "Elche", "Benalmádena", "Cieza", "A Coruña", "Villadolid", "Rivas-Vaciamadrid",
    "Majadahonda", "Alcobendas", "Soria", "Móstoles", "Ferrol", "Logroño", "Alicante", "Huelva", "Valencia", "Granada",
    "Albacete", "Burgos", "Córdoba", "Murcia", "San Sebastián", "León", "Oviedo", "Cádiz", "Toledo", "Salamanca"
]

TRAFIC_TYPE = ["ALTO","MEDIO","BAJO",]
TRAFIC_HORA_PUNTA = ["0","1"]

data = []

for i in range(150):
    origen = random.choice(ciudades)
    destino = random.choice([ciudad for ciudad in ciudades if ciudad != origen])
    hora_salida = random.randint(0, 24)
    horas = random.randint(0, 2)
    minutos = random.randint(0, 59)
    velocidad_media = 120
    # Generar distancia
    distancia = round(random.uniform(1, 100), 2)
    # Calcular tiempo en horas
    tiempo_horas = distancia / velocidad_media

    # Obtener horas y minutos
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)

    # Formatear como un tiempo "HH:MM"
    tiempo_recorrido = f"{horas}:{str(minutos).zfill(2)}"
    accidente = random.choice(["0", "1"])

    data.append({
        "Id_ruta": i + 1,
        "Nombre_ruta": f"{origen.replace(' ', '')}_{destino.replace(' ', '')}",
        "Origen": origen,
        "Destino": destino,
        "Hora_salida": hora_salida,
        "Tiempo_recorrido": tiempo_recorrido,
        "Distancia": distancia,
        "Accidente": accidente
    })


df = pd.DataFrame(data)

# Calcular Hora_punta
df['Hora_punta'] = (df['Hora_salida'] >= 7) & (df['Hora_salida'] <= 9) | (df['Hora_salida'] >= 13) & (df['Hora_salida'] <= 15) | (df['Hora_salida'] >= 19) & (df['Hora_salida'] <= 22)
df['Tiempo_recorrido'] = pd.to_timedelta('00:' + df['Tiempo_recorrido'], errors='coerce')


# Aplicar las reglas para calcular Tráfico
df.loc[(df['Distancia'] * velocidad_media < df['Tiempo_recorrido'].dt.total_seconds() / 3600), 'Tráfico'] = 'ALTO'
df.loc[(df['Distancia'] * velocidad_media >= df['Tiempo_recorrido'].dt.total_seconds() / 3600), 'Tráfico'] = 'MEDIO/BAJO'
df.loc[(df['Tráfico'] == 'MEDIO/BAJO') & (df['Accidente'] == '1'), 'Tráfico'] = 'MEDIO'
df.loc[(df['Tráfico'] == 'MEDIO/BAJO') & (df['Accidente'] == '0'), 'Tráfico'] = 'BAJO'
df.loc[(df['Hora_punta'] == 1) & (df['Accidente'] == '0'), 'Tráfico'] = 'MEDIO'
df.loc[(df['Hora_punta'] == 1) & (df['Accidente'] == '1'), 'Tráfico'] = 'ALTO'
df.loc[(df['Hora_punta'] == 0) & (df['Accidente'] == '0'), 'Tráfico'] = 'BAJO'
df.loc[(df['Hora_punta'] == 0) & (df['Accidente'] == '1'), 'Tráfico'] = 'MEDIO'


# Layout de la ventana
layout = [
    [sg.Text("Tráfico entre Ciudades")],
    #[sg.Button("Mostrar Dataset"), sg.Button("Guardar Dataset")],
    [sg.Text("Entrada de datos")],
    [sg.Text("Origen"), sg.InputCombo(ciudades, key='-ORIGEN-')],
    [sg.Text("Destino"), sg.InputCombo(ciudades, key='-DESTINO-')],
    [sg.Text("Hora Salida"), sg.Spin(list(range(1,13)), key='-HOURS-', s=3), sg.Text(':'),
                                    sg.Spin(list(range(0,60)), key='-MIN-', s=3)],
    [sg.Text("Distancia (km)"), sg.Input(key='-DISTANCIA-')],
    [sg.Text("Tiempo Recorrido (horas)"), sg.Input(key='-TIEMPO_RECORRIDO-')],
    [sg.Text("Accidente (0 o 1)"), sg.Input(key='-ACCIDENTE-')],
    [sg.Text("Hora punta (0 o 1)"), sg.Input(key='-HORA_PUNTA-')],
    [sg.Text("Datos Clustering")],
    [sg.Text("Tipo tráfico"), sg.InputCombo(TRAFIC_TYPE, key='-CLUSTER_TRAFIC-')],
    [sg.Text("Hora Punta"), sg.InputCombo(TRAFIC_HORA_PUNTA, key='-CLUSTER_HORA_PUNTA-')],
    [sg.Button("Predecir Regresión"), sg.Button("Clasificación Tráfico"), sg.Button("Clustering Tráfico"), sg.Button("Clustering hora punta")],
    [sg.Text("Resultado:"), sg.Output(size=(50, 10), key='-OUTPUT-')],
    [sg.Button("Salir")]
]


def is_trafico(distancia, velocidad_media, tiempo_recorrido, hora_punta, accidente):
    # Cálculo del tráfico basado en las reglas de negocio
    if distancia * velocidad_media < tiempo_recorrido / 3600:
        trafico = 'ALTO'
    else:
        trafico = 'MEDIO/BAJO'
    
    # Ajustes según accidente
    if trafico == 'MEDIO/BAJO' and accidente == '1':
        trafico = 'MEDIO'
    elif trafico == 'MEDIO/BAJO' and accidente == '0':
        trafico = 'BAJO'
    
    # Ajustes según hora punta y accidente
    if hora_punta == '1' and accidente == '0':
        trafico = 'MEDIO'
    elif hora_punta == '1' and accidente == '1':
        trafico = 'ALTO'
    elif hora_punta == '0' and accidente == '0':
        trafico = 'BAJO'
    elif hora_punta == '0' and accidente == '1':
        trafico = 'MEDIO'
    
    # Clasificar como "TRAFICO" o "NO TRAFICO" según el valor final en la columna 'Tráfico'
    if trafico == 'BAJO':
        return "NO TRAFICO"
    else:
        return "TRAFICO"



def clasificar_trafico(distancia, velocidad_media, tiempo_recorrido, hora_punta, accidente):
    # Cálculo del tráfico basado en las reglas de negocio
    if distancia * velocidad_media < tiempo_recorrido / 3600:
        trafico = 'ALTO'
    else:
        trafico = 'MEDIO/BAJO'
    
    # Ajustes según accidente
    if trafico == 'MEDIO/BAJO' and accidente == '1':
        trafico = 'MEDIO'
    elif trafico == 'MEDIO/BAJO' and accidente == '0':
        trafico = 'BAJO'
    
    # Ajustes según hora punta y accidente
    if hora_punta == '1' and accidente == '0':
        trafico = 'MEDIO'
    elif hora_punta == '1' and accidente == '1':
        trafico = 'ALTO'
    elif hora_punta == '0' and accidente == '0':
        trafico = 'BAJO'
    elif hora_punta == '0' and accidente == '1':
        trafico = 'MEDIO'
    
    return trafico


# Crear la ventana
window = sg.Window("Tráfico entre Ciudades", layout)


# Bucle de eventos
while True:
    event, values = window.read()


    if event == sg.WIN_CLOSED or event == "Salir":
        break
    elif event == "Predecir Regresión":
        try:
            window['-OUTPUT-'].update('')  # Limpiar antes de mostrar
            # Recoger los valores de los campos de entrada de la interfaz
            distancia = float(values['-DISTANCIA-'])
            velocidad_media = 120
            hours, minutes = int(values["-HOURS-"]), int(values["-MIN-"])
            hora_salida = timedelta(hours=hours, minutes=minutes)
            tiempo_recorrido = int(values['-TIEMPO_RECORRIDO-'])
            accidente = values['-ACCIDENTE-']
            hora_punta = values['-HORA_PUNTA-']


            # Llamar a la función clasificar_trafico y recibir el tipo de tráfico
            df_resultado = is_trafico(distancia, velocidad_media, tiempo_recorrido, hora_salida, accidente)
            # Mostrar el tráfico clasificado en el campo de salida
            # tipo_trafico = df_resultado['Tráfico'].iloc[0]  # Tomamos el valor de tráfico de la primera fila
            window['-OUTPUT-'].update(f'El tipo de tráfico es: {df_resultado}')
        except ValueError:
            sg.popup("Por favor, ingrese valores válidos.")
    elif event == "Clasificación Tráfico":
        try:
            window['-OUTPUT-'].update('')  # Limpiar antes de mostrar
            # Recoger los valores de los campos de entrada de la interfaz
            distancia = float(values['-DISTANCIA-'])
            velocidad_media = 120
            hours, minutes = int(values["-HOURS-"]), int(values["-MIN-"])
            hora_salida = timedelta(hours=hours, minutes=minutes)
            tiempo_recorrido = int(values['-TIEMPO_RECORRIDO-'])
            accidente = values['-ACCIDENTE-']
            hora_punta = values['-HORA_PUNTA-']


            # Llamar a la función clasificar_trafico y recibir el tipo de tráfico
            df_resultado = clasificar_trafico(distancia, velocidad_media, tiempo_recorrido, hora_salida, accidente)
            # Mostrar el tráfico clasificado en el campo de salida
            # tipo_trafico = df_resultado['Tráfico'].iloc[0]  # Tomamos el valor de tráfico de la primera fila
            window['-OUTPUT-'].update(f'El tipo de tráfico es: {df_resultado}')
        except ValueError:
            sg.popup("Por favor, ingrese valores válidos.")
    elif event == "Clustering Tráfico":
        try:
            type_trafic = values['-CLUSTER_TRAFIC-']
            # Agrupar el DataFrame por 'Tráfico'
            df_agrupado = df.groupby('Tráfico')
            # Obtener los nombres de las rutas para cada tipo de tráfico
            nombres_rutas_por_trafico = df_agrupado['Nombre_ruta'].apply(list)
            # Obtener los nombres de las rutas con tráfico ALTO
            nombres_rutas_alto_trafico = nombres_rutas_por_trafico[type_trafic]
            # Imprimir los nombres de las rutas con tráfico ALTO
            # Agrupar el DataFrame por 'Hora_punta'
            df_agrupado = df.groupby('Hora_punta')
            # Obtener los nombres de las rutas mediante la Hora_punta
            nombres_rutas_hora_punta = df_agrupado['Nombre_ruta'].apply(list)
            window['-OUTPUT-'].update('')  # Limpiar antes de mostrar
            print(nombres_rutas_hora_punta[0])
            print(nombres_rutas_hora_punta[1])
        except ValueError:
            sg.popup("Por favor, ingrese valores válidos.")
    elif event == "Clustering hora punta":
        try:
            type_hora_punta = values['-CLUSTER_HORA_PUNTA-']
            # Agrupar el DataFrame por 'Hora_punta'
            df_agrupado = df.groupby('Hora_punta')
            # Obtener los nombres de las rutas mediante la Hora_punta
            nombres_rutas_hora_punta = df_agrupado['Nombre_ruta'].apply(list)
            window['-OUTPUT-'].update('')  # Limpiar antes de mostrar
            print(nombres_rutas_hora_punta[0])
            print(nombres_rutas_hora_punta[1])
        except ValueError:
            sg.popup("Por favor, ingrese valores válidos.")

window.close()
