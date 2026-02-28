"""样式助手"""
from src.config.colors import COLORS

def create_button_style(border_color=COLORS["BUTTON_BORDER"], 
                       pressed=False):
    """创建按钮通用样式"""
    if pressed:
        border = f"border: 2px solid #555555;"
        gradient_start = "#E0E0E0"
        gradient_mid = "#B7B7B7"
    else:
        border = f"border: 2px solid {border_color};"
        gradient_start = COLORS["BUTTON_GRADIENT_TOP"]
        gradient_mid = COLORS["BUTTON_GRADIENT_MID"]
    
    return f"""
        QPushButton {{
            {border}
            padding: 1px;
            background-color: #F7F7F7;
            margin: 0;
            background: qlineargradient(
                x1: 0.5, y1: 0,
                x2: 0.5, y2: 1,
                stop: 0 {gradient_start},
                stop: 0.3 {gradient_mid},
                stop: 0.7 {gradient_mid},
                stop: 1 #F0F0F0
            );
            border-radius: 3px;
        }}
    """