import base64
import os
import time
from typing import Optional

import cv2


class ImageHandler:
    def __init__(self, save_img_path):
        self.images = [] # stores img_url paths
        self.save_img_path = save_img_path

    def save_img(self, cv2img):
        i = len(self.images)
        new_img_path = os.path.join(self.save_img_path, f'img_{i}.jpg')

        self.images.append(new_img_path)
        cv2.imwrite(new_img_path, cv2img)

        time.sleep(0.1)

    def get_last_n_img(self, n=1) -> list:
        return self.images[-n:]

    @staticmethod
    def encode_image_to_base64(image_path: str) -> Optional[str]:
        """Encodes an image file to a base64 string."""
        if not os.path.exists(image_path):
            print(f"Error: Image path not found: {image_path}")
            return None
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image {image_path}: {e}")
            return None
