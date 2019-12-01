import os
import base64
from django.core.files import File

def encode_base64(filepath):
  with open(filepath, 'rb') as f:
    image = File(f)
    data = base64.b64encode(image.read())
    return data

def decode_base64(filename, strData):
  with open(filename, 'wb+') as f:
    data = base64.b64decode(strData)
    f.write(data)

def get_image_filename(itemId):
  return os.getcwd() + "/media/" + str(itemId) + ".jpg"