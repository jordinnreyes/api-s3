import base64
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
   
    # Extraer parámetros del JSON recibido en el evento
    datos = event.get('body', {})
    nombre_bucket = datos.get('bucket')
    directorio = datos.get('directorio', '')
    nombre_archivo = datos.get('filename')
    archivo_base64 = datos.get('file_data')

    # Validar que se proporcionaron los parámetros necesarios
    if not nombre_bucket or not nombre_archivo or not archivo_base64:
        return {
            'statusCode': 400,
            'body': 'Los parámetros "bucket", "filename" y "file_data" son obligatorios.'
        }

    # Asegurarse de que el nombre del directorio termina en "/"
    if directorio and not directorio.endswith('/'):
        directorio += '/'

    # Construir la clave S3 para el archivo (directorio + nombre de archivo)
    s3_file_name = f"{directorio}{nombre_archivo}"

    try:
        # Inicializar el recurso S3
        s3 = boto3.resource('s3')

        # Subir el archivo decodificado a S3
        s3.Object(nombre_bucket, s3_file_name).put(Body=base64.b64decode(archivo_base64))

        return {
            'statusCode': 200,
            'body': f"Archivo '{nombre_archivo}' subido exitosamente al bucket '{nombre_bucket}' en el directorio '{directorio}'."
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"Error al subir el archivo: {e}"
        }
