Apart from dashboard/reporting, another main use of data lake is training predictive models with machine learning (ML). In this task you will get started with Amazon SageMaker, explore a Jupyter notebook with codes performing ad-hoc query to the data lake through `PyAthena`.

> **Amazon SageMaker Studio** is a ML IDE for building, training, and debugging models, tracking experiments, deploying models, and monitoring their performance.
> 
> **Amazon SageMaker Python SDK** is an open source library for training and deploying machine-learned models on Amazon SageMaker

![09-eda](images/09_eda.png)

# Provisioning

1. Go to the [Amazon SageMaker console](https://console.aws.amazon.com/sagemaker)
2. Click **Amazon SageMaker Studio**
3. Execution role:
   1. Create a role
   2. Allow access to any S3 bucket
   3. Click **Create role**
   ![sagemaker studio provisioning](images/sagemaker-studio-provisioning.png)
4. Open Studio when the provisioning process has completed

## Additional IAM permissions
1. Go to the [IAM console](https://console.aws.amazon.com/iam)
2. Click **Roles**
3. Search for *AmazonSageMaker-ExecutionRole-xxxx*
4. Click **Attach policies**
5. Select *AmazonAthenaFullAccess*
6. Click **Attach policy**
   ![sagemaker-athena-policy](images/sagemaker-athena-policy.png)

# Data exploration

1. Open the page [09a_Amazon Customer Reviews - EDA.ipynb](09a_Amazon%20Customer%20Reviews%20-%20EDA.ipynb)
2. Download the ipynb file
3. Upload the file to the Studio environment (Jupyter) and follow the instructions within

