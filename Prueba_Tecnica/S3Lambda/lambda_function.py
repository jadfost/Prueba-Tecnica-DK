import os
import boto3
import zipfile
import importlib.util
import pandas as pd  

def download_and_import_libs():
    s3_client = boto3.client('s3')
    s3_bucket = 'modelacion'
    s3_key = 'projectdk.zip'
    local_dir = '/tmp'
    local_path = os.path.join(local_dir, 'projectdk.zip')

    # Descargar el archivo ZIP desde S3
    s3_client.download_file(s3_bucket, s3_key, local_path)

    # Extraer el contenido del archivo ZIP
    with zipfile.ZipFile(local_path, 'r') as zip_ref:
        zip_ref.extractall(local_dir)

    # Agregar el directorio de bibliotecas al PATH de Python
    lib_path = local_dir
    print(f'Contenido de {lib_path}: {os.listdir(lib_path)}')  # Agregar esta línea
    spec = importlib.util.spec_from_file_location('tulib', lib_path)
    tulib = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tulib)

    return tulib


from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import boto3
import io

def lambda_handler(event, context):
    # Configuración de S3
    bucket_name = 'modelacion'
    train_key = 'train.csv'
    test_key = 'test.csv'
    result_key = 'test_evaluado.csv'

    # Crear cliente de S3
    s3_client = boto3.client('s3')

    # Descargar datos de entrenamiento desde S3
    train_obj = s3_client.get_object(Bucket=bucket_name, Key=train_key)
    datos_train = pd.read_csv(train_obj['Body'])

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

    # Entrenar el modelo
    pipeline.fit(X_train, y_train)

    # Descargar datos de prueba desde S3
    test_obj = s3_client.get_object(Bucket=bucket_name, Key=test_key)
    datos_test = pd.read_csv(test_obj['Body'])

    # En este caso, estamos asumiendo que Dist_max_NAL en train corresponde a Dist_max_COL en test
    datos_test.rename(columns={'Dist_max_COL': 'Dist_max_NAL'}, inplace=True)

    # Realizar imputación en los datos de prueba
    datos_test_imputed = transformador.transform(datos_test)

    # Tratar las predicciones en los datos de prueba
    predicciones_test = pipeline.predict(datos_test_imputed)

    # Agregar las predicciones al dataframe de test
    datos_test['FRAUDE'] = predicciones_test

    # Guardar resultado en S3
    result_key = 'test_evaluado.csv'
    result_path = os.path.join('/tmp', result_key)
    datos_test.to_csv(result_path, index=False)

    # Subir el resultado a S3
    s3_client.upload_file(result_path, s3_bucket, result_key)

    print(f'Archivo {result_key} creado con éxito en el bucket {s3_bucket}.')
    print("El script se ha ejecutado correctamente.")
