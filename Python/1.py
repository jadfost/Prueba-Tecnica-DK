import pandas as pd
import os

# Ruta completa del archivo
file_path = r'C:\Users\Daniela Benavides\Documents\Documentos Jared Foster\Prueba Tecnica DK\Prueba_Tecnica\Datos3\OFEI1204.txt'

# Diccionario para almacenar datos por agente
agent_data_dict = {}

# Bandera para indicar si estamos procesando un nuevo agente
new_agent = False

# Abrir el archivo y leer línea por línea
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Buscar la línea que contiene el nombre del agente
        if line.startswith("AGENTE:"):
            agent_name = line.split(":")[1].strip()
            new_agent = True
            agent_data_dict[agent_name] = {'Planta': [], 'Data': []}
            continue

        # Procesar líneas de datos
        if new_agent and line.strip():
            # Dividir la línea en columnas
            columns = line.split(',')
            # Filtrar registros Tipo D
            if columns[1].strip() == 'D':
                # Extraer información relevante
                plant = columns[0].strip()
                hours = [float(value.strip()) for value in columns[2:]]
                # Crear un diccionario con la información
                agent_data = {
                    'Agente': agent_name,
                    'Planta': plant,
                    **{f'Hora_{i+1}': hour for i, hour in enumerate(hours)}
                }
                # Agregar el diccionario a la lista de datos
                agent_data_dict[agent_name]['Data'].append(agent_data)
                # Agregar la planta al conjunto de plantas del agente
                agent_data_dict[agent_name]['Planta'].append(plant)
            new_agent = False

# Crear un DataFrame de pandas
final_data = []
for agent_name, agent_info in agent_data_dict.items():
    for data in agent_info['Data']:
        final_data.append(data)

df = pd.DataFrame(final_data)

# Imprimir el DataFrame
print(df)

# Especifica la ruta completa deseada para el archivo Excel
excel_file_path = r'C:\Users\Daniela Benavides\Documents\Documentos Jared Foster\Prueba Tecnica DK\1_DataSet.xlsx'

# Guardar el DataFrame como un archivo Excel
df.to_excel(excel_file_path, index=False)