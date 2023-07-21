import json
import boto3
import io
import pandas as pd

def lambda_handler(event, context):
    BUCKET_NAME="jiyun-seoul-serverless-keb"
    session = boto3.Session()
    s3 = session.client('s3')
    filename = event['filename']
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=filename
        )
    df = pd.read_csv(io.BytesIO(obj["Body"].read()), index_col=0)
    
    data = {
        "Index" : list(df['Index']),
        "Date" : list(df['Date']),
        "Type" : list(df['Type']),
        "Category" : list(df['Category']),
        "Item" : list(df['Item']),
        "Amount" : list(df['Amount']),
        "Note" : list(df['Note'])   
        }

    #TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(data),
    }
