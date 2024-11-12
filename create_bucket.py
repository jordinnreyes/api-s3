import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    

    # Extraer parámetros del JSON recibido en el evento
    datos = event.get('body', {})
    nombre_bucket = datos.get('bucket')
    region = datos.get('region', 'us-east-1')  # Región por defecto: us-east-1

    # Validar que el nombre del bucket fue proporcionado
    if not nombre_bucket:
        return {
            'statusCode': 400,
            'body': 'El parámetro "bucket" es obligatorio.'
        }
    
    try:
        # Inicializar el cliente S3
        s3_client = boto3.client('s3', region_name=region)
        
        # Crear el bucket
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=nombre_bucket)
        else:
            s3_client.create_bucket(
                Bucket=nombre_bucket,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        return {
            'statusCode': 200,
            'body': f"Bucket '{nombre_bucket}' creado exitosamente en la región {region}."
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"Error al crear el bucket: {e}"
        }
