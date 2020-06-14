# python3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import sys

import numpy as np
import picamera
import subprocess

from PIL import Image
import tensorflow as tf
from datetime import datetime
import base64

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

import pyrebase

import UploadVideo as VideoManager
from BuzzerManager import BuzzerManager
from MenuOption import MenuOption
from mbp_client import MBPclient
from MQTTClientSerializer import MQTTClientSerializer
from MQTTMessageManager import MQTTMessageManager

camera = picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30)
recognition_turned_on = True

def personWasDetected(results):
    for result in results:
        if result['class_id'] == 0:
            return True
    return False

def updatePersonDetectedStatus(status):
    data = {"personDetected": status}
    db.child("raspberryData").set(data)

def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor

def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results

def main():

    print("main fcuntion")

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='File path of .tflite file.', required=False, default='detect.tflite')
    parser.add_argument(
    '--threshold',
    help='Score threshold for detected objects.',
    required=False,
    type=float,
    default=0.4)
    args = parser.parse_args()
    # labels = load_labels(args.labels
    interpreter = tf.lite.Interpreter(args.model)
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

    property_file_name = "SensorRaspberrySettings.json"
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    manager = MQTTMessageManager(mqtt_client)

    while True:
        try:
            if recognition_turned_on:
                print("recognition turned on")
                stream = io.BytesIO()
                capture = camera.capture(stream, format='jpeg', use_video_port=True)
                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS)
                results = detect_objects(interpreter, image, args.threshold)
                if personWasDetected(results) and recognition_turned_on:
                    print("PERSON WAS DETECTED")
                    message = '{"value": "%.2f"}' % 1.0
                    mqtt_client.publish(topic="sensor/personRecognition", payload=message, qos=0, retain=False))
                else:
                    print("PERSON NOT DETECTED")
                    message = '{"value": "%.2f"}' % 0.0
                    mqtt_client.publish(topic="sensor/personRecognition", payload=message, qos=0, retain=False))

                stream.seek(0)
                stream.truncate()

        except:
            error = sys.exc_info()
            print ('Error:', str(error))
            break

    mqtt_client.finalize()
    camera.close()
    return

if __name__ == '__main__':
    main()
