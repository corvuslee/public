# Work in progress

- [Work in progress](#work-in-progress)
- [Preparation](#preparation)
  - [Create a new conda environment](#create-a-new-conda-environment)
- [Draw bounding boxes](#draw-bounding-boxes)
- [Convert to tfrecord](#convert-to-tfrecord)
- [Retrain the object detection model](#retrain-the-object-detection-model)
  - [Setup the Docker container](#setup-the-docker-container)
  - [Organize the dataset](#organize-the-dataset)
  - [Prepare the checkpoint directory](#prepare-the-checkpoint-directory)
  - [Configure the training pipeline](#configure-the-training-pipeline)
  - [Start the retrain process](#start-the-retrain-process)
- [Compile the model for Edge TPU](#compile-the-model-for-edge-tpu)

# Preparation

## Create a new conda environment

environment.yml
```yml
name: labelImg
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.8
  - tensorflow
  - pillow
```

Activate the env and install labelImg with pip
```
pip3 install labelImg
```

# Draw bounding boxes

Put the JPG images under two folders:
* dataset/train
* dataset/eval

```sh
labelImg
```

1. **Open Dir**: dataset/eval
2. **Change Save Dir**: dataset/eval (same folder)
3. **Save format**: PascalVOC
4. For each image, click **Create RectBox** and draw bounding boxes around each objects that need to be detected

> When finished, we will see the JPG & XML file pair in the same folder.

# Convert to tfrecord

1. Clone the TensorFlow Model Garden
```
git clone https://github.com/tensorflow/models.git --depth 1
```
2. Stay in the research directory: `models/research`

3. Compile the proto files
```
protoc object_detection/protos/*.proto --python_out=.
```
4. Modify `PYTHONPATH`
```
export PYTHONPATH=$PYTHONPATH:`pwd`
```
5. Modify the [sample file](https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_pascal_tf_record.py) to fit with the dataset. There is a basic one in [scripts/create_custom_pascal_tf_record.py](scripts/create_custom_pascal_tf_record.py)

6. Created two files
   * train.tfrecord
   * eval.tfrecord

# Retrain the object detection model

> Ref: https://www.coral.ai/docs/edgetpu/retrain-detection/

## Setup the Docker container

Follow the steps in the guide above, and mount additional directory

```
docker run --name edgetpu-detect \
--rm -it --privileged -p 6006:6006 \
--mount type=bind,src=${PWD}/out,dst=/tensorflow/models/research/learn_pet \
--mount type=bind,src=${PWD}/couchpotato,dst=/tensorflow/models/research/couchpotato \
detect-tutorial-tf1
```

## Organize the dataset

Within the docker container (tensorflow/models/research/):

* couchpotato/dataset
* couchpotato/dataset/val.tfrecord
* couchpotato/dataset/label_map.pbtxt
* couchpotato/dataset/train.tfrecord
* couchpotato/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz

> The model file can be copied from the `learn_pet` directory

## Prepare the checkpoint directory
```
tar -xzvf couchpotato/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz
mv ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03 ckpt
```

## Configure the training pipeline

file:constants.sh
```sh
# LEARN_DIR="${OBJ_DET_DIR}/learn_pet"
LEARN_DIR="${OBJ_DET_DIR}/couchpotato"
CKPT_DIR="${LEARN_DIR}/ckpt"
TRAIN_DIR="${LEARN_DIR}/train"
OUTPUT_DIR="${LEARN_DIR}/models"
```

Modify `pipeline.config` following the [official guide](https://www.coral.ai/docs/edgetpu/retrain-detection/#configure-your-training-pipeline)

## Start the retrain process

```sh
NUM_TRAINING_STEPS=500 && \
NUM_EVAL_STEPS=100

# From the /tensorflow/models/research/ directory
./retrain_detection_model.sh \
--num_training_steps ${NUM_TRAINING_STEPS} \
--num_eval_steps ${NUM_EVAL_STEPS}
```
> Tested on a m5a.4xlarge EC2 instance. If the processed is killed without error message, try increasing the memory.

> Wrap everything within a `screen` as the process can take hours
> * screen -list
> * screen -d
> * screen -r

# Compile the model for Edge TPU

