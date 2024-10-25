import os


import cv2
import glob
from PIL import Image

from .stage1 import ebsynth_utility_stage1,ebsynth_utility_stage1_invert
from .stage2 import ebsynth_utility_stage2
from .stage5 import ebsynth_utility_stage5
from .stage7 import ebsynth_utility_stage7
from .stage3_5 import ebsynth_utility_stage3_5


def x_ceiling(value, step):
  return -(-value // step) * step

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
class ebsynth_main:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "stage_index":("INT", {"default": 0, "values": [0,1,3,5,7]}),
                "project_dir": ("STRING", {}),
                "original_movie_path": ("STRING", {}),
                "frame_width": ("INT", {"default": -1}),
                "frame_height": ("INT", {"default": -1}),
                "st1_masking_method_index":("INT", {"default": 0, "values": [0,1,2]}),
                "st1_mask_threshold":("FLOAT", {"default": 0.1,"min":0,"max":1.0,"step":0.1}),
                "tb_use_fast_mode":("BOOLEAN", {"default": True, "true_value": "True", "false_value": "False"}),
                "tb_use_jit":("BOOLEAN", {"default": True, "true_value": "True", "false_value": "False"}),
                "clipseg_mask_prompt":("STRING", {"default": ""}),
                "clipseg_exclude_prompt":("STRING", {"default": ""}),
                "clipseg_mask_threshold":("INT", {"default": 0,"min":0,"max":1,"step":0.01}),
                "clipseg_mask_blur_size":("INT", {"default": 11}),
                "clipseg_mask_blur_size2":("INT", {"default": 11}),
                "key_min_gap":("INT", {"default": 10,"min":1,"max":100,"step":1}),
                "key_max_gap":("INT", {"default": 300,"min":1,"max":1000,"step":1}),
                "key_th":("FLOAT", {"default": 8.5,"min":0,"max":100,"step":0.1}),
                "key_add_last_frame":("BOOLEAN", {"default": True, "true_value": "True", "false_value": "False"}),
                "color_matcher_method":("STRING", {"default": "hm-mvgd-hm"}),
                "st3_5_use_mask":("BOOLEAN", {"default": True, "true_value": "True", "false_value": "False"}),
                "st3_5_use_mask_ref":("BOOLEAN", {"default": False, "true_value": "True", "false_value": "False"}),
                "st3_5_use_mask_org":("BOOLEAN", {"default": False, "true_value": "True", "false_value": "False"}),
                "color_matcher_ref_type":("INT", {"default": 0}),
                
                "blend_rate":("FLOAT", {"default": 1,"min":0,"max":1,"step":0.1}),
                "export_type":("STRING", {"default": "mp4", "values": ["gif", "webm","mp4","rawvideo"]}),

                "mask_mode": ("STRING", {"default": "Normal", "values": ["Normal", "Invert", "None"]}),
                "is_invert_mask": ("BOOLEAN", {"default": False, "true_value": "True", "false_value": "False"}),
                "devices":(["cuda:0", "cpu"],),
                "SYNTHS_PER_PROJECT":("INT", {"default": 15,"min":1,"max":20,"step":1}),
            },
            "optional": {
                # 应该默认是第一张
                "color_matcher_ref_image":("IMAGE", {"default": None}), 

                },
        }
        
    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("debug","info",)
    FUNCTION = "ebsynth_utility_process"
    CATEGORY = "IMAGEmake"

    def ebsynth_utility_process(self, stage_index: int, project_dir:str, original_movie_path:str, frame_width:int, frame_height:int, st1_masking_method_index:int, st1_mask_threshold:float, tb_use_fast_mode:bool, tb_use_jit:bool, clipseg_mask_prompt:str, clipseg_exclude_prompt:str, clipseg_mask_threshold:int, clipseg_mask_blur_size:int, clipseg_mask_blur_size2:int, key_min_gap:int, key_max_gap:int, key_th:float, key_add_last_frame:bool, color_matcher_method:str, st3_5_use_mask:bool, st3_5_use_mask_ref:bool, st3_5_use_mask_org:bool, color_matcher_ref_type:int,  blend_rate:float, export_type:str, mask_mode:str, is_invert_mask:bool, devices:str,SYNTHS_PER_PROJECT:int,color_matcher_ref_image:Image=None):
        args = locals()
        info = ""
        info = dump_dict(info, args)
        dbg = debug_string()

        if not os.path.isdir(project_dir):
            dbg.print("{0} project_dir not found".format(project_dir))
            return ( dbg, info )

        if not os.path.isfile(original_movie_path):
            dbg.print("{0} original_movie_path not found".format(original_movie_path))
            return ( dbg, info )
        
        is_invert_mask = False
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


        if stage_index == 0:
            ebsynth_utility_stage1(dbg, project_args, frame_width, frame_height, st1_masking_method_index, st1_mask_threshold, tb_use_fast_mode, tb_use_jit, clipseg_mask_prompt, clipseg_exclude_prompt, clipseg_mask_threshold, clipseg_mask_blur_size, clipseg_mask_blur_size2, is_invert_mask,devices)
            if is_invert_mask:
                inv_mask_path = os.path.join(inv_path, "inv_video_mask")
                ebsynth_utility_stage1_invert(dbg, frame_mask_path, inv_mask_path)

        elif stage_index == 1:
            ebsynth_utility_stage2(dbg, project_args, key_min_gap, key_max_gap, key_th, key_add_last_frame, is_invert_mask)
        
        elif stage_index == 3:
            ebsynth_utility_stage3_5(dbg, project_args, color_matcher_method, st3_5_use_mask, st3_5_use_mask_ref, st3_5_use_mask_org, color_matcher_ref_type, color_matcher_ref_image)

        
        elif stage_index == 5:
            ebsynth_utility_stage5(dbg, project_args, is_invert_mask,SYNTHS_PER_PROJECT)
        
        elif stage_index == 7:
            ebsynth_utility_stage7(dbg, project_args, blend_rate, export_type, is_invert_mask)
        
        else:
            pass

        return (dbg, info )
