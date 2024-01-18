import pandas as pd
import numpy as np

# Cargar el dataset Master Data
ruta_master_data = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\Prueba_Tecnica\Datos3\Datos Maestros VF.xlsx'
hoja_master_data = 'Master Data Oficial'
master_data = pd.read_excel(ruta_master_data, sheet_name=hoja_master_data)

# Filtrar el dataset Master Data
filtro_agentes = master_data['AGENTE (OFEI)'].isin(['EMGESA', 'EMGESA S.A.'])
filtro_tipo_central = master_data['Tipo de central (Hidro, Termo, Filo, Menor)'].isin(['H', 'T'])
master_data_filtrado = master_data[filtro_agentes & filtro_tipo_central]

# Cargar el archivo dDEC1204.TXT con la codificación 'latin1'
ruta_ddec = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\Prueba_Tecnica\Datos3\dDEC1204.txt'
ddec_data = pd.read_csv(ruta_ddec, header=None, names=['Central'] + list(range(24)), encoding='latin1')

# Realizar el merge especificando las columnas de fusión
merged_data = pd.merge(master_data_filtrado, ddec_data, left_on='CENTRAL (dDEC, dSEGDES, dPRU…)', right_on='Central', how='inner')

# Calcular la suma horizontal de todas las horas
merged_data['Suma_Horizontal'] = merged_data.iloc[:, -24:].sum(axis=1)

# Seleccionar solo los que cuya suma horizontal sea mayor que cero
resultado_final = merged_data[merged_data['Suma_Horizontal'] > 0]

# Mostrar el resultado final
print(resultado_final)

# Guardar el DataSet
resultado_final.to_excel('2_DataSet.xlsx', index=False)
