- [Challenge 3](#challenge-3)
  - [Method](#method)
    - [Green taxi](#green-taxi)
    - [For-hire vehicle (FHV)](#for-hire-vehicle-fhv)
    - [The rest](#the-rest)

# Challenge 3
Schema evolution is common. However, in this dataset even if we force a Glue crawler to "Create a single schema for each S3 path", in some tables (e.g., green) the schema are considered incompatible and the crawler will create one table per file.

Develop the Spark code (in Python) to:
* Create dataframes from input files (CSV)
* Work on the schema compatibility across years and merge into a single one

EMR for code development:
* Region: us-east-1
* Software
  * Version: 6.2.0
  * Applications: Hadoop, Ganglia, JupyterEnterpriseGateway, Spark, Livy
  * Others: Use Glue data catalog for Spark table metadata
* Hardware
  * Master node: One m5.xlarge
  * Core node: Four m6g.xlarge
  * Task node: Zero m6g.xlarge
  * Cluster scaling: Max 4 core nodes (on-demand) and 26 task nodes (spot)

## Method

### Green taxi

Green taxi dataset is the smallest so we will start from here. Recall the schema is:

| year | schema |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |
| ---- | ------ |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |- |
| 2014 | VendorID|lpep_pickup_datetime|Lpep_dropoff_datetime|Store_and_fwd_flag|RateCodeID|Pickup_longitude|Pickup_latitude|Dropoff_longitude|Dropoff_latitude|Passenger_count|Trip_distance|Fare_amount|Extra|MTA_tax|Tip_amount|Tolls_amount|Ehail_fee|Total_amount|Payment_type|Trip_type |
| 2015-2016 | VendorID|lpep_pickup_datetime|Lpep_dropoff_datetime|Store_and_fwd_flag|RateCodeID|Pickup_longitude|Pickup_latitude|Dropoff_longitude|Dropoff_latitude|Passenger_count|Trip_distance|Fare_amount|Extra|MTA_tax|Tip_amount|Tolls_amount|Ehail_fee|improvement_surcharge|Total_amount|Payment_type|Trip_type |
| 2017-2018 | VendorID|lpep_pickup_datetime|lpep_dropoff_datetime|store_and_fwd_flag|RatecodeID|PULocationID|DOLocationID|passenger_count|trip_distance|fare_amount|extra|mta_tax|tip_amount|tolls_amount|ehail_fee|improvement_surcharge|total_amount|payment_type|trip_type |
| 2019-2020 | VendorID|lpep_pickup_datetime|lpep_dropoff_datetime|store_and_fwd_flag|RatecodeID|PULocationID|DOLocationID|passenger_count|trip_distance|fare_amount|extra|mta_tax|tip_amount|tolls_amount|ehail_fee|improvement_surcharge|total_amount|payment_type|trip_type|congestion_surcharge |

1. Start exploring the 2013-2014 data by instructing Spark to infer schema

```python
df1_raw = spark.read.csv(
    [green_2013, green_2014],
    header=True,
    inferSchema=True,
    timestampFormat='yyyy-MM-dd HH:mm:ss',
)
```

2. Check the summary statistics

```python
df1_raw.summary().show()
```

3. Manually define the schema. Rename the columns to make it compatible across all years

```python
# Changes:
# Upper case > lower case
# Ehail_fee - double


df1_schema = StructType([
    StructField('VendorID',IntegerType(),True),
    StructField('lpep_pickup_datetime',TimestampType(),True),
    StructField('lpep_dropoff_datetime',TimestampType(),True),
    StructField('store_and_fwd_flag',StringType(),True),
    StructField('RatecodeID',IntegerType(),True),
    StructField('Pickup_longitude',DoubleType(),True),
    StructField('Pickup_latitude',DoubleType(),True),
    StructField('Dropoff_longitude',DoubleType(),True),
    StructField('Dropoff_latitude',DoubleType(),True),
    StructField('passenger_count',IntegerType(),True),
    StructField('trip_distance',DoubleType(),True),
    StructField('fare_amount',DoubleType(),True),
    StructField('extra',DoubleType(),True),
    StructField('mta_tax',DoubleType(),True),
    StructField('tip_amount',DoubleType(),True),
    StructField('tolls_amount',DoubleType(),True),
    StructField('ehail_fee',DoubleType(),True),
    StructField('total_amount',DoubleType(),True),
    StructField('payment_type',IntegerType(),True),
    StructField('trip_type' ,IntegerType(),True)])
```

4. Load again the 2013-2014 data

```python
df1_raw = spark.read.csv(
    [green_2013, green_2014],
    schema=df1_schema,
    header=True,
    timestampFormat='yyyy-MM-dd HH:mm:ss',
)
```

5. Add more columns to make the schema the same across all years

```python
# Add: improvement_surcharge, PULocationID, DOLocationID, congestion_surcharge

df_2013_2014 = (df1_raw.withColumn('improvement_surcharge', lit(None).astype(DoubleType()))
                .withColumn('PULocationID', lit(None).astype(IntegerType()))
                .withColumn('DOLocationID', lit(None).astype(IntegerType()))
                .withColumn('congestion_surcharge', lit(None).astype(DoubleType()))
               )
```

6. Repeat the same for the remaining years
7. Merge all dataframes into a single one

```python
df_green = (df_2013_2014
            .unionByName(df_2015_2016)
            .unionByName(df_2017_2018)
            .unionByName(df_2019_2020)
           )
```

8. Check the summary statistics to confirm the merge
9. Write the dataframe to a staging folder for further cleansing

```python
df_green_final = (df_green
                  .withColumn("year", year('lpep_pickup_datetime'))
                  .withColumn("month", month('lpep_pickup_datetime'))
                 )

partitions = ['year', 'month']

(df_green_final
 .repartition(col(partitions[0]), col(partitions[1]))
 .write.mode("OVERWRITE")
 .option("maxRecordsPerFile", 1000000)
 .partitionBy(partitions)
 .parquet(output_path, compression="gzip"))
```


### For-hire vehicle (FHV)

Schema for the FHV dataset is quite a mess. Recall from challenge 1:

| year | schema |- |- |- |- |- |- |
| ---- | ------ |- |- |- |- |- |- |
| 2015-2016 | Dispatching_base_num|Pickup_date|locationID |
| 2017 | Dispatching_base_num|Pickup_DateTime|DropOff_datetime|PUlocationID|DOlocationID |
| 2018 | Pickup_DateTime|DropOff_datetime|PUlocationID|DOlocationID|SR_Flag|Dispatching_base_number|Dispatching_base_num |
| 2019-2020 | dispatching_base_num|pickup_datetime|dropoff_datetime|PULocationID|DOLocationID|SR_Flag |

### The rest

Yellow taxi and High volume for-hire vehicle follow similar approach, and we will skip it here.