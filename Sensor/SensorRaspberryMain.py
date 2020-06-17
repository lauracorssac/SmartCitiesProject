# python3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import sys
import os

import picamera
import subprocess

from PIL import Image
import tensorflow as tf
from datetime import datetime

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

sys.path.insert(1, os.path.dirname(os.getcwd()))

from Common.MQTTClientSerializer import MQTTClientSerializer
from ImageRecognitionManager import ImageRecognitionManager
from PIRManager import PIRManager

camera = picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30)
recognition_turned_on = True

def personWasDetected(results):
    for result in results:
        if result['class_id'] == 0:
            return True
    return False

 #function called when a notification of a new menu action is received by mbp client
def motion_recognized_callback():

    print("motion_recognized_callback")

    global recognition_turned_on
    recognition_turned_on = True


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

    image_rec_manager = ImageRecognitionManager()
    pir_manager = PIRManager(motion_recognized_callback)

    while True:
        try:
            if recognition_turned_on:
                print("recognition turned on")
                stream = io.BytesIO()
                capture = camera.capture(stream, format='jpeg', use_video_port=True)
                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS)
                results = image_rec_manager.detect_objects(interpreter, image, args.threshold)
                if personWasDetected(results) and recognition_turned_on:
                    print("PERSON WAS DETECTED")
                    message = '{"value": "%.2f"}' % 1.0
                    mqtt_client.publish(topic="sensor/personRecognition", payload=message, qos=0, retain=False)
                else:
                    print("PERSON NOT DETECTED")
                    message = '{"value": "%.2f"}' % 0.0
                    mqtt_client.publish(topic="sensor/personRecognition", payload=message, qos=0, retain=False)

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
