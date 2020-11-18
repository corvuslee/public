import boto3
from botocore.exceptions import ClientError
import pandas as pd

pd.set_option('max_colwidth', None)  # Display the whole column content

s3 = boto3.client('s3')
bucket = 'nyc-tlc'
year_lst = [i for i in range(2009, 2021)]  # 2009-2020


def s3_query(file):
    """
    Query the first line of the file,
    return null if file not found
    """
    try:
        # submit the query
        response = s3.select_object_content(
            Bucket=bucket,
            Key=file,
            Expression="select * from s3object limit 1",
            ExpressionType='SQL',
            InputSerialization={"CSV": {}, "CompressionType": "NONE"},
            OutputSerialization={"CSV": {}}
        )

    except ClientError as e:
        # return null if file not found
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(f'File not found: {file}')
            return([b''])

    else:
        # get the response
        records = list()

        for event in response['Payload']:
            if 'Records' in event:
                records.append(event['Records']['Payload'])
        return records


def print_schema(type):
    """
    Return a dataframe with the CSV header (column names)
    year: e.g., 2020
    schema: e.g., col1,col2,col3
    """
    df = pd.DataFrame()

    for year in year_lst:
        file = f'trip data/{type}_tripdata_{year}-04.csv'
        print(f'Getting columns from file {file}')
        # get the first line of the CSV file
        cols = s3_query(file)
        df = df.append(
            {
                'year': year,
                # decode 1st line of the query result
                'schema': cols[0].decode('utf-8')
            },
            ignore_index=True
        )
    return df


df_yellow = print_schema('yellow')
df_green = print_schema('green')
df_fhv = print_schema('fhv')
df_fhvhv = print_schema('fhvhv')
