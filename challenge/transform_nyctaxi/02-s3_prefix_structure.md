- [Challenge 2](#challenge-2)
  - [Method](#method)
    - [Copying files from S3 to local folders](#copying-files-from-s3-to-local-folders)
    - [Compress the files](#compress-the-files)
    - [Copy the files to S3](#copy-the-files-to-s3)

# Challenge 2
How we organize files into S3 folders (or prefix to be exact) plays a very important role in performance, from both processing and querying point of view.

> EC2 instance for conversion:
> * Region: us-east-1
> * Instance size: t4g-xlarge (Amazon Linux 2)
> * storage: 400GB gp2


## Method

Target S3 prefix structure:

```
s3://bucket/raw/nyc-tlc/
                           PRE fhv/
                           PRE fhvhv/
                           PRE green/
                           PRE yellow/
```

### Copying files from S3 to local folders
```
aws s3 cp "s3://nyc-tlc/trip data/" ~/nyc-tlc/yellow --recursive --exclude "*" --include "yellow_*" --dryrun

(240GB)
```

Repeat for *green*, *fhv* and *fhvhv*
```
aws s3 cp "s3://nyc-tlc/trip data/" ~/nyc-tlc/green --recursive --exclude "*" --include "green_*" --dryrun

(10GB)

aws s3 cp "s3://nyc-tlc/trip data/" ~/nyc-tlc/fhv --recursive --exclude "*" --include "fhv_*" --dryrun

(36GB)

aws s3 cp "s3://nyc-tlc/trip data/" ~/nyc-tlc/fhvhv --recursive --exclude "*" --include "fhvhv_*" --dryrun

(15GB)
```

### Compress the files
In each taxi type folder, compress the files
```
gzip *.csv
```

> The largest compressed file is around 600MB in size.

### Copy the files to S3
```
aws s3 cp ~/nyc-tlc/ "s3://bucket/raw/nyc-tlc/" --recursive --exclude "*" --include "*.csv.gz" --dryrun
```
