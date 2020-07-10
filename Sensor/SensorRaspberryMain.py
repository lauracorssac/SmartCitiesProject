# python3
#from __future__ import absolute_import
#from __future__ import division

import argparse
import io
import re
import time
import sys
import os

from datetime import datetime

sys.path.insert(1, os.path.dirname(os.getcwd()))

from Common.MQTTClientSerializer import MQTTClientSerializer
from ImageRecognitionManager import ImageRecognitionManager
from PIRManager import PIRManager
from SensorMQTTMessageManager import SensorMQTTMessageManager
from Common.IoTGeneralManager import IoTGeneralManager
from CameraManager import CameraManager

recognition_turned_on = True

 #function called when a notification of a new menu action is received by mbp client
def motion_recognized_callback():

    print("motion_recognized_callback")

    global recognition_turned_on
    recognition_turned_on = True

def main():

    print("main fcuntion")
    global recognition_turned_on
    recognition_turned_on = False

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='File path of .tflite file.', required=False, default='detect.tflite')
    parser.add_argument(
    '--threshold',
    help='Score threshold for detected objects.',
    required=False,
    type=float,
    default=0.4)
    args = parser.parse_args()
   
    property_file_name = "SensorRaspberrySettings.json"
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    message_manager = SensorMQTTMessageManager(mqtt_client)

    iot_manager = IoTGeneralManager()
    iot_manager.start()
    image_rec_manager = ImageRecognitionManager(args.model, args.threshold)
    pir_manager = PIRManager(motion_recognized_callback)
    camera_manager = CameraManager()
    start_time = 0.0

    while True:
        try:
            if recognition_turned_on:
                camera_manager.open_camera()
                print("recognition turned on")
                if image_rec_manager.analize_image(camera_manager.camera) and recognition_turned_on:
                    print("PERSON WAS DETECTED")
                    if start_time == 0.0:
                        start_time = time.time()
                    message_manager.send_person_rec_status(1.0)
                else:
                    camera_manager.close_camera()
                    print("PERSON NOT DETECTED")
                    message_manager.send_person_rec_status(0.0)
                    recognition_turned_on = False
                
                if start_time != 0:
                    end_time = time.time()
                    diff = end_time - start_time
                    print("time measured = ", diff)
                    message_manager.send_time(diff)
        except:
            break

    print("ending program. Please wait.")
    iot_manager.stop()
    mqtt_client.finalize()
    camera_manager.close_camera()
    return

if __name__ == '__main__':
    main()
