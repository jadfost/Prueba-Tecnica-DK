import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Cargar los datos de train.csv
ruta_train = r'C:\Users\Daniela Benavides\Documents\Documentos Jared Foster\Prueba Tecnica DK\Prueba_Tecnica\Datos3\train.csv'
datos_train = pd.read_csv(ruta_train)

# Separar las features (X) y la variable objetivo (y)
X_train = datos_train.drop('FRAUDE', axis=1)
y_train = datos_train['FRAUDE']

# Definir las columnas numéricas y categóricas
columnas_numericas = X_train.select_dtypes(include=['float64']).columns
columnas_categoricas = X_train.select_dtypes(include=['object']).columns

# Construir el transformador para imputar datos faltantes y codificar variables categóricas
transformador = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='mean'), columnas_numericas),
        ('cat', OneHotEncoder(handle_unknown='ignore'), columnas_categoricas)
    ],
    remainder='passthrough'
)

# Construir el pipeline con el transformador y el modelo RandomForestClassifier
pipeline = Pipeline(steps=[
    ('preprocessor', transformador),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Entrenar el modelo
pipeline.fit(X_train, y_train)

# Cargar los datos de test.csv
ruta_test = r'C:\Users\Daniela Benavides\Documents\Documentos Jared Foster\Prueba Tecnica DK\Prueba_Tecnica\Datos3\test.csv'
datos_test = pd.read_csv(ruta_test)

# Asegúrate de manejar la diferencia en nombres de columnas
# En este caso, estamos asumiendo que Dist_max_NAL en train corresponde a Dist_max_COL en test
# Puedes ajustar esta parte según tus necesidades específicas
datos_test.rename(columns={'Dist_max_COL': 'Dist_max_NAL'}, inplace=True)

# Realizar imputación en los datos de prueba
datos_test_imputed = transformador.transform(datos_test)

# Realizar predicciones en los datos de prueba
predicciones_test = pipeline.predict(datos_test)

# Agregar las predicciones al dataframe de test
datos_test['FRAUDE'] = predicciones_test

# Guardar el dataframe con las predicciones en un archivo test_evaluado.csv
ruta_resultado = r'C:\Users\Daniela Benavides\Documents\Documentos Jared Foster\Prueba Tecnica DK\test_evaluado.csv'
datos_test.to_csv(ruta_resultado, index=False)

print(f'Archivo test_evaluado.csv creado con éxito.')
