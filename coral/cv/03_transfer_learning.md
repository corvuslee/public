- [1. Preparation](#1-preparation)
  - [1.1. Create a new conda environment](#11-create-a-new-conda-environment)
- [2. Draw bounding boxes](#2-draw-bounding-boxes)
- [3. Convert to TFRecord](#3-convert-to-tfrecord)
- [4. Retrain the object detection model](#4-retrain-the-object-detection-model)
  - [4.1. Setup the Docker container](#41-setup-the-docker-container)
  - [4.2. Organize the dataset](#42-organize-the-dataset)
  - [4.3. Prepare the checkpoint directory](#43-prepare-the-checkpoint-directory)
  - [4.4. Configure the training pipeline](#44-configure-the-training-pipeline)
  - [4.5. Start the retrain process](#45-start-the-retrain-process)
- [5. Compile the model for Edge TPU](#5-compile-the-model-for-edge-tpu)
- [6. Test the new model](#6-test-the-new-model)

To start with, we can base on the a [pretrained model](https://coral.ai/models/object-detection/) -- SSD MobileNet v2 with the COCO dataset. There is a class called "person" in the COCO dataset, meaning that there is a high chance we can fine tune the model (i.e., transfer learning) to recognize individual family member.

# 1. Preparation

## 1.1. Create a new conda environment

environment.yml
```yml
name: coral
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.8
  - tensorflow
  - pillow
```

Activate the env and install [labelImg](https://github.com/tzutalin/labelImg) with pip
```
pip3 install labelImg
```

# 2. Draw bounding boxes

To fine tune the model recognizing individual family member, we need ground truth images. For this project, we have gathered 50 photos per person, and put the JPG images under two folders:
* dataset/train
* dataset/val

```sh
labelImg
```

Annotate both the train and val dataset. Below is an example for the val dataset only:
1. **Open Dir**: dataset/val
2. **Change Save Dir**: dataset/val (same folder)
3. **Save format**: PascalVOC
4. For each image, click **Create RectBox** and draw bounding boxes around each objects that need to be detected

> When finished, we will see the JPG & XML file pair in the same folder.

# 3. Convert to TFRecord

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
   * val.tfrecord

# 4. Retrain the object detection model

> Ref: https://www.coral.ai/docs/edgetpu/retrain-detection/

## 4.1. Setup the Docker container

Follow the steps in the guide above, and mount additional directory `couchpotato`

```
docker run --name edgetpu-detect \
--rm -it --privileged -p 6006:6006 \
--mount type=bind,src=${PWD}/out,dst=/tensorflow/models/research/learn_pet \
--mount type=bind,src=${PWD}/couchpotato,dst=/tensorflow/models/research/couchpotato \
detect-tutorial-tf1
```

## 4.2. Organize the dataset

Within the docker container (tensorflow/models/research/):

* couchpotato/dataset
* couchpotato/dataset/val.tfrecord
* couchpotato/dataset/label_map.pbtxt
* couchpotato/dataset/train.tfrecord
* couchpotato/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz

> The model file can be downloaded from https://coral.ai/models/object-detection/

> Looks like the SSDLite MobileDet has a higher mAP, which worths a try.

## 4.3. Prepare the checkpoint directory
```
tar -xzvf couchpotato/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz
mv ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03 ckpt
```

## 4.4. Configure the training pipeline

file:constants.sh
```sh
# LEARN_DIR="${OBJ_DET_DIR}/learn_pet"
LEARN_DIR="${OBJ_DET_DIR}/couchpotato"
CKPT_DIR="${LEARN_DIR}/ckpt"
TRAIN_DIR="${LEARN_DIR}/train"
OUTPUT_DIR="${LEARN_DIR}/models"
```

Modify `pipeline.config` following the [official guide](https://www.coral.ai/docs/edgetpu/retrain-detection/#configure-your-training-pipeline)

## 4.5. Start the retrain process

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

# 5. Compile the model for Edge TPU

> Ref: https://www.coral.ai/docs/edgetpu/retrain-detection/#compile-the-model-for-the-edge-tpu

```sh
# From the Docker /tensorflow/models/research directory
./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num 500
```

Follow the guide above to:
1. Convert a checkpoint to TF Lite file
2. Install `edgetpu-compiler`

3. Change the directory ownership
```sh
sudo chown -R $USER ${HOME}/google-coral/tutorials/docker/object_detection/couchpotato 
```

4. Modify `labels.txt` in the `models` directory

```sh
# labels.txt
0 object_A
1 object_B
2 ...

```

5. Compile the TF lite file to the Edge TPU platform
```
edgetpu_compiler output_tflite_graph.tflite
```

6. Rename the file
```
mv output_tflite_graph_edgetpu.tflite ssd_mobilenet_v2_couchpotato_quant_edgetpu.tflite
```

# 6. Test the new model

1. Push the files to the Coral board
```
mdt push ssd_mobilenet_v2_couchpotato_quant_edgetpu.tflite

mdt push labels.txt
```

2. Run the detection
```
edgetpu_detect_server --model ssd_mobilenet_v2_couchpotato_quant_edgetpu.tflite --labels labels.couchpotato.txt
```

Notice the performance (i.e. confidence) of recognizing each family member, and re-train with more ground truth images if required. Once we are satisfied with the object detection model, we can work on storing the metrics in Elasticsearch for further analysis.