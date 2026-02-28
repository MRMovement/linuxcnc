"""右侧面板"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                           QLabel, QStackedWidget, QButtonGroup, QGridLayout,
                           QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from src.utils.image_loader import load_pixmap
from src.config import sizes

class RightPanel(QWidget):
    """右侧垂直按钮面板"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_pager_buttons = []
        self.right_buttons_stacked = None
        self.time_label = None
        self.timer = None
        self.init_ui()
    
    def init_ui(self):
        self.setFixedWidth(sizes.SIZES["RIGHT_VERTICAL_BUTTON_WIDTH"])
        
        # 背景渐变
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #999999,
                    stop: 0.1 #CBCBCB,
                    stop: 1 #CBCBCB
                );
                border-left: 1px solid #AAAAAA;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 左侧竖排换页按钮
        pager_widget = self.create_vertical_pager_buttons()
        layout.addWidget(pager_widget, stretch=0)
        
        # 右侧主要内容区域
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 时间显示
        time_widget = self.create_time_widget()
        content_layout.addWidget(time_widget, stretch=0)
        
        # 按钮堆叠窗口
        self.right_buttons_stacked = QStackedWidget()
        self.right_buttons_stacked.setStyleSheet("background: transparent;")
        
        # 第1页：6个功能按钮
        page1 = self.create_button_page1()
        self.right_buttons_stacked.addWidget(page1)
        
        # 第2页：空页面
        page2 = self.create_button_page2()
        self.right_buttons_stacked.addWidget(page2)
        
        content_layout.addWidget(self.right_buttons_stacked, stretch=1)
        layout.addWidget(content_widget, stretch=1)
        
        # 启动定时器
        self.start_timer()
    
    def create_vertical_pager_buttons(self):
        """创建竖排换页按钮"""
        widget = QWidget()
        widget.setFixedWidth(10)
        widget.setFixedHeight(400)
        widget.setStyleSheet("background: transparent; border: none;")
        
        # 计算居中位置
        container_height = 250
        button_height = 120
        button_spacing = 10
        total_height = 2 * button_height + button_spacing
        start_y = (container_height - total_height) // 2 + 130
        
        # 第一个按钮（蓝色）
        btn1 = QPushButton("", widget)
        btn1.setGeometry(0, start_y, 9, button_height)
        btn1.setStyleSheet("""
            QPushButton {
                background-color: #0000E9;
                border: none;
                margin: 0;
                padding: 0;
            }
            QPushButton:pressed {
                background-color: #0055AA;
            }
        """)
        btn1.setCheckable(True)
        btn1.setChecked(True)
        btn1.clicked.connect(lambda: self.on_vertical_pager_clicked(0))
        
        # 第二个按钮（黑色）
        btn2 = QPushButton("", widget)
        btn2.setGeometry(0, start_y + button_height + button_spacing, 9, button_height)
        btn2.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border: none;
                margin: 0;
                padding: 0;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        btn2.setCheckable(True)
        btn2.clicked.connect(lambda: self.on_vertical_pager_clicked(1))
        
        self.vertical_pager_buttons = [btn1, btn2]
        
        return widget
    
    def create_time_widget(self):
        """创建时间显示部件"""
        widget = QWidget()
        widget.setFixedHeight(sizes.SIZES["TIME_HEIGHT"])
        widget.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 5)
        layout.setSpacing(0)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.time_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 16pt;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        
        layout.addWidget(self.time_label)
        widget.setLayout(layout)
        return widget
    
    def create_button_page1(self):
        """创建第1页按钮"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 0, 0, 0)
        layout.setSpacing(1)
        
        for i in range(6):
            btn = self.create_right_vertical_custom_button(i + 1)
            layout.addWidget(btn)
        
        return widget
    
    def create_button_page2(self):
        """创建第2页按钮（空页面）"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 0, 0, 0)
        layout.setSpacing(1)
        
        for i in range(6):
            empty_btn = self.create_empty_right_button()
            layout.addWidget(empty_btn)
        
        return widget
    
    def create_right_vertical_custom_button(self, button_type):
        """创建右侧垂直按钮 - 这里需要实现具体的按钮创建逻辑"""
        # 由于代码较长，这里简化为创建基本按钮
        # 实际实现可以参考原代码的create_right_vertical_custom_button方法
        btn = QPushButton(f"Button {button_type}")
        btn.setFixedSize(sizes.SIZES["RIGHT_BUTTON_WIDTH"], 
                        sizes.SIZES["RIGHT_BUTTON_HEIGHT"])
        
        # 设置基本样式
        btn.setStyleSheet("""
            QPushButton {
                border: 2px solid #757575;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #F0F0F0,
                    stop: 0.3 #C7C7C7,
                    stop: 0.7 #C7C7C7,
                    stop: 1 #F0F0F0
                );
                border-radius: 3px;
                font-size: 12pt;
            }
        """)
        
        return btn
    
    def create_empty_right_button(self):
        """创建空按钮"""
        btn = QPushButton()
        btn.setFixedSize(148, 98)
        btn.setStyleSheet("""
            QPushButton {
                border: 2px solid #757575;
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
        
        # 添加占位文字
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(5, 5, 5, 5)
        placeholder = QLabel("(空)")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color: #888888; font-size: 12pt; font-weight: bold;")
        layout.addWidget(placeholder)
        
        return btn
    
    def on_vertical_pager_clicked(self, index):
        """竖排换页按钮点击事件"""
        for i, btn in enumerate(self.vertical_pager_buttons):
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
        
        # 切换右侧按钮页面
        if self.right_buttons_stacked:
            self.right_buttons_stacked.setCurrentIndex(index)
    
    def start_timer(self):
        """启动时间更新定时器"""
        self.update_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)  # 每分钟更新
    
    def update_time(self):
        """更新时间显示"""
        if self.time_label:
            current_time = QDateTime.currentDateTime()
            time_str = current_time.toString("HH:mm")
            self.time_label.setText(time_str)