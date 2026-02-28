"""路径配置"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

def get_image_path(filename):
    """获取图片完整路径"""
    return os.path.join(IMAGE_DIR, filename)