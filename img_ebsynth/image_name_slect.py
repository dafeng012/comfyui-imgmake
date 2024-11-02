class SelectImageName:
    def __init__(self) -> None:
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "imagelist": ("STRING", {}),
                "selected_image_index": ("INT", {"default": 1, "min": 1, "max": 9900})
            },
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_name",)
    FUNCTION = "select_image_name"
    CATEGORY = "IMAGEmake"



    def select_image_name(self, imagelist,selected_image_index):
        image_list = imagelist.split(",")
        image_name = image_list[selected_image_index]
        return (image_name,)
        

