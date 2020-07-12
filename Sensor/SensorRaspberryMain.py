# python3
from __future__ import absolute_import
from __future__ import division

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

process_stopped = True
 #function called when a notification of a new menu action is received by mbp client
def motion_recognized_callback(PIN):

    print("motion_recognized_callback")
    global process_stopped
    if process_stopped == True:
        process_stopped = False
        start_cam_analise()



def start_cam_analise():

    camera_manager = CameraManager()
    camera_manager.open_camera()
    global image_rec_manager
    global process_stopped
    global message_manager
    if image_rec_manager.analize_image(camera_manager.camera):
        print("PERSON WAS DETECTED")
        message_manager.send_person_rec_status(1.0)
        start_time = time.time()
        while time.time() - start_time < 91:
            message_manager.send_time(time.time() - start_time)
            time.sleep(1)
    else:
        camera_manager.close_camera()
        print("PERSON NOT DETECTED")
        message_manager.send_person_rec_status(0.0)

    process_stopped = True
    camera_manager.close_camera()


def main():

    print("main fcuntion")
    global recognition_turned_on
    recognition_turned_on = False

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='File path of .tflite file.',
                        required=False, default='detect.tflite')
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
    global message_manager
    message_manager = SensorMQTTMessageManager(mqtt_client)

    iot_manager = IoTGeneralManager()
    iot_manager.start()
    global image_rec_manager
    image_rec_manager = ImageRecognitionManager(args.model, args.threshold)
    pir_manager = PIRManager(motion_recognized_callback, 20)

    while True:
        pass

    print("ending program. Please wait.")
    iot_manager.stop()
    mqtt_client.finalize()
    camera_manager.close_camera()
    return

if __name__ == '__main__':
    main()
