
- [Lab 1: RDBMS - Amazon Aurora (30 mins)](#lab-1-rdbms---amazon-aurora-30-mins)
- [Lab 2: Cache - Amazon ElastiCache (45 mins)](#lab-2-cache---amazon-elasticache-45-mins)
- [Lab 3: NoSQL - Amazon DynamoDB (45 mins)](#lab-3-nosql---amazon-dynamodb-45-mins)

> Use `us-east-1` region

# Lab 1: RDBMS - Amazon Aurora (30 mins)
In this lab, we are going to learn about the basic of Amazon Aurora

1. Provision a serverless Aurora MySQL cluster for quick development
2. Load sample data into the development database
3. Use snapshot to deploy into a production Aurora MySQL provisioned cluster
4. Explore different options of read replica to increase the availability
5. Explore common operations such as monitoring and patching

Go to [Aurora lab guide](aurora/README.md)

# Lab 2: Cache - Amazon ElastiCache (45 mins)
In this lab, we are going to learn how to deploy Amazon ElastiCache as an in-memory caching layer to the RDBMS

1. Provision a ElastiCache for Redis cluster
2. Review how to write a Python function using cache-aside strategy
3. Explore different options of scaling
4. Explore common operations such as monitoring and patching

Go to [ElastiCache lab guide](elasticache/README.md)

# Lab 3: NoSQL - Amazon DynamoDB (45 mins)
In this lab, we are going to learn about Amazon DynamoDB, with some basic data modelling

1. Create a DynamoDB table
2. Load and retrieve a few items using boto3
3. Visualize the data model
4. Create a global secondary index for another access pattern
5. Update an item

Go to [DynamoDB lab guide](dynamodb/README.md)