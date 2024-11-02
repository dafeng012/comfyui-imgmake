from img_ebsynth.image2mask import *
from img_ebsynth.video2image import *
from img_ebsynth.gj_image import *
from img_ebsynth.load_images_nodes import *
from img_ebsynth.image_name_slect import *
from img_ebsynth.ebs import *
from img_ebsynth.main import *
NODE_CLASS_MAPPINGS = {
    "image2mask": image2mask,
    "video2image": Video2Frames,
    "VideoKeyFramesExtractor": VideoKeyFramesExtractor,
    "LoadImageListPlus": LoadImageListPlus,
    "SaveImageExtended": SaveImageExtended,
    "LoadImagesFromPath_lp":LoadImagesFromPath_lp,
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
    "LoadImagesFromPath_lp": "LoadImagesFromPath_lp",
    "SelectImageName": "SelectImageName",
    "ebsynth_process": "ebsynth_process",
    "ebsynth_hecheng": "ebsynth_hecheng",
    "ebsynth_main": "ebsynth_main",
}
