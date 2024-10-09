import os


import cv2
import glob
from PIL import Image

from .stage5 import ebsynth_utility_stage5
from .stage7 import ebsynth_utility_stage7


# def x_ceiling(value, step):
#   return -(-value // step) * step

def dump_dict(string, d:dict):
    for key in d.keys():
        string += ( key + " : " + str(d[key]) + "\n")
    return string

class debug_string:
    txt = ""
    def print(self, comment):
        print(comment)
        self.txt += comment + '\n'
    def to_string(self):
        return self.txt

class ebsynth_process:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "project_dir": ("STRING", {}),
                "original_movie_path": ("STRING", {}),
                "mask_mode": ("STRING", {"values": ["None", "Invert"]}),
                "is_invert_mask": ("BOOLEAN", {"default": False, "true_value": "True", "false_value": "False"})
            },
        }
        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("info",)
    FUNCTION = "ebsynth_utility_process"
    CATEGORY = "IMAGEmake"

    def ebsynth_utility_process(self,project_dir:str, original_movie_path:str, mask_mode:str,is_invert_mask):
        args = locals()
        info = ""
        info = dump_dict(info, args)
        dbg = debug_string()

        
        
        if mask_mode == "Invert":
            is_invert_mask = True

        frame_path = os.path.join(project_dir , "video_frame")
        frame_mask_path = os.path.join(project_dir, "video_mask")

        if is_invert_mask:
            inv_path = os.path.join(project_dir, "inv")
            os.makedirs(inv_path, exist_ok=True)

            org_key_path = os.path.join(inv_path, "video_key")
            img2img_key_path = os.path.join(inv_path, "img2img_key")
            img2img_upscale_key_path = os.path.join(inv_path, "img2img_upscale_key")
        else:
            org_key_path = os.path.join(project_dir, "video_key")
            img2img_key_path = os.path.join(project_dir, "img2img_key")
            img2img_upscale_key_path = os.path.join(project_dir, "img2img_upscale_key")

        if mask_mode == "None":
            frame_mask_path = ""
        

        project_args = [project_dir, original_movie_path, frame_path, frame_mask_path, org_key_path, img2img_key_path, img2img_upscale_key_path]


        
        ebsynth_utility_stage5(dbg, project_args, is_invert_mask)
        
    

        return (info,)
class ebsynth_hecheng:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "project_dir": ("STRING", {}),
                "original_movie_path": ("STRING", {}),
                "blend_rate": ("FLOAT", {"default": 1, "min": 0, "max": 1, "step": 0.1}),
                "export_type": ("STRING", {"default": "mp4", "values": ["mp4"]}),
                "mask_mode": ("STRING", {"values": ["None", "Invert"]}),
                "is_invert_mask": ("BOOLEAN", {"default": False, "true_value": "True", "false_value": "False"})
            },
        }
        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("info",)
    FUNCTION = "ebsynth_utility_hecheng"
    CATEGORY = "IMAGEmake"
    def ebsynth_utility_hecheng(self,project_dir:str, original_movie_path:str, mask_mode:str,is_invert_mask,blend_rate:float, export_type:str):
        args = locals()
        info = ""
        info = dump_dict(info, args)
        dbg = debug_string()

        
        
        if mask_mode == "Invert":
            is_invert_mask = True

        frame_path = os.path.join(project_dir , "video_frame")
        frame_mask_path = os.path.join(project_dir, "video_mask")

        if is_invert_mask:
            inv_path = os.path.join(project_dir, "inv")
            os.makedirs(inv_path, exist_ok=True)

            org_key_path = os.path.join(inv_path, "video_key")
            img2img_key_path = os.path.join(inv_path, "img2img_key")
            img2img_upscale_key_path = os.path.join(inv_path, "img2img_upscale_key")
        else:
            org_key_path = os.path.join(project_dir, "video_key")
            img2img_key_path = os.path.join(project_dir, "img2img_key")
            img2img_upscale_key_path = os.path.join(project_dir, "img2img_upscale_key")

        if mask_mode == "None":
            frame_mask_path = ""
        

        project_args = [project_dir, original_movie_path, frame_path, frame_mask_path, org_key_path, img2img_key_path, img2img_upscale_key_path]

        ebsynth_utility_stage7(dbg, project_args, blend_rate, export_type, is_invert_mask)
        return (info,)


