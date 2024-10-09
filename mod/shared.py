import os
import sys

import gradio as gr

from mod.shared import shared_cmd_options, shared_gradio_themes, options, shared_items, sd_models_types
from mod.paths_internal import models_path, script_path, data_path, sd_configs_path, sd_default_config, sd_model_file, default_sd_model_file, extensions_dir, extensions_builtin_dir  # noqa: F401
from mod import util
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mod import shared_state, styles, interrogate, shared_total_tqdm, memmon

def initialize_shared():
    # ... 其他代码 ...
    from mod import util  # 延迟导入 util
    # ... 其他代码 ...

# 将 shared_cmd_options 的导入放入函数内部
def get_shared_cmd_options():
    from mod.shared import shared_cmd_options  # 延迟导入 shared_cmd_options
    return shared_cmd_options

# 其他需要使用 shared_cmd_options 的地方也进行延迟导入
def some_function():
    from mod.shared import shared_cmd_options  # 延迟导入
    # ... 使用 shared_cmd_options 的代码 ...

cmd_opts = get_shared_cmd_options().cmd_opts
parser = get_shared_cmd_options().parser

batch_cond_uncond = True  # old field, unused now in favor of shared.opts.batch_cond_uncond
parallel_processing_allowed = True
styles_filename = cmd_opts.styles_file = cmd_opts.styles_file if len(cmd_opts.styles_file) > 0 else [os.path.join(data_path, 'styles.csv')]
config_filename = cmd_opts.ui_settings_file
hide_dirs = {"visible": not cmd_opts.hide_ui_dir_config}

demo: gr.Blocks = None

device: str = None

weight_load_location: str = None

xformers_available = False

hypernetworks = {}

loaded_hypernetworks = []

state: 'shared_state.State' = None

prompt_styles: 'styles.StyleDatabase' = None

interrogator: 'interrogate.InterrogateModels' = None

face_restorers = []

options_templates: dict = None
opts: options.Options = None
restricted_opts: set[str] = None

sd_model: sd_models_types.WebuiSdModel = None

settings_components: dict = None
"""assigned from ui.py, a mapping on setting names to gradio components responsible for those settings"""

tab_names = []

latent_upscale_default_mode = "Latent"
latent_upscale_modes = {
    "Latent": {"mode": "bilinear", "antialias": False},
    "Latent (antialiased)": {"mode": "bilinear", "antialias": True},
    "Latent (bicubic)": {"mode": "bicubic", "antialias": False},
    "Latent (bicubic antialiased)": {"mode": "bicubic", "antialias": True},
    "Latent (nearest)": {"mode": "nearest", "antialias": False},
    "Latent (nearest-exact)": {"mode": "nearest-exact", "antialias": False},
}

sd_upscalers = []

clip_model = None

progress_print_out = sys.stdout

gradio_theme = gr.themes.Base()

total_tqdm: 'shared_total_tqdm.TotalTQDM' = None

mem_mon: 'memmon.MemUsageMonitor' = None

options_section = options.options_section
OptionInfo = options.OptionInfo
OptionHTML = options.OptionHTML

natural_sort_key = util.natural_sort_key
listfiles = util.listfiles
html_path = util.html_path
html = util.html
walk_files = util.walk_files
ldm_print = util.ldm_print

reload_gradio_theme = shared_gradio_themes.reload_gradio_theme

list_checkpoint_tiles = shared_items.list_checkpoint_tiles
refresh_checkpoints = shared_items.refresh_checkpoints
list_samplers = shared_items.list_samplers
reload_hypernetworks = shared_items.reload_hypernetworks

hf_endpoint = os.getenv('HF_ENDPOINT', 'https://huggingface.co')
