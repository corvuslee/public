- [Challenge 1](#challenge-1)
  - [Method](#method)
  - [Result](#result)
    - [Yellow taxi](#yellow-taxi)
    - [Green taxi](#green-taxi)
    - [For-hire vehicle](#for-hire-vehicle)
    - [High volume for-hire vehicle](#high-volume-for-hire-vehicle)

> * Raw data: https://registry.opendata.aws/nyc-tlc-trip-records-pds/
> * Bucket: s3://nyc-tlc

# Challenge 1
This dataset is well-known for schema change over years. Take a note of the schema for each type per year.

> Tips: Browse to `https://s3.console.aws.amazon.com/s3/buckets/<bucketname>` to view the folders and files

* Number of years: 2009-2020
* Type: fhv, fhvhv, green, yellow

## Method
Files are too big to preview in console. If we use CLI, replace the `key` and repeat like 40 times.
```
aws s3api select-object-content \
    --bucket nyc-tlc \
    --key "trip data/yellow_tripdata_2019-08.csv" \
    --expression "select * from s3object limit 3" \
    --expression-type 'SQL' \
    --input-serialization '{"CSV": {}, "CompressionType": "NONE"}' \
    --output-serialization '{"CSV": {}}' "output.csv"
```

Should be easier in Python. Full script is at [script/check_schema.py](script/check_schema.py) at here are the extract

```py
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
```

```py
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
```

## Result

### Yellow taxi

| year | schema |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |
| ---- | ------ |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |
| 2009-2014 | vendor_id|pickup_datetime|dropoff_datetime|passenger_count|trip_distance|pickup_longitude|pickup_latitude|rate_code|store_and_fwd_flag|dropoff_longitude|dropoff_latitude|payment_type|fare_amount|surcharge|mta_tax|tip_amount|tolls_amount|total_amount |
| 2015-2016 | VendorID|tpep_pickup_datetime|tpep_dropoff_datetime|passenger_count|trip_distance|pickup_longitude|pickup_latitude|RateCodeID|store_and_fwd_flag|dropoff_longitude|dropoff_latitude|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount |
| 2017-2018 | VendorID|tpep_pickup_datetime|tpep_dropoff_datetime|passenger_count|trip_distance|RatecodeID|store_and_fwd_flag|PULocationID|DOLocationID|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount|
 | 2019-2020 | VendorID|tpep_pickup_datetime|tpep_dropoff_datetime|passenger_count|trip_distance|RatecodeID|store_and_fwd_flag|PULocationID|DOLocationID|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount|congestion_surcharge |

 ### Green taxi
| year | schema |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |
| ---- | ------ |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |
| 2014 | VendorID|lpep_pickup_datetime|Lpep_dropoff_datetime|Store_and_fwd_flag|RateCodeID|Pickup_longitude|Pickup_latitude|Dropoff_longitude|Dropoff_latitude|Passenger_count|Trip_distance|Fare_amount|Extra|MTA_tax|Tip_amount|Tolls_amount|Ehail_fee|Total_amount|Payment_type|Trip_type |
| 2015-2016 | VendorID|lpep_pickup_datetime|Lpep_dropoff_datetime|Store_and_fwd_flag|RateCodeID|Pickup_longitude|Pickup_latitude|Dropoff_longitude|Dropoff_latitude|Passenger_count|Trip_distance|Fare_amount|Extra|MTA_tax|Tip_amount|Tolls_amount|Ehail_fee|improvement_surcharge|Total_amount|Payment_type|Trip_type |
| 2017-2018 | VendorID|lpep_pickup_datetime|lpep_dropoff_datetime|store_and_fwd_flag|RatecodeID|PULocationID|DOLocationID|passenger_count|trip_distance|fare_amount|extra|mta_tax|tip_amount|tolls_amount|ehail_fee|improvement_surcharge|total_amount|payment_type|trip_type |
| 2019-2020 | VendorID|lpep_pickup_datetime|lpep_dropoff_datetime|store_and_fwd_flag|RatecodeID|PULocationID|DOLocationID|passenger_count|trip_distance|fare_amount|extra|mta_tax|tip_amount|tolls_amount|ehail_fee|improvement_surcharge|total_amount|payment_type|trip_type|congestion_surcharge |

### For-hire vehicle
| year | schema |- |- |- |- |- |- |
| ---- | ------ |- |- |- |- |- |- |
| 2015-2016 | Dispatching_base_num|Pickup_date|locationID |
| 2017 | Dispatching_base_num|Pickup_DateTime|DropOff_datetime|PUlocationID|DOlocationID |
| 2018 | Pickup_DateTime|DropOff_datetime|PUlocationID|DOlocationID|SR_Flag|Dispatching_base_number|Dispatching_base_num |
| 2019-2020 | dispatching_base_num|pickup_datetime|dropoff_datetime|PULocationID|DOLocationID|SR_Flag |

### High volume for-hire vehicle
| year | schema |- |- |- |- |- |- |
| ---- | ------ |- |- |- |- |- |- |
| 2019-2020 | hvfhs_license_num|dispatching_base_num|pickup_datetime|dropoff_datetime|PULocationID|DOLocationID|SR_Flag |