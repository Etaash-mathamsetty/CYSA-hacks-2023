import tensorflow as tf
import numpy as np
import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

configs = config_util.get_configs_from_pipeline_file("../trainingai/Tensorflow/workspace/models/my_ssd_mobnet/pipeline.config")
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join("../trainingai/Tensorflow/workspace/models/my_ssd_mobnet", 'ckpt-11')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

# add more in future if needed
labels = [{'name': 'tylenol', 'id': 1}, {'name': 'peroxide', 'id': 2}, 
          {'name': 'move free', 'id': 3}, {'name': 'motrin', 'id': 4}]   
Threshold = 0.3

def ExtractBBoxes(bboxes, bclasses, bscores, width, height):
    bbox = []
    class_labels = []
    for idx in range(len(bboxes)):
        if bscores[idx] >= Threshold:
            y_min = int(bboxes[idx][0] * height)
            x_min = int(bboxes[idx][1] * width)
            y_max = int(bboxes[idx][2] * height)
            x_max = int(bboxes[idx][3] * width)
            class_label = labels[int(bclasses[idx])]['name']
            # peroxide detection is really bad
            # if(class_label == "peroxide"):
                # continue
            class_labels.append(class_label)
            bbox.append([x_min, y_min, x_max, y_max, class_label, float(bscores[idx])])
            print(f"label: {labels[int(bclasses[idx])]['name']}, score: {float(bscores[idx])}")
    return (bbox, class_labels)

def get_classification(image_path):

    image = tf.image.decode_image(open(image_path, 'rb').read(), channels=3)
    # Change this resolution if needed
    image = tf.image.resize(image, (320, 213))

    input_tensor = tf.expand_dims(image, 0)
    detections = detect_fn(input_tensor)

    bboxes = detections['detection_boxes'][0].numpy()
    bclasses = detections['detection_classes'][0].numpy().astype(np.int32)
    bscores = detections['detection_scores'][0].numpy()
    _, class_labels = ExtractBBoxes(bboxes, bclasses, bscores, image.shape[1], image.shape[0])

    return class_labels


if __name__ == "__main__":
    print(get_classification("validation_images/DSC_4685.JPG"))
