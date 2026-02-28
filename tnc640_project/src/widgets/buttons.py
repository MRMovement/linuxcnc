"""自定义按钮组件"""
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from src.utils.image_loader import load_pixmap, load_icon
from src.utils.style_helper import create_button_style
from src.config import colors, sizes

class SpecialButton(QPushButton):
    """特殊格式按钮"""
    def __init__(self, button_type, parent=None):
        super().__init__(parent)
        self.button_type = button_type
        self.init_ui()
    
    def init_ui(self):
        if self.button_type == 2:  # "T 5" + Z标签
            self.create_type2_button()
        else:
            self.create_default_button()
    
    def create_type2_button(self):
        container = QWidget()
        container.setFixedSize(sizes.SIZES["MEDIUM_BUTTON_WIDTH"], 
                             sizes.SIZES["MEDIUM_BUTTON_HEIGHT"])
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)
        
        t_label = QLabel("T   5")
        t_label.setStyleSheet("""
            QLabel {
                font-size: 17pt;
                font-weight: bold;
                color: #0505ff;
                background-color: transparent;
                border: none;
                margin: 0;
                padding: 0;
            }
        """)
        
        z_label = QLabel("Z")
        z_label.setStyleSheet("""
            QLabel {
                background-color: #0000FF;
                color: #FFFFFF;
                font-size: 17pt;
                font-weight: bold;
                padding: 2px 6px;
                border-radius: 3px;
                margin: 0px;
            }
        """)
        z_label.setFixedWidth(25)
        z_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(t_label)
        layout.addStretch()
        layout.addWidget(z_label)
        
        container.setStyleSheet("""
            QWidget {
                border: 1px solid #969696;
                border-radius: 10px;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #FDFDFD,
                    stop: 0.5 #EEEEEE,
                    stop: 1 #DDDDDD
                );
            }
        """)
        
        self.setFixedSize(sizes.SIZES["MEDIUM_BUTTON_WIDTH"], 
                         sizes.SIZES["MEDIUM_BUTTON_HEIGHT"])
        self.setStyleSheet("border: none; background: transparent;")
        
        # 将容器添加到按钮
        btn_layout = QHBoxLayout(self)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(container)
    
    def create_default_button(self):
        self.setFixedSize(sizes.SIZES["MEDIUM_BUTTON_WIDTH"], 
                         sizes.SIZES["MEDIUM_BUTTON_HEIGHT"])
        
        if self.button_type == 1:
            icon = load_icon("坐标.png", 25)
            if not icon.isNull():
                self.setIcon(icon)
                self.setIconSize(QSize(25, 25))
                self.setText(" 0")
            else:
                self.setText("📊 0")
            
            text_style = "text-align: left; padding-left: 10px;"
            color = "#0000D9"
        elif self.button_type == 3:
            self.setText("S  0")
            text_style = "text-align: left; padding-left: 5px;"
            color = "#0000D9"
        elif self.button_type == 4:
            self.setText("F  0mm/min")
            text_style = "text-align: left; padding-left: 5px;"
            color = "#0000D9"
        elif self.button_type == 5:
            self.setText("Over  100%")
            text_style = "text-align: left; padding-left: 5px;"
            color = "#0000D9"
        elif self.button_type == 6:
            self.setText("M  5/9")
            text_style = "text-align: left; padding-left: 5px;"
            color = "#0000D9"
        else:
            text_style = "text-align: left; padding-left: 5px;"
            color = "#0000D9"
        
        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid #969696;
                border-radius: 10px;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #FDFDFD,
                    stop: 0.5 #EEEEEE,
                    stop: 1 #DDDDDD
                );
                font-size: 17pt;
                font-weight: bold;
                color: {color};
                {text_style}
            }}
            QPushButton:pressed {{
                border: 1px solid #868686;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #EDEDED,
                    stop: 0.5 #DEDEDE,
                    stop: 1 #CDCDCD
                );
            }}
        """)