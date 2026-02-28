"""手动操作页面"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QFrame, QPushButton, QTextEdit)
from PyQt5.QtCore import Qt
from src.widgets.displays import DisplayItem
from src.widgets.sliders import SliderWidget
from src.utils.image_loader import load_pixmap
from src.config import colors

class ManualPage(QWidget):
    """手动操作页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_items = {}
        self.selected_display_item = None
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. 灰色背景区域
        gray_background = self.create_gray_background()
        main_layout.addWidget(gray_background)
        
        # 2. 位置显示框
        title_frame = self.create_title_frame()
        main_layout.addWidget(title_frame)
        
        # 3. 坐标显示区域
        coord_container = self.create_coordinate_display()
        main_layout.addWidget(coord_container)
        
        # 4. 小按钮区域
        small_btn_container = self.create_small_button_area()
        main_layout.addWidget(small_btn_container)
        
        # 5. 特殊按钮区域
        medium_btn_container = self.create_medium_button_area()
        main_layout.addWidget(medium_btn_container)
        
        # 6. 滑块区域
        slider_container = self.create_slider_area()
        main_layout.addWidget(slider_container)
    
    def create_gray_background(self):
        """创建灰色背景区域"""
        widget = QWidget()
        widget.setFixedHeight(105)
        widget.setStyleSheet(f"background-color: {colors.COLORS['LIGHT_GRAY']};")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        return widget
    
    def create_title_frame(self):
        """创建标题框"""
        frame = QFrame()
        frame.setFixedHeight(40)
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #FCFCFC,
                    stop: 1 #E2E2E2
                );
                border-top: 2px solid #999999;
            }
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 20, 5)
        
        title_text = QLabel("位置显示 <span style='color: #0000E9;'>模式：命令值</span>")
        title_text.setTextFormat(Qt.RichText)
        title_text.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 16pt;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        
        layout.addWidget(title_text)
        layout.addStretch()
        
        return frame
    
    def create_coordinate_display(self):
        """创建坐标显示区域"""
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {colors.COLORS['WHITE']};")
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 10, 40, 10)
        layout.setSpacing(30)
        
        # 左侧坐标列
        left_coord_widget = QWidget()
        left_coord_layout = QVBoxLayout(left_coord_widget)
        left_coord_layout.setSpacing(5)
        
        # 创建坐标显示项
        coord_items = [
            ("X", "+0.000"),
            ("Y", "+0.000"),
            ("Z", "+428.000"),
            ("A", "+0.000"),
        ]
        
        for idx, (label, value) in enumerate(coord_items):
            item = DisplayItem(label, value, f"coord_{idx}")
            item.mousePressEvent = lambda e, w=item: self.handle_display_click(w)
            left_coord_layout.addWidget(item)
            self.display_items[f"coord_{idx}"] = item
        
        layout.addWidget(left_coord_widget)
        
        # 右侧状态列
        right_status_widget = QWidget()
        right_status_layout = QVBoxLayout(right_status_widget)
        right_status_layout.setContentsMargins(0, 10, 0, 0)
        right_status_layout.setSpacing(5)
        
        status_items = [
            ("C", "+0.000"),
            ("S1", "+0.000"),
        ]
        
        for idx, (label, value) in enumerate(status_items, start=len(coord_items)):
            item = DisplayItem(label, value, f"status_{idx}")
            item.mousePressEvent = lambda e, w=item: self.handle_display_click(w)
            right_status_layout.addWidget(item)
            self.display_items[f"status_{idx}"] = item
        
        right_status_layout.addStretch()
        layout.addWidget(right_status_widget)
        layout.addStretch()
        
        return widget
    
    def create_small_button_area(self):
        """创建小按钮区域"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 40, 10)
        layout.setSpacing(8)
        
        # 两个38x38图片按钮
        image_files = ["38按钮1.png", "38按钮2.png"]
        
        for image_file in image_files:
            btn = self.create_small_image_button(image_file)
            layout.addWidget(btn)
        
        layout.addStretch()
        return widget
    
    def create_small_image_button(self, image_file):
        """创建小图片按钮"""
        btn = QPushButton()
        btn.setFixedSize(38, 38)
        
        pixmap = load_pixmap(image_file)
        if pixmap:
            # 设置按钮样式
            css_path = image_file.replace('\\', '/')
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid #DDDDDD;
                    border-image: url("{css_path}") 0 0 0 0 stretch stretch;
                    background-color: rgba(229, 229, 229, 0.3);
                    padding: 0px;
                    border-radius: 2px;
                }}
                QPushButton:pressed {{
                    border: 1px solid #BBBBBB;
                    background-color: rgba(213, 213, 213, 0.7);
                }}
            """)
        else:
            btn.setText("Btn")
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #DDDDDD;
                    background: qlineargradient(
                        x1: 0.5, y1: 0,
                        x2: 0.5, y2: 1,
                        stop: 0 #E5E5E5,
                        stop: 0.5 #C7C7C7,
                        stop: 1 #E5E5E5
                    );
                    color: #000000;
                    font-size: 9pt;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    border: 1px solid #BBBBBB;
                    background: qlineargradient(
                        x1: 0.5, y1: 0,
                        x2: 0.5, y2: 1,
                        stop: 0 #D5D5D5,
                        stop: 0.5 #B7B7B7,
                        stop: 1 #D5D5D5
                    );
                }
            """)
        
        return btn
    
    def create_medium_button_area(self):
        """创建中等按钮区域"""
        from src.widgets.buttons import SpecialButton
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 5, 40, 5)
        layout.setSpacing(0)
        
        layout.addStretch()
        
        # 创建6个特殊按钮
        button_types = [1, 2, 3, 4, 5, 6]
        
        for btn_type in button_types:
            if btn_type == 2:
                btn = SpecialButton(btn_type)
            else:
                btn = SpecialButton(btn_type)
            
            layout.addWidget(btn)
            layout.addStretch()
        
        return widget
    
    def create_slider_area(self):
        """创建滑块区域"""
        widget = QWidget()
        widget.setFixedHeight(100)
        widget.setStyleSheet(f"background-color: {colors.COLORS['LIGHT_GRAY']};")
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 5, 40, 0)
        layout.setSpacing(0)
        
        # 第一个滑块行
        slider_row1 = self.create_slider_row(
            slider_width=400,
            label_text="100%&nbsp;&nbsp;&nbsp;&nbsp;S-OVR"
        )
        layout.addWidget(slider_row1)
        
        # 第二个滑块行
        slider_row2 = self.create_slider_row(
            slider_width=400,
            label_text="100%&nbsp;&nbsp;&nbsp;&nbsp;F-OVR&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;S1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: #1589fd;'>LIMIT&nbsp;&nbsp;&nbsp;&nbsp;1</span>"
        )
        layout.addWidget(slider_row2)
        
        return widget
    
    def create_slider_row(self, slider_width, label_text):
        """创建滑块行"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 滑块
        slider = SliderWidget(width=slider_width, height=20)
        layout.addWidget(slider)
        
        # 文字标签
        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setText(label_text)
        label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 22pt;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(label)
        layout.addStretch()
        
        return widget
    
    def handle_display_click(self, widget):
        """处理显示项点击"""
        if self.selected_display_item:
            self.selected_display_item.deselect()
        
        widget.select()
        self.selected_display_item = widget