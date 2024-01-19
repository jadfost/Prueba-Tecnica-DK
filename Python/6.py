import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Cargamos los datos de train.csv
ruta_train = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\Prueba_Tecnica\Datos3\train.csv'
datos_train = pd.read_csv(ruta_train)

# Separamos las features (X) y la variable objetivo (y)
X_train = datos_train.drop('FRAUDE', axis=1)
y_train = datos_train['FRAUDE']

# Se definen las columnas numéricas y categóricas
columnas_numericas = X_train.select_dtypes(include=['float64']).columns
columnas_categoricas = X_train.select_dtypes(include=['object']).columns

# Se monta el transformador para imputar datos faltantes y codificar variables categóricas
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

# Entrenamos el modelo
pipeline.fit(X_train, y_train)

# Se cargan los datos de test.csv
ruta_test = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\Prueba_Tecnica\Datos3\test.csv'
datos_test = pd.read_csv(ruta_test)

# En este caso, estamos asumiendo que Dist_max_NAL en train corresponde a Dist_max_COL en test
datos_test.rename(columns={'Dist_max_COL': 'Dist_max_NAL'}, inplace=True)

# Realizar imputación en los datos de prueba
datos_test_imputed = transformador.transform(datos_test)

# Se tratan las predicciones en los datos de prueba
predicciones_test = pipeline.predict(datos_test)

# Agregamos las predicciones al dataframe de test
datos_test['FRAUDE'] = predicciones_test

# Se guerda el dataframe con las predicciones en un archivo test_evaluado.csv
ruta_resultado = r'C:\Users\JadFost\OneDrive\Escritorio\Prueba-Tecnica-DK\test_evaluado.csv'
datos_test.to_csv(ruta_resultado, index=False)

print(f'Archivo test_evaluado.csv creado con éxito.')
