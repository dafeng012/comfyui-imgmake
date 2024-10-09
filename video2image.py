import os
import re
import subprocess
from PIL import Image
import torch
from transparent_background import Remover
import cv2
import numpy as np
from tqdm.auto import tqdm
import glob
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, Optional, Callable, TYPE_CHECKING
from torch import Tensor
if TYPE_CHECKING:
    from mypy.typeshed.stdlib._typeshed import SupportsDunderGT, SupportsDunderLT

class Video2Frames:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": "", "multiline": False}),
                "project_path": ("STRING", {"default": "", "multiline": False}),
                "device": (["cuda:0", "cpu"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("project_path",)
    FUNCTION = "extract_video_frames"
    CATEGORY = 'IMAGEmake'

    def extract_video_frames(self, video_path, project_path, device):
        frame_path = os.path.join(project_path, "video_frame")

        if not os.path.exists(frame_path):
            os.makedirs(frame_path)

        # 使用ffmpeg提取视频帧
        png_path = os.path.join(frame_path, "%05d.png")
        subprocess.call(f"ffmpeg -ss 00:00:00 -y -i \"{video_path}\" -qscale 0 -f image2 -c:v png \"{png_path}\"", shell=True)

        return (project_path,)
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
def tensor2rgba(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t.unsqueeze(3).repeat(1, 1, 1, 4)
    elif size[3] == 1:
        return t.repeat(1, 1, 1, 4)
    elif size[3] == 3:
        alpha_tensor = torch.ones((size[0], size[1], size[2], 1))
        return torch.cat((t, alpha_tensor), dim=3)
    else:
        return t

class LoadImageListPlus:

    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "folder_path": ("STRING", {}),
                "file_filter": ("STRING", {"default": "*.png"}),
                "sort_method": (["numerical", "alphabetical"], {"default": "numerical"}),
            },
        }

    RELOAD_INST = True
    RETURN_TYPES = ("IMAGE","STRING")
    RETURN_NAMES = ("images","image_list")
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (True,False)
    FUNCTION = "load_images"

    CATEGORY = "IMAGEmake"

    @staticmethod
    def numerical_sort(file_name: Path) -> int:
        subbed = re.sub("\D", "", str(file_name))
        if subbed == "":
            return 0
        return int(subbed)
    
    
    @staticmethod
    def alphabetical_sort(file_name: Path) -> str:
        return str(file_name)

    def load_images(
        self, folder_path: str, file_filter: str, sort_method: str
    ) -> Tuple[List[Tensor]]:
        folder = Path(folder_path)
    
        if not folder.is_dir():
            raise Exception(f"Folder path {folder_path} does not exist.")

        sort_method_impl: Callable[[str], Union[SupportsDunderGT, SupportsDunderLT]]
        if sort_method == "numerical":
            sort_method_impl = self.numerical_sort
        elif sort_method == "alphabetical":
            sort_method_impl = self.alphabetical_sort
        else:
            raise ValueError(f"Unknown sort method {sort_method}")

        files = sorted(folder.glob(file_filter), key=sort_method_impl)
        images = [pil2tensor(Image.open(file)) for file in files]
        image_list = [file for file in os.listdir(folder_path)]
        output_string = ', '.join(image_list)
        print(output_string)
      
        return (images,output_string,)
