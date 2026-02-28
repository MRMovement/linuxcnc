"""滑块组件"""
from PyQt5.QtWidgets import QWidget
from src.config import colors

class SliderWidget(QWidget):
    """自定义滑块控件"""
    def __init__(self, width=400, height=20, 
                 active_color=colors.COLORS["SLIDER_ACTIVE"],
                 inactive_color=colors.COLORS["SLIDER_INACTIVE"],
                 progress=0.66, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.progress = progress
        self.init_ui()
    
    def init_ui(self):
        self.setFixedSize(self.width, self.height)
        
        # 外层容器
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.inactive_color};
                border: 2px solid #c0c0c0;  
                border-radius: 2px;  
            }}
        """)
        
        # 进度条
        border_width = 3
        inner_width = self.width - border_width * 2
        inner_height = self.height - border_width * 2
        inner_progress_width = int(inner_width * self.progress)
        
        self.progress_widget = QWidget(self)
        self.progress_widget.setGeometry(border_width, border_width, 
                                        inner_progress_width, 
                                        inner_height)
        self.progress_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {self.active_color};
                border: none;
                border-radius: 3px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
        """)
    
    def set_progress(self, progress):
        """设置进度"""
        self.progress = max(0, min(1, progress))
        border_width = 3
        inner_width = self.width - border_width * 2
        inner_height = self.height - border_width * 2
        inner_progress_width = int(inner_width * self.progress)
        
        self.progress_widget.setGeometry(border_width, border_width, 
                                        inner_progress_width, 
                                        inner_height)