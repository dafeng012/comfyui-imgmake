import os
from comfy.cli_args import args
import re
from PIL import Image, ExifTags
from PIL.PngImagePlugin import PngInfo
import json
from transparent_background import Remover
import cv2
import numpy as np
from tqdm.auto import tqdm
import glob
import folder_paths
# device = "cuda:0"  # 或者使用 "cpu"
class image2mask:
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required":{
            "input_dir":("STRING", {"default": "", "multiline": False}),
            "output_dir":("STRING", {"default": "", "multiline": False}),
            "tb_use_fast_mode":("BOOLEAN", {"default": True}),
            "tb_use_jit":("BOOLEAN", {"default": True}),
            "st1_mask_threshold":("FLOAT", {"default": 0, "max": 0.5, "step": 0.1}),
            "device":(["cuda:0", "cpu"],),
            
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_dir",)
    FUNCTION = "create_mask_transparent_background"
    CATEGORY = 'IMAGEmake'



    def create_mask_transparent_background(self,input_dir, output_dir, tb_use_fast_mode, tb_use_jit, st1_mask_threshold,device):
        input_dir = os.path.join(input_dir, "video_frame")
        output_dir = os.path.join(output_dir, "video_mask")
        os.makedirs(output_dir, exist_ok=True)  # 如果不存在则创建
        remover = Remover(fast=tb_use_fast_mode, jit=tb_use_jit, device=device)

        original_imgs = glob.glob( os.path.join(input_dir, "*.png") )

        pbar_original_imgs = tqdm(original_imgs, bar_format='{desc:<15}{percentage:3.0f}%|{bar:50}{r_bar}')
        for m in pbar_original_imgs:
            base_name = os.path.basename(m)
            pbar_original_imgs.set_description('{}'.format(base_name))
            img = Image.open(m).convert('RGB')
            out = remover.process(img, type='map')
            if isinstance(out,Image.Image):
                out = np.array(out)
            out[out < int( 255 * st1_mask_threshold )] = 0
            cv2.imwrite(os.path.join(output_dir, base_name), out)
        return (output_dir,)
# create_mask_transparent_background(input_dir="C:\\Users\\56381\\Desktop\\fdg\\img2img_key", output_dir="C:\\Users\\56381\\Desktop\\fdg\\fgfggfg", tb_use_fast_mode=True, tb_use_jit=True, st1_mask_threshold=0.5)
class SaveImage_lp:
    def __init__(self):
        pass


    FILE_TYPE_PNG = "PNG"
    FILE_TYPE_JPEG = "JPEG"
    FILE_TYPE_WEBP_LOSSLESS = "WEBP (lossless)"
    FILE_TYPE_WEBP_LOSSY = "WEBP (lossy)"
    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "IMAGEmake"


    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "output_dir": ("STRING", {"default": "", "multiline": False}),
                "images": ("IMAGE", ),
                "filename": ("STRING", {"default": "ComfyUI"}),
                "file_type": ([s.FILE_TYPE_PNG, s.FILE_TYPE_JPEG, s.FILE_TYPE_WEBP_LOSSLESS, s.FILE_TYPE_WEBP_LOSSY], ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }



    def save_images(self, images, filename_prefix="ComfyUI", file_type=FILE_TYPE_PNG, prompt=None, extra_pnginfo=None,output_dir="",filename=""):
        
        
        extension = {
            self.FILE_TYPE_PNG: "png",
            self.FILE_TYPE_JPEG: "jpg",
            self.FILE_TYPE_WEBP_LOSSLESS: "webp",
            self.FILE_TYPE_WEBP_LOSSY: "webp",
        }.get(file_type, "png")

        results = []
        for image in images:
            array = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            kwargs = dict()
            if extension == "png":
                kwargs["compress_level"] = 4
                if not args.disable_metadata:
                    metadata = PngInfo()
                    if prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None:
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))
                    kwargs["pnginfo"] = metadata
            else:
                if file_type == self.FILE_TYPE_WEBP_LOSSLESS:
                    kwargs["lossless"] = True
                else:
                    kwargs["quality"] = 90
                if not args.disable_metadata:
                    metadata = {}
                    if prompt is not None:
                        metadata["prompt"] = prompt
                    if extra_pnginfo is not None:
                        metadata.update(extra_pnginfo)
                    exif = img.getexif()
                    exif[ExifTags.Base.UserComment] = json.dumps(metadata)
                    kwargs["exif"] = exif.tobytes()


            numeric_filename = f"{int(filename):05d}"
            file = f"{numeric_filename}.{extension}"
            img.save(os.path.join(output_dir, file), **kwargs)
            results.append({
                "filename": file,
                "type": "output",
            })
            

        return { "ui": { "images": results } }

