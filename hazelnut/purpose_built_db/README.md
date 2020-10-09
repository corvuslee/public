# AWS Region

> Please use the `us-east-1` region

# Lab 1: RDBMS - Amazon Aurora (45 mins)
In this lab, we are going to learn about the basic of Amazon Aurora

1. Provision an Aurora MySQL serverless cluster for quick development
2. Use snapshot to deploy into a production Aurora MySQL provisioned cluster
3. Explore different options of read replica to increase the availability
4. Explore common operations such as monitoring and patching

Go to [Aurora lab guide](aurora/README.md)

# Lab 2: Cache - Amazon ElastiCache (45 mins)
In this lab, we are going to learn 1) how to deploy Amazon ElastiCache as an in-memory caching layer to the RDBMS, and 2) sample application code to work with Redis

1. Provision a ElastiCache for Redis cluster
2. Review the cache-aside strategy and related Python code
3. Explore different options of scaling
4. Explore common operations such as monitoring and patching

Go to [ElastiCache lab guide](elasticache/README.md)

# Lab 3: NoSQL - Amazon DynamoDB (45 mins)
In this lab, we are going to learn about Amazon DynamoDB, with some basic data modelling

1. Create a DynamoDB table
2. Load and retrieve a few items using boto3
3. Visualize the data model
4. Create a global secondary index for another query pattern
5. Update an item
6. Explore common operations

Go to [DynamoDB lab guide](dynamodb/README.md)