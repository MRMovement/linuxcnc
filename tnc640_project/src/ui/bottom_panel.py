"""底部面板"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QStackedWidget)
from PyQt5.QtCore import Qt
from src.utils.text_utils import create_html_button_text
from src.config import sizes

class BottomPanel(QWidget):
    """底部面板（分页按钮 + 功能按钮）"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pager_buttons = []
        self.bottom_stacked_widget = None
        self.init_ui()
    
    def init_ui(self):
        # 背景渐变
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #999999,
                    stop: 1 #CBCBCB
                );
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 分页按钮
        pager_widget = self.create_pager_buttons()
        layout.addWidget(pager_widget, stretch=0)
        
        # 功能按钮
        bottom_buttons = self.create_bottom_buttons()
        layout.addWidget(bottom_buttons, stretch=0)
    
    def create_pager_buttons(self):
        """创建分页按钮"""
        widget = QWidget()
        widget.setFixedHeight(12)
        widget.setStyleSheet("""
            QWidget {
                background-color: #CBCBCB;
                border-top: 1px solid #AAAAAA;
            }
        """)
        
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        
        # 4个分页按钮
        self.pager_buttons = []
        
        for i in range(4):
            btn = QPushButton("")
            btn.setFixedSize(sizes.SIZES["PAGER_BUTTON_WIDTH"], 
                           sizes.SIZES["PAGER_BUTTON_HEIGHT"])
            btn.setCheckable(True)
            
            if i == 0:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #003cff;
                        border: 1px solid #004488;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                """)
                btn.setChecked(True)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #000000;
                        border: 1px solid #333333;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                """)
            
            btn.clicked.connect(lambda checked, idx=i: self.on_pager_button_clicked(idx))
            container_layout.addWidget(btn)
            self.pager_buttons.append(btn)
        
        container.setLayout(container_layout)
        
        # 主布局，居中显示
        main_layout = QHBoxLayout(widget)
        main_layout.setContentsMargins(0, 2, 0, 2)
        main_layout.addStretch()
        main_layout.addWidget(container)
        main_layout.addStretch()
        
        return widget
    
    def create_bottom_buttons(self):
        """创建底部功能按钮"""
        widget = QWidget()
        widget.setFixedHeight(110)
        widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #999999,
                    stop: 1 #CBCBCB
                );
            }
        """)
        
        self.bottom_stacked_widget = QStackedWidget()
        
        # 第1页
        page1 = self.create_button_page1()
        self.bottom_stacked_widget.addWidget(page1)
        
        # 第2-4页（空页面）
        for page_num in range(2, 5):
            page = self.create_empty_button_page()
            self.bottom_stacked_widget.addWidget(page)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.bottom_stacked_widget)
        
        return widget
    
    def create_button_page1(self):
        """创建第1页按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        buttons_config = [
            {"text": "M", "icon": None},
            {"text": "S", "icon": None},
            {"text": "F", "icon": None},
            {"text": "探测功能", "icon": "探测功能.png"},
            {"text": "原点管理", "icon": "原点管理.png"},
            {"text": "", "icon": None},
            {"text": "3D-ROT", "icon": "3D-ROT.png"},
            {"text": "刀具表", "icon": "刀具表.png"}
        ]
        
        for config in buttons_config:
            btn = self.create_bottom_button(config["text"], config["icon"])
            layout.addWidget(btn)
        
        return widget
    
    def create_empty_button_page(self):
        """创建空按钮页面"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        for i in range(8):
            btn = self.create_bottom_button("")
            layout.addWidget(btn)
        
        return widget
    
    def create_bottom_button(self, text, icon_filename=None):
        """创建单个底部按钮"""
        label = QLabel()
        label.setFixedSize(sizes.SIZES["BOTTOM_BUTTON_WIDTH"], 
                          sizes.SIZES["BOTTOM_BUTTON_HEIGHT"])
        label.setAlignment(Qt.AlignCenter)
        label.setCursor(Qt.PointingHandCursor)
        
        html_content = create_html_button_text(text, icon_filename)
        if html_content:
            label.setText(html_content)
        
        label.setStyleSheet("""
            QLabel {
                border: 2px solid #757575;
                padding: 1px;
                background-color: #F7F7F7;
                margin: 0;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #F0F0F0,
                    stop: 0.3 #C7C7C7,
                    stop: 0.7 #C7C7C7,
                    stop: 1 #F0F0F0
                );
                border-radius: 3px;
            }
        """)
        
        return label
    
    def on_pager_button_clicked(self, index):
        """分页按钮点击事件"""
        for i, btn in enumerate(self.pager_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0000E9;
                        border: 1px solid #004488;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                """)
                btn.setChecked(True)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #000000;
                        border: 1px solid #333333;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                """)
                btn.setChecked(False)
        
        # 切换底部按钮页面
        if self.bottom_stacked_widget:
            self.bottom_stacked_widget.setCurrentIndex(index)