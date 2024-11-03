from .img_ebsynth.image2mask import image2mask,SaveImage_lp
from .img_ebsynth.video2image import Video2Frames,LoadImageListPlus
from .img_ebsynth.gj_image import VideoKeyFramesExtractor
from .img_ebsynth.load_images_nodes import LoadImagesFromPath_lp
from .img_ebsynth.image_name_slect import SelectImageName
from .img_ebsynth.ebs import ebsynth_process,ebsynth_hecheng
from .img_ebsynth.main import ebsynth_main
NODE_CLASS_MAPPINGS = {
    "image2mask": image2mask,
    "video2image": Video2Frames,
    "VideoKeyFramesExtractor": VideoKeyFramesExtractor,
    "LoadImageListPlus": LoadImageListPlus,
    "SaveImage_lp": SaveImage_lp,
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
    "SaveImage_lp": "SaveImage_lp",
    "LoadImagesFromPath_lp": "LoadImagesFromPath_lp",
    "SelectImageName": "SelectImageName",
    "ebsynth_process": "ebsynth_process",
    "ebsynth_hecheng": "ebsynth_hecheng",
    "ebsynth_main": "ebsynth_main",
}
