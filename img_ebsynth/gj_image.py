import os
import cv2
import glob
import shutil
import numpy as np
import math
from PIL import Image
from tqdm.auto import tqdm

#---------------------------------
# Copied from PySceneDetect
def mean_pixel_distance(left: np.ndarray, right: np.ndarray) -> float:
    """Return the mean average distance in pixel values between `left` and `right`.
    Both `left and `right` should be 2 dimensional 8-bit images of the same shape.
    """
    assert len(left.shape) == 2 and len(right.shape) == 2
    assert left.shape == right.shape
    num_pixels: float = float(left.shape[0] * left.shape[1])
    return (np.sum(np.abs(left.astype(np.int32) - right.astype(np.int32))) / num_pixels)


def estimated_kernel_size(frame_width: int, frame_height: int) -> int:
    """Estimate kernel size based on video resolution."""
    size: int = 4 + round(math.sqrt(frame_width * frame_height) / 192)
    if size % 2 == 0:
        size += 1
    return size

_kernel = None

def _detect_edges(lum: np.ndarray) -> np.ndarray:
    global _kernel
    """Detect edges using the luma channel of a frame.
    Arguments:
        lum: 2D 8-bit image representing the luma channel of a frame.
    Returns:
        2D 8-bit image of the same size as the input, where pixels with values of 255
        represent edges, and all other pixels are 0.
    """
    # Initialize kernel.
    if _kernel is None:
        kernel_size = estimated_kernel_size(lum.shape[1], lum.shape[0])
        _kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Estimate levels for thresholding.
    sigma: float = 1.0 / 3.0
    median = np.median(lum)
    low = int(max(0, (1.0 - sigma) * median))
    high = int(min(255, (1.0 + sigma) * median))

    # Calculate edges using Canny algorithm, and reduce noise by dilating the edges.
    edges = cv2.Canny(lum, low, high)
    return cv2.dilate(edges, _kernel)

#---------------------------------

def detect_edges(img_path, mask_path, is_invert_mask):
    im = cv2.imread(img_path)
    if mask_path:
        mask = cv2.imread(mask_path)[:, :, 0]
        mask = mask[:, :, np.newaxis]
        im = im * ((mask == 0) if is_invert_mask else (mask > 0))

    hue, sat, lum = cv2.split(cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    return _detect_edges(lum)

def get_mask_path_of_img(img_path, mask_dir):
    img_basename = os.path.basename(img_path)
    mask_path = os.path.join(mask_dir, img_basename)
    return mask_path if os.path.isfile(mask_path) else None

def analyze_key_frames(png_dir, mask_dir, th, min_gap, max_gap, add_last_frame, is_invert_mask):
    keys = []
    
    frames = sorted(glob.glob(os.path.join(png_dir, "[0-9]*.png")))
    
    if not frames:
        raise ValueError(f"No PNG files found in directory: {png_dir}")
    
    key_frame = frames[0]
    keys.append(int(os.path.splitext(os.path.basename(key_frame))[0]))
    key_edges = detect_edges(key_frame, get_mask_path_of_img(key_frame, mask_dir), is_invert_mask)
    gap = 0
    
    for frame in frames:
        gap += 1
        if gap < min_gap:
            continue
        
        edges = detect_edges(frame, get_mask_path_of_img(frame, mask_dir), is_invert_mask)
        
        delta = mean_pixel_distance(edges, key_edges)
        
        _th = th * (max_gap - gap) / max_gap
        
        if _th < delta:
            basename_without_ext = os.path.splitext(os.path.basename(frame))[0]
            keys.append(int(basename_without_ext))
            key_frame = frame
            key_edges = edges
            gap = 0
    
    if add_last_frame:
        basename_without_ext = os.path.splitext(os.path.basename(frames[-1]))[0]
        last_frame = int(basename_without_ext)
        if last_frame not in keys:
            keys.append(last_frame)

    return keys

def remove_pngs_in_dir(path):
    if not os.path.isdir(path):
        return
    
    pngs = glob.glob(os.path.join(path, "*.png"))
    for png in pngs:
        os.remove(png)

def ebsynth_utility_stage2(png_dir, output_dir, min_gap, max_gap, key_th, key_add_last_frame, is_invert_mask):
    remove_pngs_in_dir(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    keys = analyze_key_frames(png_dir, png_dir, key_th, min_gap, max_gap, key_add_last_frame, is_invert_mask)

    for k in keys:
        filename = str(k).zfill(5) + ".png"
        shutil.copy(os.path.join(png_dir, filename), os.path.join(output_dir, filename))

    print(f"Keyframes are output to [{output_dir}]")
    return keys
#---------------------------------

class VideoKeyFramesExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "png_dir": ("STRING", {"default": "", "multiline": False}),
                "output_dir": ("STRING", {"default": "", "multiline": False}),
                "min_gap": ("INT", {"default": 10, "min": 1, "max": 300}),
                "max_gap": ("INT", {"default": 300, "min": 10, "max": 300}),
                "key_th": ("FLOAT", {"default": 0.1, "min": 0, "max": 1, "step": 0.1}),
                "key_add_last_frame": ("BOOLEAN", {"default": True}),
                "is_invert_mask": ("BOOLEAN", {"default": False})
            }
        }

    RETURN_TYPES = ("STRING","INT")
    RETURN_NAMES = ("output_dir","INT")
    FUNCTION = "extract_key_frames"
    CATEGORY = 'IMAGEmake'

    def extract_key_frames(self, png_dir, output_dir, min_gap, max_gap, key_th, key_add_last_frame, is_invert_mask):
        png_dir = os.path.join(png_dir, "video_frame")
        # 拼接 output_dir 为项目路径下的 img2img_key
        output_dir = os.path.join(output_dir, "img2img_key")  # 使用传入的 output_dir
        os.makedirs(output_dir, exist_ok=True)  # 如果不存在则创建
        ebsynth_utility_stage2(png_dir, output_dir, min_gap, max_gap, key_th, key_add_last_frame, is_invert_mask)
        keys = ebsynth_utility_stage2(png_dir, output_dir, min_gap, max_gap, key_th, key_add_last_frame, is_invert_mask)
        return (output_dir,len(keys))

# 示例调用
# extractor = VideoKeyFramesExtractor()
# extractor.extract_key_frames(
#     png_dir="path/to/png_dir",
#     output_dir="path/to/output",
#     min_gap=10,
#     max_gap=300,
#     key_th=0.1,
#     key_add_last_frame=True,
#     is_invert_mask=False
# )
