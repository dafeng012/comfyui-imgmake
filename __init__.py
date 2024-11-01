from .image2mask import *
from .video2image import *
from .gj_image import *
from .load_images_nodes import *
from .image_name_slect import *
from .ebs import *
from .main import *
NODE_CLASS_MAPPINGS = {
    "image2mask": image2mask,
    "video2image": Video2Frames,
    "VideoKeyFramesExtractor": VideoKeyFramesExtractor,
    "LoadImageListPlus": LoadImageListPlus,
    "SaveImageExtended": SaveImageExtended,
    "LoadImagesFromPath":LoadImagesFromPath,
    "loadImagesFromFile": loadImagesFromFile,
    "SelectImageName":SelectImageName,
    "ebsynth_process":ebsynth_process,
    "ebsynth_hecheng":ebsynth_hecheng,
    "ebsynth_main":ebsynth_main,
    
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "image2mask": "image2mask",
    "video2image": "video2image",
    "VideoKeyFramesExtractor": "VideoKeyFramesExtractor",
    "LoadImageListPlus": "LoadImageListPlus",
    "SaveImagePlus": "SaveImageExtended",
    "SaveImageExtended": "SaveImageExtended",
    "LoadImagesFromPath": "LoadImagesFromPath",
    "loadImagesFromFile": "loadImagesFromFile",
    "SelectImageName": "SelectImageName",
    "ebsynth_process": "ebsynth_process",
    "ebsynth_hecheng": "ebsynth_hecheng",
    "ebsynth_main": "ebsynth_main",
}
