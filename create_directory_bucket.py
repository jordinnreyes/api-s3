import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
   
    # Extraer parámetros del JSON recibido en el evento
    datos = event.get('body', {})
    nombre_bucket = datos.get('bucket')
    nombre_directorio = datos.get('directorio')

    if not nombre_bucket or not nombre_directorio:
        return {
            'statusCode': 400,
            'body': 'Los parámetros "bucket" y "directorio" son obligatorios.'
        }

    # Asegurarse de que el nombre del directorio termina en "/"
    if not nombre_directorio.endswith('/'):
        nombre_directorio += '/'

    try:
        # Inicializar el cliente S3
        s3_client = boto3.client('s3')
        
        # Crear un objeto con la clave del "directorio"
        s3_client.put_object(Bucket=nombre_bucket, Key=nombre_directorio)
        
        return {
            'statusCode': 200,
            'body': f"Directorio '{nombre_directorio}' creado en el bucket '{nombre_bucket}'."
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"Error al crear el directorio: {e}"
        }
