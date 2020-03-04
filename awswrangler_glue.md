# Using AWS Wrangler in Glue where Internet is not Allowed

## Prerequisites

1. Get the latest wheel file for glue from https://github.com/awslabs/aws-data-wrangler/releases

2. Ready a Python 3.6 environment

## Download dependencies

Check the dependencies of the wheel file
```
pkginfo -f requires_dist awswrangler-0.3.2-glue-none-any.whl
```

For version 0.3.2, we can prepare a `requirements.txt` file as shown below:
```
numpy==1.18.1
pandas==1.0.1
pyarrow==0.16.0
botocore==1.13.34
boto3==1.10.34
s3fs==0.4.0
tenacity==6.0.0
pg8000==1.13.2
pymysql==0.9.3
```

Download the dependencies (~100MB)
```
pip download -r requirements.txt -d libs
```

Copy `awswrangler-0.3.2-glue-none-any.whl` into `libs` and we will get 19 wheel files
```
# ls -1 libs
awswrangler-0.3.2-glue-none-any.whl
boto3-1.10.34-py2.py3-none-any.whl
botocore-1.13.34-py2.py3-none-any.whl
docutils-0.15.2-py3-none-any.whl
fsspec-0.6.2-py3-none-any.whl
jmespath-0.9.5-py2.py3-none-any.whl
numpy-1.18.1-cp36-cp36m-manylinux1_x86_64.whl
pandas-1.0.1-cp36-cp36m-manylinux1_x86_64.whl
pg8000-1.13.2-py3-none-any.whl
pyarrow-0.16.0-cp36-cp36m-manylinux1_x86_64.whl
PyMySQL-0.9.3-py2.py3-none-any.whl
python_dateutil-2.8.1-py2.py3-none-any.whl
pytz-2019.3-py2.py3-none-any.whl
s3fs-0.4.0-py3-none-any.whl
s3transfer-0.2.1-py2.py3-none-any.whl
scramp-1.1.0-py3-none-any.whl
six-1.14.0-py2.py3-none-any.whl
tenacity-6.0.0-py2.py3-none-any.whl
urllib3-1.25.8-py2.py3-none-any.whl
```

Package as a zip file
```
cd libs
zip ../awswrangler-depends.zip *
```

## Configure in Glue

1. Upload the zip file to S3
2. Add `s3://{bucket}/awswrangler-depends.zip` to the `Referenced files path` in the Glue job

## Edit the Glue job Python script
```python
import os.path
import subprocess
import sys

# borrowed from https://stackoverflow.com/questions/48596627/how-to-import-referenced-files-in-etl-scripts
def get_referenced_filepath(file_name, matchFunc=os.path.isfile):
    for dir_name in sys.path:
        candidate = os.path.join(dir_name, file_name)
        if matchFunc(candidate):
            return candidate
    raise Exception("Can't find file: ".format(file_name))

zip_file = get_referenced_filepath("awswrangler-depends.zip")

subprocess.run(["unzip", zip_file])

# Can't install --user, or without "-t ." because of permissions issues on the filesystem
subprocess.run(["pip3 install --no-index --find-links=. -t . *.whl"], shell=True)

# Todo: get rid of shell=True
# subprocess.run(["pip3", "install", "--no-index", "--find-links=.", "-t", ".", "*.whl"])

# Start the script here
import awswrangler
```
