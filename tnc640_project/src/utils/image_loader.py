"""图片加载工具"""
import os
import base64
from PyQt5.QtGui import QPixmap, QIcon
from src.config.paths import get_image_path

def load_pixmap(filename, width=None, height=None):
    """加载并缩放图片"""
    image_path = get_image_path(filename)
    
    if not os.path.exists(image_path):
        return None
    
    pixmap = QPixmap(image_path)
    if width and height:
        pixmap = pixmap.scaled(width, height, 
                               Qt.KeepAspectRatio, 
                               Qt.SmoothTransformation)
    return pixmap

def load_icon(filename, size=25):
    """加载图标"""
    pixmap = load_pixmap(filename, size, size)
    if pixmap:
        return QIcon(pixmap)
    return QIcon()

def image_to_base64(filename):
    """将图片转换为base64编码"""
    image_path = get_image_path(filename)
    
    if not os.path.exists(image_path):
        return None
    
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('ascii')
    except:
        return None