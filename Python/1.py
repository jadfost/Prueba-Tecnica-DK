import pandas as pd

# Ruta completa del archivo
file_path = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\Prueba_Tecnica\Datos3\OFEI1204.txt'

# Lista para almacenar datos
final_data = []

# Variables para almacenar el agente actual y sus plantas
current_agent = None
current_plantas = []

# Bandera para indicar si estamos dentro del bloque de procesamiento de datos
inside_data_block = False

# Abrir el archivo y leer línea por línea
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Buscar la línea que contiene el nombre del agente
        if line.startswith("AGENTE:"):
            if current_agent is not None:
                # Agregar todas las combinaciones de agentes y plantas al DataFrame final
                for planta in current_plantas:
                    final_data.append({
                        'Agente': current_agent,
                        'Planta': planta,
                        **{f'Hora_{i+1}': None for i in range(24)}
                    })
            current_agent = line.split(":")[1].strip()
            current_plantas = []
            inside_data_block = True
            continue

        # Procesar líneas de datos dentro del bloque de datos
        if inside_data_block and line.strip():
            # Dividir la línea en columnas
            columns = line.split(',')
            # Verificar si hay al menos dos elementos en la lista y si el segundo elemento es 'D'
            if len(columns) >= 2 and columns[1].strip() == 'D':
                # Extraer información relevante
                plant = columns[0].strip()
                hours = [float(value.replace(',', '.').strip()) for value in columns[2:]]
                # Crear un diccionario con la información
                data = {
                    'Agente': current_agent,
                    'Planta': plant,
                    **{f'Hora_{i+1}': hour for i, hour in enumerate(hours)}
                }
                # Agregar el diccionario a la lista de datos
                final_data.append(data)
                # Agregar la planta a la lista de plantas del agente
                current_plantas.append(plant)

# Crear un DataFrame de pandas
df = pd.DataFrame(final_data)

# Imprimir el DataFrame
print(df)

# Especifica la ruta completa deseada para el archivo Excel
excel_file_path = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\1_DataSet.xlsx'

# Guardar el DataFrame como un archivo Excel
df.to_excel(excel_file_path, index=False, header=['Agente', 'Planta'] + [f'Hora_{i}' for i in range(1, 25)])
