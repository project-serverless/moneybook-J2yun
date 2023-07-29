import json
import io
import pandas as pd
import boto3

def lambda_handler(event, context):
    BUCKET_NAME="alex6-ICN-moneybook-bucket"
    crud = event["CRUD"]
    
    if crud=="CREATE":
        addData(event["filename"],event["date"],event["type"], \
            event["category"],event["item"],event["amount"],event["note"],BUCKET_NAME)
    elif crud=="DELETE":
        deleteData(event["filename"],BUCKET_NAME,event["index"])
    elif crud=="UPDATE":
        updateData(event["filename"],event["date"],event["type"],event["category"], \
        event["item"],event["amount"],event["note"],event["index"],BUCKET_NAME)
    
    
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('add Data Successfully!')
    }
    
def readCSV(filename,BUCKET_NAME):
    session = boto3.Session()
    s3 = session.client('s3')
    
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=filename
        )
    df = pd.read_csv(io.BytesIO(obj["Body"].read()), index_col=0)
    
    return df
    
def writeCSV(df,filename,BUCKET_NAME):
    session = boto3.Session()
    s3 = session.client('s3')
    s3.put_object(
        Body=df.to_csv().encode(),
        Bucket=BUCKET_NAME,
        Key=filename
    )
    

def addData(filename,date,type,category,item,amount,note,BUCKET_NAME):
    
    df = readCSV(filename,BUCKET_NAME)
    
    now_index = df.iloc[-1]["Index"]
    new_df = pd.DataFrame({ "Index" : now_index + 1,
           "Date":[date],
           "Type":[type],
           "Category":[category],
           "Item":[item],
           "Amount":[amount],
           "Note":[note]})
    df = pd.concat([df,new_df],ignore_index=True)
    
    writeCSV(df,filename,BUCKET_NAME)
    
def deleteData(filename,BUCKET_NAME,s_index):
    df = readCSV(filename,BUCKET_NAME)
    
    df = df.drop(df[df["Index"]==s_index].index)
    
    writeCSV(df,filename,BUCKET_NAME)
    
def updateData(filename,date,type,category,item,amount,note,index,BUCKET_NAME):
    df = readCSV(filename,BUCKET_NAME)
    
    df.loc[df["Index"] == index, "Date"] = date
    df.loc[df["Index"] == index, "Type"] = type
    df.loc[df["Index"] == index, "Category"] = category
    df.loc[df["Index"] == index, "Item"] = item
    df.loc[df["Index"] == index, "Amount"] = amount
    df.loc[df["Index"] == index, "Note"] = note
    
    writeCSV(df,filename,BUCKET_NAME)