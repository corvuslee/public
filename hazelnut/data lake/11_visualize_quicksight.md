In this task you will explore Amazon QuickSight, which is a serverless visualization services.

# Sign up

1. Go to the [QuickSight console](https://quicksight.aws.amazon.com/)
2. Sign up for QuickSight
3. Select the Enterprise Edition
4. Fill in the details
   * Use role based federation (SSO) - default
   * Region: *US East (N. Virginia)* for `us-east-1` - default
   * Account name: *qs-yourname*
   * Email address: *whatever*
   * Permission: Enable S3 access, and select the *data.set.yourname* bucket

> While waiting, explore the [Amazon QuickSight Gallery](https://aws.amazon.com/quicksight/gallery/) for sample industry and domain specific analytics.

# Dataset

1. Click **Datasets** on the left menu
2. Click **New dataset** on the top right corner
3. Click **Athena**
    * Name: *test*
    * Workgroup: *primary*
![New Athena data source](images/quicksight-new%20athena%20data%20source.png)
4. Click **Validate connection**
5. Click **Create data source**
6. Select the *reviews* database and *parquet_athena* table
![Select Athena table](images/quicksight-select%20athena%20table.png)
7. Select **Directly query your data**  and **Visualize**
![Finish dataset creation](images/quicksight-finish%20dataset%20creation.png)

# Analysis

![New analysis](images/quicksight-new%20analysis.png)

## Task 1: Review counts and average star rating per product category

1. Click **product category**
2. Click **star rating**
3. Expand **Field wells**
4. Add another **star rating** to Values
5. Change one star rating to (average) and the other to (count)
![Fields selection](images/quicksight-task1%20fields.png)
6. Select *scatter plot* in the visual types

Final result:
![Task 1 final](images/quicksight-task1%20final.png)

## Task 2: Review count per month over years

1. Add a new visual or sheet
2. Click **review date**
3. Select the x-axis (review date) and aggregate by *month*

Final result:
![Task 2 final](images/quicksight-task2%20final.png)