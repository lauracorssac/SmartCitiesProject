import numpy as np

class ImageRecognitionManager(object):

    def set_input_tensor(self, interpreter, image):
      """Sets the input tensor."""
      tensor_index = interpreter.get_input_details()[0]['index']
      input_tensor = interpreter.tensor(tensor_index)()[0]
      input_tensor[:, :] = image

    def get_output_tensor(self, interpreter, index):
      """Returns the output tensor at the given index."""
      output_details = interpreter.get_output_details()[index]
      tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
      return tensor

    def detect_objects(self, interpreter, image, threshold):
      """Returns a list of detection results, each a dictionary of object info."""
      self.set_input_tensor(interpreter, image)
      interpreter.invoke()

      # Get all output details
      boxes = self.get_output_tensor(interpreter, 0)
      classes = self.get_output_tensor(interpreter, 1)
      scores = self.get_output_tensor(interpreter, 2)
      count = int(self.get_output_tensor(interpreter, 3))

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
