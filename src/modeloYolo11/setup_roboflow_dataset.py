import tensorflow as tf
from roboflow import Roboflow
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
from roboflow import Roboflow
rf = Roboflow(api_key=api_key)
project = rf.workspace("lvaro-czewi").project("treedetector-xmdts")
version = project.version(2)
dataset = version.download("yolov11")
                