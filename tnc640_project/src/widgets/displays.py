"""显示组件"""
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from src.config import sizes

class DisplayItem(QFrame):
    """坐标显示项"""
    def __init__(self, label, value, item_id, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        self.label = label
        self.value = value
        self.selected = False
        self.init_ui()
    
    def init_ui(self):
        self.setFixedSize(sizes.SIZES["DISPLAY_ITEM_WIDTH"], 
                         sizes.SIZES["DISPLAY_ITEM_HEIGHT"])
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #757575;
                border-radius: 4px;
                background-color: #F7F7F7;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标签部分
        self.label_widget = QLabel(self.label)
        self.label_widget.setFixedWidth(70)
        self.label_widget.setStyleSheet("""
            QLabel {
                background-color: #0000ED;
                color: #ffffff;
                font-size: 35pt;
                font-weight: bold;
                border-right: 1px solid #555555;
                padding: 0px;
                text-align: center;
            }
        """)
        
        # 数值部分
        self.value_widget = QLabel(self.value)
        self.value_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # 存储样式
        self.normal_style = """
            QLabel {
                color: #0000ff;
                font-size: 45pt;
                font-weight: bold;
                padding-left: 20px;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #FFFFFF,
                    stop: 0.7 #DEDEDE,
                    stop: 1 #DEDEDE
                );
                border-top-right-radius: 1px;
                border-bottom-right-radius: 1px;
            }
        """
        
        self.selected_style = """
            QLabel {
                color: #FFFFFF;
                font-size: 45pt;
                font-weight: bold;
                padding-left: 20px;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #A0C0FF,
                    stop: 0.3 #83a3e3,
                    stop: 1 #83a3e3
                );
                border-top-right-radius: 1px;
                border-bottom-right-radius: 1px;
            }
        """
        
        self.value_widget.setStyleSheet(self.normal_style)
        
        layout.addWidget(self.label_widget)
        layout.addWidget(self.value_widget)
    
    def select(self):
        """选中状态"""
        self.selected = True
        self.value_widget.setStyleSheet(self.selected_style)
    
    def deselect(self):
        """取消选中"""
        self.selected = False
        self.value_widget.setStyleSheet(self.normal_style)