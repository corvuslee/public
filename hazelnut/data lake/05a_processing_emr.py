from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('reviews-transform').enableHiveSupport().getOrCreate()


# variables
s3_bucket='s3://data.set.corvus'  # change to your bucket name; without trailing slash
output_path=f'{s3_bucket}/reviews/us'


# functions
def run_query(query, show=True):
    """
    Custom function to run spark.sql. Default will submit the query and show the result.
    """
    if show:
        return spark.sql(query).show()
    else:
        return spark.sql(query)


# US marketplace only to avoid non-US character
df = run_query('''
SELECT
  marketplace, 
  customer_id, 
  review_id, 
  product_id, 
  product_parent, 
  product_title, 
  product_category,
  CAST(star_rating as INT) star_rating, 
  CAST(helpful_votes as INT) helpful_votes, 
  CAST(total_votes as INT) total_votes, 
  vine, 
  verified_purchase, 
  review_headline, 
  review_body, 
  CAST(review_date as DATE) review_date
FROM reviews.tsv
WHERE marketplace='US'
''', show=False)

# Sink
df.repartition('product_category')\
    .write.mode("OVERWRITE")\
    .option("maxRecordsPerFile", 1000000)\
    .partitionBy('product_category')\
    .parquet(output_path, compression='gzip')