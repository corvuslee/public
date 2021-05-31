"""
Convert raw PASCAL dataset to TFRecord for object_detection.
Example usage:
    python object_detection/dataset_tools/create_custom_pascal_tf_record.py \
        --data_dir=$HOME/Desktop/dataset/val \
        --output_path=$HOME/Desktop/dataset/test/val.tfrecord \
        --label_map_path=$HOME/Desktop/dataset/label_map.pbtxt

Reference:
https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_pascal_tf_record.py
"""

import hashlib
import io
import logging
import os
from pathlib import Path

from lxml import etree
import PIL.Image
import tensorflow.compat.v1 as tf

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util


flags = tf.app.flags
flags.DEFINE_string('data_dir', '', 'Root directory to PASCAL dataset.')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('label_map_path', 'data/pascal_label_map.pbtxt',
                    'Path to label map proto')
FLAGS = flags.FLAGS


def dict_to_tf_example(data, data_dir, label_map_dict):
    """Convert XML derived dict to tf.Example proto.
    Notice that this function normalizes the bounding box coordinates provided
    by the raw data.
    Args:
        data: dict holding PASCAL XML fields for a single image (obtained by
        running dataset_util.recursive_parse_xml_to_dict)
        label_map_dict: A map from string label names to integers ids.
    Returns:
        example: The converted tf.Example.
    Raises:
        ValueError: if the image is not a valid JPEG
    """

    # Handling JPG
    img_path = os.path.join(data['filename'])
    full_path = os.path.join(data_dir, img_path)
    logging.info(f'Processing image {full_path}')

    with tf.gfile.GFile(full_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)
    if image.format not in ('JPEG', 'MPO'):
        raise ValueError(f'Wrong image format {image.format}')
    key = hashlib.sha256(encoded_jpg).hexdigest()

    width = int(data['size']['width'])
    height = int(data['size']['height'])

    # Metadata
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []

    if 'object' in data:
        for obj in data['object']:

            xmin.append(float(obj['bndbox']['xmin']) / width)
            ymin.append(float(obj['bndbox']['ymin']) / height)
            xmax.append(float(obj['bndbox']['xmax']) / width)
            ymax.append(float(obj['bndbox']['ymax']) / height)
            classes_text.append(obj['name'].encode('utf8'))
            classes.append(label_map_dict[obj['name']])

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(
            data['filename'].encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(
            data['filename'].encode('utf8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes)
    }))
    return example


def main(_):
    data_dir = FLAGS.data_dir
    label_map_path = FLAGS.label_map_path
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    logging.info(f'Loading label map from {label_map_path}')
    label_map_dict = label_map_util.get_label_map_dict(label_map_path)

    logging.info(f'Reading from PASCAL dataset in {data_dir}')
    xml_folder = Path(data_dir).rglob('*.xml')
    xml_files = [x for x in xml_folder]

    for file in xml_files:
        logging.info(f'<={file}')
        with tf.gfile.GFile(file, 'r') as fid:
            xml_str = fid.read()
        xml = etree.fromstring(xml_str)
        data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

        tf_example = dict_to_tf_example(data, data_dir, label_map_dict)
        writer.write(tf_example.SerializeToString())

    writer.close()


if __name__ == '__main__':
    tf.app.run()
