# tnc640_dynamic_ratio.py
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TNC640DynamicRatioUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_top_tab = 0  # 0=手动操作, 1=编程
        self.selected_display_item = None  # 当前选中的显示项
        self.display_items = {}  # 存储所有显示项
        self.initUI()
    
    def initUI(self):
        # 设置窗口为 1030x800
        self.setWindowTitle("TNC640 数控系统")
        self.setGeometry(100, 100, 1325, 1000)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 垂直布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === 中间主内容区域（包含顶部标签、中间内容和右侧按钮）===
        middle_area = self.create_middle_area()
        main_layout.addWidget(middle_area, stretch=1)
        
        # === 底部区域（分页按钮 + 功能按钮）独立占据完整宽度 ===
        bottom_area = self.create_bottom_area()
        main_layout.addWidget(bottom_area, stretch=0)
        
        central_widget.setLayout(main_layout)
        
        # 应用白色背景
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
        """)
    
    def create_middle_area(self):
        """创建中间主内容区域（包含顶部标签、中间内容和右侧按钮）"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # === 左侧主内容区域 ===
        left_main_widget = self.create_left_main_content()
        layout.addWidget(left_main_widget, stretch=1)
        
        # === 右侧垂直按钮区域（宽度150px）===
        right_buttons_widget = self.create_right_vertical_buttons()
        layout.addWidget(right_buttons_widget, stretch=0)
        
        widget.setLayout(layout)
        return widget
    
    def create_left_main_content(self):
        """创建左侧主内容区域（包含顶部标签和中间内容）"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # === 顶部标签区域 ===
        self.top_tabs_widget = self.create_top_tabs()  # 保存为实例变量
        
        # 调整顶部标签区域的高度比例，让它占据更多空间
        layout.addWidget(self.top_tabs_widget, stretch=5)  # 增加拉伸系数
        
        # === 中间内容区域 ===
        self.right_content = self.create_right_content()
        layout.addWidget(self.right_content, stretch=36)  # 减少中间内容的拉伸系数
        
        widget.setLayout(layout)
        return widget
    
    def create_top_tabs(self):
        """创建顶部标签块（手动操作+编程）- 按钮顶格显示"""
        widget = QWidget()
        
        # 设置整个顶部标签部件的背景颜色为手动操作选中时的颜色，并添加5px圆角
        widget.setStyleSheet("""
            QWidget {
                background-color: #DDDDDD;  /* 手动操作选中时的背景颜色，填充空白区域 */
                border-radius: 5px;  /* 四周5px圆角 */
            }
        """)
        
        # 使用垂直布局，但移除弹性空间让按钮顶格
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 0, 5, 5)  # 上边距设为0，让按钮顶格
        main_layout.setSpacing(0)
        
        # 标签按钮容器
        tab_container = QWidget()
        tab_container.setStyleSheet("""
            QWidget {
                background-color: transparent;  /* 透明背景 */
            }
        """)
        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        # === 中间标签区域 ===
        center_widget = QWidget()
        center_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;  /* 透明背景 */
            }
        """)
        self.center_layout = QHBoxLayout()
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)
        
        # 手动操作块 - 可点击（添加圆角边框）
        self.manual_tab_btn = QPushButton()
        self.manual_tab_btn.setCheckable(True)
        self.manual_tab_btn.setChecked(True)  # 默认选中
        
        # 增加按钮高度，占满更多垂直空间
        self.manual_tab_btn.setMinimumHeight(75)  # 增加高度，让按钮更大
        
        # 创建按钮布局，包含图标和文字
        manual_btn_widget = QWidget()
        manual_btn_layout = QHBoxLayout(manual_btn_widget)
        manual_btn_layout.setContentsMargins(5, 0, 0, 0)  # 左边距40px
        manual_btn_layout.setSpacing(10)  # 图标和文字间距
        
        # 添加图标
        manual_icon_path = os.path.join(os.path.dirname(__file__), "手动操作.png")
        if os.path.exists(manual_icon_path):
            manual_icon_label = QLabel()
            manual_icon_pixmap = QPixmap(manual_icon_path)
            # 缩放图标到合适大小，例如30x30
            scaled_pixmap = manual_icon_pixmap.scaled(47, 47, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            manual_icon_label.setPixmap(scaled_pixmap)
        else:
            # 如果图片不存在，使用占位符
            manual_icon_label = QLabel("📝")
            manual_icon_label.setStyleSheet("font-size: 20pt;")
        
        # 添加文字
        manual_text_label = QLabel("手动操作")
        manual_text_label.setStyleSheet("""
            QLabel {
                color: #0000E9;
                font-size: 20pt;
                font-weight: 200;
                background-color: transparent;
            }
        """)
        
        manual_btn_layout.addWidget(manual_icon_label)
        manual_btn_layout.addWidget(manual_text_label)
        manual_btn_layout.addStretch()  # 添加弹性空间，让内容靠左
        
        # 将自定义widget设置为按钮的布局
        self.manual_tab_btn.setLayout(manual_btn_layout)
        
        self.manual_tab_btn.setStyleSheet("""
            QPushButton {
                color: #0000E9;  /* 选中状态蓝色字体 */
                font-size: 20pt;
                font-weight: 200;
                text-align: left;
                border: none;
                margin: 0;
                background-color: #DDDDDD;  /* 手动操作选中时的背景颜色 */
                border-top-left-radius: 5px;  /* 左上角圆角 */
                border-top-right-radius: 0px;  /* 右上角直角（与编程按钮相邻） */
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QPushButton:pressed {
                background-color: #CCCCCC;
            }
        """)
        self.manual_tab_btn.clicked.connect(lambda: self.switch_top_tab(0))
        
        # 编程块 - 可点击（添加圆角边框）
        self.program_tab_btn = QPushButton()
        self.program_tab_btn.setCheckable(True)
        
        # 增加按钮高度，占满更多垂直空间
        self.program_tab_btn.setMinimumHeight(75)  # 增加高度，让按钮更大
        
        # 创建按钮布局，包含图标和文字
        program_btn_widget = QWidget()
        program_btn_layout = QHBoxLayout(program_btn_widget)
        program_btn_layout.setContentsMargins(5, 0, 0, 0)  # 左边距40px
        program_btn_layout.setSpacing(10)  # 图标和文字间距
        
        # 添加图标
        program_icon_path = os.path.join(os.path.dirname(__file__), "编程.png")
        if os.path.exists(program_icon_path):
            program_icon_label = QLabel()
            program_icon_pixmap = QPixmap(program_icon_path)
            # 缩放图标到合适大小，例如30x30
            scaled_pixmap = program_icon_pixmap.scaled(47, 47, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            program_icon_label.setPixmap(scaled_pixmap)
        else:
            # 如果图片不存在，使用占位符
            program_icon_label = QLabel("📄")
            program_icon_label.setStyleSheet("font-size: 20pt;")
        
        # 添加文字
        program_text_label = QLabel("编程")
        program_text_label.setStyleSheet("""
            QLabel {
                color: #000000;  /* 未选中状态黑色字体 */
                font-size: 20pt;
                font-weight: 200;
                background-color: transparent;
            }
        """)
        
        program_btn_layout.addWidget(program_icon_label)
        program_btn_layout.addWidget(program_text_label)
        program_btn_layout.addStretch()  # 添加弹性空间，让内容靠左
        
        # 将自定义widget设置为按钮的布局
        self.program_tab_btn.setLayout(program_btn_layout)
        
        self.program_tab_btn.setStyleSheet("""
            QPushButton {
                color: #000000;  /* 未选中黑色字体 */
                font-size: 20pt;
                font-weight: 200;
                text-align: left;
                border: none;
                margin: 0;
                background-color: #999999;  /* 未选中时的背景颜色 */
                border-top-left-radius: 0px;  /* 左上角直角（与手动操作按钮相邻） */
                border-top-right-radius: 5px;  /* 右上角圆角 */
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QPushButton:pressed {
                background-color: #888888;
            }
        """)
        self.program_tab_btn.clicked.connect(lambda: self.switch_top_tab(1))
        
        # 互斥选择
        self.top_tab_group = QButtonGroup(self)
        self.top_tab_group.addButton(self.manual_tab_btn, 0)
        self.top_tab_group.addButton(self.program_tab_btn, 1)
        self.top_tab_group.setExclusive(True)
        
        # 初始布局：手动操作占70%，编程占30%
        # 使用弹性系数而不是网格布局
        self.center_layout.addWidget(self.manual_tab_btn, stretch=7)  # 占70%
        self.center_layout.addWidget(self.program_tab_btn, stretch=3)  # 占30%
        
        center_widget.setLayout(self.center_layout)
        tab_layout.addWidget(center_widget, stretch=1)  # 中间区域可拉伸
        
        tab_container.setLayout(tab_layout)
        main_layout.addWidget(tab_container, stretch=0)
        
        # 添加底部弹性空间，让按钮靠上显示
        main_layout.addStretch()
        
        widget.setLayout(main_layout)
        
        return widget
        
    def create_right_vertical_buttons(self):
        """创建右侧垂直按钮区域 - 换页按钮和功能按钮在同一背景区域"""
        widget = QWidget()
        widget.setFixedWidth(180)  # 宽度包含换页按钮
        
        # 设置整个区域的背景渐变
        widget.setStyleSheet("""
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
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 左侧：竖排换页按钮
        pager_widget = self.create_vertical_pager_buttons()
        layout.addWidget(pager_widget, stretch=0)
        
        # 右侧：主要内容区域
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 1. 时间显示区域
        time_widget = QWidget()
        time_widget.setFixedHeight(115)
        time_widget.setStyleSheet("background: transparent; border: none;")

        time_layout = QVBoxLayout()
        time_layout.setContentsMargins(10, 10, 10, 5)
        time_layout.setSpacing(0)

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
        
        time_layout.addWidget(self.time_label)
        time_widget.setLayout(time_layout)
        content_layout.addWidget(time_widget, stretch=0)
        
        # 2. 按钮堆叠窗口
        self.right_buttons_stacked = QStackedWidget()
        self.right_buttons_stacked.setStyleSheet("background: transparent;")
        
        # 第1页：原有的6个按钮
        page1 = QWidget()
        page1.setStyleSheet("background: transparent;")
        page1_layout = QVBoxLayout(page1)
        page1_layout.setContentsMargins(5, 0, 0, 0)  # 左边距减少，因为换页按钮在旁边
        page1_layout.setSpacing(1)
        
        for i in range(6):
            btn = self.create_right_vertical_custom_button(i + 1)
            page1_layout.addWidget(btn)
        
        self.right_buttons_stacked.addWidget(page1)
        
        # 第2页：空页面
        page2 = QWidget()
        page2.setStyleSheet("background: transparent;")
        page2_layout = QVBoxLayout(page2)
        page2_layout.setContentsMargins(5, 0, 0, 0)
        page2_layout.setSpacing(1)
        
        for i in range(6):
            empty_btn = self.create_empty_right_button()
            page2_layout.addWidget(empty_btn)
        
        self.right_buttons_stacked.addWidget(page2)
        
        content_layout.addWidget(self.right_buttons_stacked, stretch=1)
        
        layout.addWidget(content_widget, stretch=1)
        
        # 启动定时器更新时间
        self.update_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)
        
        return widget

    def create_vertical_pager_buttons(self):
        """创建竖排换页按钮 - 绝对定位居中"""
        widget = QWidget()
        widget.setFixedWidth(10)
        widget.setFixedHeight(400)  # 固定高度
        
        widget.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
        """)
        
        # 计算居中位置
        container_height = 250
        button_height = 120
        button_spacing = 10  # 间距
        total_height = 2 * button_height + button_spacing
        start_y = (container_height - total_height) // 2 + 130
        
        self.vertical_pager_buttons = []
        
        # 第一个按钮
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
        
        # 第二个按钮（紧贴下方）
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

    def on_vertical_pager_clicked(self, index):
        """竖排换页按钮点击事件"""
        # 更新所有竖排换页按钮样式
        for i, btn in enumerate(self.vertical_pager_buttons):
            if i == index:
                # 选中状态（蓝色按钮）
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0000E9;  /* 蓝色背景 */
                        border: 1px solid #004488;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                    QPushButton:pressed {
                        background-color: #0055AA;
                    }
                """)
                btn.setChecked(True)
            else:
                # 未选中状态（黑色按钮）
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #000000;  /* 黑色背景 */
                        border: 1px solid #333333;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                    QPushButton:pressed {
                        background-color: #333333;
                    }
                """)
                btn.setChecked(False)
        
        # 切换右侧按钮页面
        if hasattr(self, 'right_buttons_stacked'):
            self.right_buttons_stacked.setCurrentIndex(index)

    def create_empty_right_button(self):
        """创建右侧区域第2页的空按钮"""
        btn = QPushButton()
        btn.setFixedSize(148, 98)  # 宽度减小，因为换页按钮占用了空间
        
        # 创建内部容器
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(2)
        
        # 添加占位文字
        placeholder = QLabel("(空)")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12pt;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        container_layout.addWidget(placeholder)
        btn.setLayout(container_layout)
        
        # 按钮基础样式
        btn.setStyleSheet("""
            QPushButton {
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
            QPushButton:pressed {
                border: 2px solid #555555;
                padding: 1px;
                background-color: #E7E7E7;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #E0E0E0,
                    stop: 0.3 #B7B7B7,
                    stop: 0.7 #B7B7B7,
                    stop: 1 #E0E0E0
                );
            }
        """)
        
        return btn

    def create_right_vertical_custom_button(self, button_type):
        """创建右侧垂直区域的自定义按钮"""
        btn = QPushButton()
        btn.setFixedSize(153, 98)
        
        # 创建内部容器
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(2)
        
        if button_type == 1:
            # 第一个按钮：左上角字母M + 右边图片
            top_layout = QHBoxLayout()
            
            # 左上角字母M
            m_label = QLabel("M")
            m_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            m_label.setStyleSheet("""
                QLabel {
                    font-size: 15pt; 
                    font-weight: bold; 
                    color: #000000;
                    padding-left: 5px;
                    padding-top: 2px;
                    margin: 0px;
                    border: none;
                    background-color: transparent;
                }
            """)
            
            # 右边图片 - 替换为右按钮1.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path1 = os.path.join(current_dir, "右按钮1.png")
            
            if os.path.exists(image_path1):
                # 使用QLabel显示图片
                left_icon = QLabel()
                pixmap = QPixmap(image_path1)
                # 缩放图片到合适大小
                scaled_pixmap = pixmap.scaled(115, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                left_icon.setPixmap(scaled_pixmap)
                left_icon.setStyleSheet("""
                    QLabel {
                        border: none;
                        margin: 0px;
                        padding: 0px;
                        background-color: transparent;
                    }
                """)
            else:
                # 如果图片不存在，使用原emoji
                left_icon = QLabel("▶️")
                left_icon.setStyleSheet("font-size: 16pt;")
            
            top_layout.addWidget(m_label)
            top_layout.addStretch()
            top_layout.addWidget(left_icon)
            
            container_layout.addLayout(top_layout)
            
        elif button_type == 2:
            # 第二个按钮：左上角字母S + 右边图片
            top_layout = QHBoxLayout()
            
            # 左上角字母S
            s_label = QLabel("S")
            s_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            s_label.setStyleSheet("""
                QLabel {
                    font-size: 15pt; 
                    font-weight: bold; 
                    color: #000000;
                    padding-left: 5px;
                    padding-top: 2px;
                    margin: 0px;
                    border: none;
                    background-color: transparent;
                }
            """)
            
            # 右边图片 - 替换为右按钮2.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path2 = os.path.join(current_dir, "右按钮2.png")
            
            if os.path.exists(image_path2):
                left_icon = QLabel()
                pixmap = QPixmap(image_path2)
                scaled_pixmap = pixmap.scaled(95, 95, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                left_icon.setPixmap(scaled_pixmap)
                left_icon.setStyleSheet("""
                    QLabel {
                        border: none;
                        margin: 0px;
                        padding: 0px;
                        background-color: transparent;
                    }
                """)
            else:
                left_icon = QLabel("⏸️")
                left_icon.setStyleSheet("font-size: 16pt;")
            
            top_layout.addWidget(s_label)
            top_layout.addStretch()
            top_layout.addWidget(left_icon)
            
            container_layout.addLayout(top_layout)
            
        elif button_type == 3:
            # 第三个按钮：图片居中 - 替换为右按钮3.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path3 = os.path.join(current_dir, "右按钮3.png")
            
            if os.path.exists(image_path3):
                icon_label = QLabel()
                pixmap = QPixmap(image_path3)
                scaled_pixmap = pixmap.scaled(150, 85, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setAlignment(Qt.AlignCenter)
            else:
                icon_label = QLabel("📝")
                icon_label.setAlignment(Qt.AlignCenter)
                icon_label.setStyleSheet("font-size: 24pt;")
            
            container_layout.addWidget(icon_label)
            
        elif button_type == 4:
            # 第四个按钮：无内容（保持不变）
            text_label = QLabel("")
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #000000;")
            container_layout.addWidget(text_label)
            
        elif button_type == 5:
            # 第五个按钮：表格布局
            grid_layout = QGridLayout()
            grid_layout.setContentsMargins(3, 3, 3, 3)
            grid_layout.setVerticalSpacing(3)
            grid_layout.setHorizontalSpacing(3)
            
            # 左上角：S100%标签（第0行，第0列）
            s_label = QLabel("S100%")
            s_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            s_label.setStyleSheet("""
                QLabel {
                    font-size: 15pt;
                    font-weight: bold;
                    color: #000000;
                    padding-left: 5px;
                }
            """)
            grid_layout.addWidget(s_label, 0, 0)  # 第0行，第0列
            
            # 左边中间：图片 - 替换为停止.png（第1行，第0列）
            current_dir = os.path.dirname(os.path.abspath(__file__))
            stop_image_path = os.path.join(current_dir, "停止.png")
            
            if os.path.exists(stop_image_path):
                left_icon = QLabel()
                pixmap = QPixmap(stop_image_path)
                scaled_pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                left_icon.setPixmap(scaled_pixmap)
                left_icon.setAlignment(Qt.AlignCenter)
                left_icon.setStyleSheet("border: none; margin: 0; padding: 0;")
            else:
                left_icon = QLabel("⚙️")
                left_icon.setAlignment(Qt.AlignCenter)
                left_icon.setStyleSheet("font-size: 20pt;")
            
            grid_layout.addWidget(left_icon, 1, 0)  # 第1行，第0列
            
            # 右边中间：图片 - 替换为运行1.png（跨越第0行和第1行，第1列）
            run1_image_path = os.path.join(current_dir, "运行1.png")
            
            if os.path.exists(run1_image_path):
                right_icon = QLabel()
                pixmap = QPixmap(run1_image_path)
                # 放大图片，因为现在要占据两行空间
                scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                right_icon.setPixmap(scaled_pixmap)
                right_icon.setAlignment(Qt.AlignCenter)
                right_icon.setStyleSheet("border: none; margin: 0; padding: 0;")
            else:
                right_icon = QLabel("📊")
                right_icon.setAlignment(Qt.AlignCenter)
                right_icon.setStyleSheet("font-size: 30pt;")  # 放大字体
            
            # 关键修改：让右边图片跨越2行（第0行和第1行）
            grid_layout.addWidget(right_icon, 0, 1, 2, 1)  # 从第0行开始，跨越2行，在第1列
            
            # 左下角：停止按钮（第2行，第0列）
            stop_btn = QPushButton("停止")
            stop_btn.setCheckable(True)
            stop_btn.setChecked(True)
            stop_btn.setFixedSize(62, 27)
            stop_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            stop_btn.setStyleSheet("""
                QPushButton {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #000000;
                    border: none;
                    border-radius: 2px;
                    background-color: transparent;
                    padding: 3px;
                    margin-left: 9px;
                }
                QPushButton:checked {
                    border: 2px solid #000000;
                    background-color: #80c2ff;
                    margin-left: 9px;
                }
                QPushButton:pressed {
                    background-color: #E0E0E0;
                }
                QPushButton:checked:pressed {
                    background-color: #80c2ff;
                    border: 2px solid #000000;
                }
            """)
            grid_layout.addWidget(stop_btn, 2, 0)  # 第2行，第0列
            
            # 右下角：运行按钮（第2行，第1列）
            run_btn = QPushButton("运行")
            run_btn.setCheckable(True)
            run_btn.setFixedSize(62, 27)
            run_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            run_btn.setStyleSheet("""
                QPushButton {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #000000;
                    border: none;
                    border-radius: 2px;
                    background-color: transparent;
                    padding: 3px;
                    margin-left: 1px;
                }
                QPushButton:checked {
                    border: 2px solid #000000;
                    background-color: #80c2ff;
                    margin-left: 1px;
                }
                QPushButton:pressed {
                    background-color: #E0E0E0;
                }
                QPushButton:checked:pressed {
                    background-color: #80c2ff;
                    border: 2px solid #000000;
                }
            """)
            grid_layout.addWidget(run_btn, 2, 1)  # 第2行，第1列
            
            # 创建按钮组
            self.speed_button_group = QButtonGroup()
            self.speed_button_group.addButton(stop_btn, 0)
            self.speed_button_group.addButton(run_btn, 1)
            self.speed_button_group.setExclusive(True)
            
            # 调整行拉伸比例，让图片行更高
            grid_layout.setRowStretch(0, 1)  # 第一行（S100%标签）
            grid_layout.setRowStretch(1, 3)  # 第二行（左边图片行）- 增加拉伸
            grid_layout.setRowStretch(2, 1)  # 第三行（按钮行）
            
            # 列拉伸比例
            grid_layout.setColumnStretch(0, 1)  # 第一列
            grid_layout.setColumnStretch(1, 1)  # 第二列
            
            container_layout.addLayout(grid_layout)
            
        elif button_type == 6:
            # 第六个按钮：表格布局
            grid_layout = QGridLayout()
            grid_layout.setContentsMargins(3, 3, 3, 3)
            grid_layout.setVerticalSpacing(3)
            grid_layout.setHorizontalSpacing(3)
            
            # 左上角：F100%标签（第0行，第0列）
            f_label = QLabel("F100%")
            f_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            f_label.setStyleSheet("""
                QLabel {
                    font-size: 15pt;
                    font-weight: bold;
                    color: #000000;
                    padding-left: 5px;
                }
            """)
            grid_layout.addWidget(f_label, 0, 0)  # 第0行，第0列
            
            # 左边中间：图片 - 替换为停止.png（第1行，第0列）
            current_dir = os.path.dirname(os.path.abspath(__file__))
            stop_image_path = os.path.join(current_dir, "停止.png")
            
            if os.path.exists(stop_image_path):
                left_icon = QLabel()
                pixmap = QPixmap(stop_image_path)
                scaled_pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                left_icon.setPixmap(scaled_pixmap)
                left_icon.setAlignment(Qt.AlignCenter)
                left_icon.setStyleSheet("border: none; margin: 0; padding: 0;")
            else:
                left_icon = QLabel("🔧")
                left_icon.setAlignment(Qt.AlignCenter)
                left_icon.setStyleSheet("font-size: 20pt;")
            
            grid_layout.addWidget(left_icon, 1, 0)  # 第1行，第0列
            
            # 右边中间：图片 - 替换为运行2.png（跨越第0行和第1行，第1列）
            run2_image_path = os.path.join(current_dir, "运行2.png")
            
            if os.path.exists(run2_image_path):
                right_icon = QLabel()
                pixmap = QPixmap(run2_image_path)
                # 放大图片，因为现在要占据两行空间
                scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                right_icon.setPixmap(scaled_pixmap)
                right_icon.setAlignment(Qt.AlignCenter)
                right_icon.setStyleSheet("border: none; margin: 0; padding: 0;")
            else:
                right_icon = QLabel("📈")
                right_icon.setAlignment(Qt.AlignCenter)
                right_icon.setStyleSheet("font-size: 30pt;")  # 放大字体
            
            # 关键修改：让右边图片跨越2行（第0行和第1行）
            grid_layout.addWidget(right_icon, 0, 1, 2, 1)  # 从第0行开始，跨越2行，在第1列
            
            # 左下角：停止按钮（第2行，第0列）
            up_btn = QPushButton("停止")
            up_btn.setCheckable(True)
            up_btn.setChecked(True)
            up_btn.setFixedSize(62, 27)
            up_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            up_btn.setStyleSheet("""
                QPushButton {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #000000;
                    border: none;
                    border-radius: 2px;
                    background-color: transparent;
                    padding: 3px;
                    margin-left: 9px;
                }
                QPushButton:checked {
                    border: 2px solid #000000;
                    background-color: #80c2ff;
                    margin-left: 9px;
                }
                QPushButton:pressed {
                    background-color: #E0E0E0;
                }
                QPushButton:checked:pressed {
                    background-color: #80c2ff;
                    border: 2px solid #000000;
                }
            """)
            grid_layout.addWidget(up_btn, 2, 0)  # 第2行，第0列
            
            # 右下角：运行按钮（第2行，第1列）
            down_btn = QPushButton("运行")
            down_btn.setCheckable(True)
            down_btn.setFixedSize(62, 27)
            down_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            down_btn.setStyleSheet("""
                QPushButton {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #000000;
                    border: none;
                    border-radius: 2px;
                    background-color: transparent;
                    padding: 3px;
                    margin-left: 1px;
                }
                QPushButton:checked {
                    border: 2px solid #000000;
                    background-color: #80c2ff;
                    margin-left: 1px;
                }
                QPushButton:pressed {
                    background-color: #E0E0E0;
                }
                QPushButton:checked:pressed {
                    background-color: #80c2ff;
                    border: 2px solid #000000;
                }
            """)
            grid_layout.addWidget(down_btn, 2, 1)  # 第2行，第1列
            
            # 创建按钮组
            self.feed_button_group = QButtonGroup()
            self.feed_button_group.addButton(up_btn, 0)
            self.feed_button_group.addButton(down_btn, 1)
            self.feed_button_group.setExclusive(True)
            
            # 调整行拉伸比例
            grid_layout.setRowStretch(0, 1)  # 第一行（F100%标签）
            grid_layout.setRowStretch(1, 3)  # 第二行（左边图片行）- 增加拉伸
            grid_layout.setRowStretch(2, 1)  # 第三行（按钮行）
            
            grid_layout.setColumnStretch(0, 1)  # 第一列
            grid_layout.setColumnStretch(1, 1)  # 第二列
            
            container_layout.addLayout(grid_layout)

        # 设置按钮的布局
        btn.setLayout(container_layout)

        # 按钮基础样式
        btn.setStyleSheet("""
            QPushButton {
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
            QPushButton:pressed {
                border: 2px solid #555555;
                padding: 1px;
                background-color: #E7E7E7;
                background: qlineargradient(
                    x1: 0.5, y1: 0,
                    x2: 0.5, y2: 1,
                    stop: 0 #E0E0E0,
                    stop: 0.3 #B7B7B7,
                    stop: 0.7 #B7B7B7,
                    stop: 1 #E0E0E0
                );
            }
        """)

        return btn

    def update_time(self):
        """更新时间显示 - 只显示HH:mm，每分钟更新"""
        current_time = QDateTime.currentDateTime()
        
        # 只格式化时分显示
        time_str = current_time.toString("HH:mm")
        
        # 更新标签
        if hasattr(self, 'time_label'):
            self.time_label.setText(time_str)
    
    def create_right_content(self):
        """创建右侧内容区域"""
        widget = QStackedWidget()
        
        # 手动操作内容页 - 重新设计布局
        manual_content = self.create_manual_content()
        widget.addWidget(manual_content)
        
        # 编程内容页（保持原样）
        program_content = QWidget()
        program_layout = QVBoxLayout()
        program_layout.setContentsMargins(40, 20, 40, 20)
        
        # 标题
        prog_title_label = QLabel("编程界面")
        prog_title_label.setStyleSheet("color: #000000; font-size: 24pt; font-weight: bold; padding-bottom: 20px;")
        program_layout.addWidget(prog_title_label)
        
        # 编程区域
        program_frame = QFrame()
        program_frame.setFrameStyle(QFrame.Box)
        program_frame.setStyleSheet("border: 1px solid #DDDDDD; padding: 20px; min-height: 400px;")
        program_inner_layout = QVBoxLayout()
        
        # 编程示例代码
        program_text = QTextEdit()
        program_text.setPlainText("""0""")
        program_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                color: #000000;
                font-family: "Courier New";
                font-size: 12pt;
                border: 1px solid #DDDDDD;
            }
        """)
        
        program_inner_layout.addWidget(program_text)
        program_frame.setLayout(program_inner_layout)
        
        program_layout.addWidget(program_frame)
        program_layout.addStretch()
        program_content.setLayout(program_layout)
        widget.addWidget(program_content)
        
        return widget
    
    def create_manual_content(self):
        """创建手动操作内容页 - 新布局"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # 外层布局无外边距
        main_layout.setSpacing(0)
        
        # === 1. 灰色背景区域（高度85px，#ECECEC）===
        gray_background = QWidget()
        gray_background.setFixedHeight(105)  # 高度
        gray_background.setStyleSheet("background-color: #ECECEC;")
        gray_layout = QVBoxLayout()
        gray_layout.setContentsMargins(0, 0, 0, 0)
        gray_layout.setSpacing(0)
        gray_background.setLayout(gray_layout)
        
        main_layout.addWidget(gray_background)
        
        # === 2. 位置显示框 - 横向占满===
        title_frame = QFrame()
        title_frame.setFixedHeight(40)
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #FCFCFC,
                    stop: 1 #E2E2E2
                );
                border-top: 2px solid #999999;
                border-right: none;
                border-bottom: none;
                border-left: none;
                margin: 0px;
            }
        """)

        # 直接在QFrame上设置布局和文字
        title_frame_layout = QHBoxLayout()
        title_frame_layout.setContentsMargins(10, 5, 20, 5)
        title_frame_layout.setSpacing(0)

        # 创建透明背景的QLabel
        title_text = QLabel("位置显示 <span style='color: #0000E9;'>模式：命令值</span>")
        title_text.setTextFormat(Qt.RichText)  # 启用富文本
        title_text.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 16pt;
                font-weight: bold;
                background-color: transparent;  /* 透明背景 */
                border: none;                   /* 无边框 */
            }
        """)

        title_frame_layout.addWidget(title_text)
        title_frame_layout.addStretch()

        title_frame.setLayout(title_frame_layout)
        main_layout.addWidget(title_frame)
        
        # === 3. 坐标显示区域（白色背景）- 也横向占满 ===
        coord_container = QWidget()
        coord_container.setStyleSheet("background-color: #FFFFFF;")
        coord_layout = QHBoxLayout()
        coord_layout.setContentsMargins(40, 10, 40, 10)
        coord_layout.setSpacing(30)

        # 初始化选中状态管理
        self.selected_display_item = None
        self.display_items = {}

        # 左侧坐标列
        left_coord_widget = QWidget()
        left_coord_layout = QVBoxLayout()
        left_coord_layout.setSpacing(5)

        # 创建唯一的item_id
        item_id_counter = 0

        # X坐标
        x_widget = self.create_display_item("X", "+0.000", f"coord_{item_id_counter}")
        self.display_items[f"coord_{item_id_counter}"] = x_widget
        item_id_counter += 1
        left_coord_layout.addWidget(x_widget)

        # Y坐标
        y_widget = self.create_display_item("Y", "+0.000", f"coord_{item_id_counter}")
        self.display_items[f"coord_{item_id_counter}"] = y_widget
        item_id_counter += 1
        left_coord_layout.addWidget(y_widget)

        # Z坐标
        z_widget = self.create_display_item("Z", "+428.000", f"coord_{item_id_counter}")
        self.display_items[f"coord_{item_id_counter}"] = z_widget
        item_id_counter += 1
        left_coord_layout.addWidget(z_widget)

        # A坐标
        a_widget = self.create_display_item("A", "+0.000", f"coord_{item_id_counter}")
        self.display_items[f"coord_{item_id_counter}"] = a_widget
        item_id_counter += 1
        left_coord_layout.addWidget(a_widget)

        left_coord_widget.setLayout(left_coord_layout)
        coord_layout.addWidget(left_coord_widget)

        # 右侧状态列
        right_status_widget = QWidget()
        right_status_layout = QVBoxLayout()
        right_status_layout.setContentsMargins(0, 10, 0, 0)  # 上边距
        right_status_layout.setSpacing(5)  # 统一间距

        # C状态
        c_widget = self.create_display_item("C", "+0.000", f"status_{item_id_counter}")
        self.display_items[f"status_{item_id_counter}"] = c_widget
        item_id_counter += 1
        right_status_layout.addWidget(c_widget)

        # S1状态
        s1_widget = self.create_display_item("S1", "+0.000", f"status_{item_id_counter}")
        self.display_items[f"status_{item_id_counter}"] = s1_widget
        item_id_counter += 1
        right_status_layout.addWidget(s1_widget)

        # 添加空白项保持与左侧高度一致（因为左侧有4项，右侧只有2项）
        right_status_layout.addStretch()
        right_status_widget.setLayout(right_status_layout)
        coord_layout.addWidget(right_status_widget)

        coord_layout.addStretch()
        coord_container.setLayout(coord_layout)
        main_layout.addWidget(coord_container)
        
        # === 4. 38x38图片按钮区域 ===
        small_btn_container = QWidget()
        small_btn_layout = QVBoxLayout()
        small_btn_layout.setContentsMargins(10, 10, 40, 10)
        small_btn_layout.setSpacing(8)

        # 两个38x38图片按钮
        image_files = ["38按钮1.png", "38按钮2.png"]

        for image_file in image_files:
            btn = QPushButton()
            btn.setFixedSize(38, 38)
            
            # 获取图片路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, image_file)
            
            if os.path.exists(image_path):
                # 转换路径为CSS格式
                css_path = image_path.replace('\\', '/')
                
                # 使用图片作为背景
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
                # 图片不存在时使用默认样式
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
            
            small_btn_layout.addWidget(btn)

        small_btn_layout.addStretch()
        small_btn_container.setLayout(small_btn_layout)
        main_layout.addWidget(small_btn_container)
        
        # === 5. 140x20按钮区域（6个按钮）===
        medium_btn_container = QWidget()
        medium_btn_layout = QHBoxLayout()
        medium_btn_layout.setContentsMargins(8, 5, 40, 5)
        medium_btn_layout.setSpacing(0)

        medium_btn_layout.addStretch()

        # 创建6个特殊按钮
        button_types = [1, 2, 3, 4, 5, 6]

        for btn_type in button_types:
            btn = self.create_special_button(btn_type)
            medium_btn_layout.addWidget(btn)
            medium_btn_layout.addStretch()

        medium_btn_container.setLayout(medium_btn_layout)
        main_layout.addWidget(medium_btn_container)
        
        # === 6. 底部灰色框区域 ===
        bottom_gray_box = QWidget()
        bottom_gray_box.setFixedHeight(100)
        bottom_gray_box.setStyleSheet("""
            QWidget {
                background-color: #ECECEC;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)

        # 底部灰色框的布局 - 调整左边距为0或更小
        bottom_box_layout = QVBoxLayout()
        bottom_box_layout.setContentsMargins(0, 5, 40, 0)  # 左边距改为0，紧靠左边界
        bottom_box_layout.setSpacing(0)

        # 第一个滑块行
        slider_row1 = QWidget()
        slider_row1_layout = QHBoxLayout()
        slider_row1_layout.setContentsMargins(0, 0, 0, 0)  # 行内边距为0
        slider_row1_layout.setSpacing(20)

        # 滑块1 - 左对齐
        slider1_widget = self.create_slider_widget(400, 20, "#E0E0E0", "#ECECEC", 0.66)
        slider_row1_layout.addWidget(slider1_widget)

        # 文字标签1 - 使用布局控制
        spacing_percent_sovr = "&nbsp;" * 4  # 4个空格

        label1 = QLabel(f"100%{spacing_percent_sovr}S-OVR")
        label1.setStyleSheet("color: #000000; font-size: 22pt; font-weight: bold;")
        label1.setTextFormat(Qt.RichText)
        slider_row1_layout.addWidget(label1)

        # 添加这一行：拉伸以填充剩余空间
        slider_row1_layout.addStretch()
        # 添加这一行：设置布局
        slider_row1.setLayout(slider_row1_layout)
        # 添加这一行：将滑块行添加到主布局
        bottom_box_layout.addWidget(slider_row1)

        # 第二个滑块行
        slider_row2 = QWidget()
        slider_row2_layout = QHBoxLayout()
        slider_row2_layout.setContentsMargins(0, 0, 0, 0)
        slider_row2_layout.setSpacing(20)

        # 滑块2
        slider2_widget = self.create_slider_widget(400, 20, "#E0E0E0", "#ECECEC", 0.66)
        slider_row2_layout.addWidget(slider2_widget)

        # 文字标签2 - 精确控制各个部分间距
        spacing_percent_fovr = "&nbsp;" * 4   # 100%和F-OVR之间的4个空格
        spacing_fovr_s1 = "&nbsp;" * 9       # F-OVR和S1之间的8个空格
        spacing_s1_limit = "&nbsp;" * 16      # S1和LIMIT之间的8个空格
        spacing_limit_1 = "&nbsp;" * 4      # LIMIT和1之间的8个空格

        label2 = QLabel(f"100%{spacing_percent_fovr}F-OVR{spacing_fovr_s1}S1{spacing_s1_limit}<span style='color: #1589fd;'>LIMIT{spacing_limit_1}1</span>")
        label2.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 22pt;
                font-weight: bold;
            }
        """)
        label2.setTextFormat(Qt.RichText)  # 启用富文本格式
        slider_row2_layout.addWidget(label2)

        slider_row2_layout.addStretch()
        slider_row2.setLayout(slider_row2_layout)
        bottom_box_layout.addWidget(slider_row2)

        bottom_gray_box.setLayout(bottom_box_layout)
        main_layout.addWidget(bottom_gray_box, stretch=0)

        widget.setLayout(main_layout)
        return widget
    
    def create_display_item(self, label, value, item_id):
        """创建统一的显示项 - 简化版本"""
        # 创建一个Frame而不是Widget，Frame有更好的事件处理
        widget = QFrame()
        widget.setFixedSize(530, 80)
        widget.setFrameShape(QFrame.Box)
        widget.setLineWidth(2)
        widget.setStyleSheet("""
            QFrame {
                border: 1px solid #757575;
                border-radius: 4px;
                background-color: #F7F7F7;
            }
        """)
        widget.item_id = item_id
        
        layout = QHBoxLayout(widget)  # 直接设置给widget
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # label部分
        label_widget = QLabel(label)
        label_widget.setFixedWidth(70)
        label_widget.setStyleSheet("""
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
        
        # value部分
        value_widget = QLabel(value)
        # 在创建value_widget设置对齐    
        value_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        value_widget.setStyleSheet("""
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
        """)
        
        # 存储样式
        value_widget.normal_style = value_widget.styleSheet()
        value_widget.selected_style = """
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
        
        widget.value_widget = value_widget
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        
        # 直接连接点击信号
        widget.mousePressEvent = lambda e, w=widget: self.handle_display_click(w)
        
        return widget

    def handle_display_click(self, clicked_widget):
        """处理点击"""
        print(f"Widget clicked: {clicked_widget.item_id}")
        
        # 取消之前选中的
        if hasattr(self, 'current_selected_widget') and self.current_selected_widget:
            self.current_selected_widget.value_widget.setStyleSheet(
                self.current_selected_widget.value_widget.normal_style
            )
        
        # 选中当前
        clicked_widget.value_widget.setStyleSheet(
            clicked_widget.value_widget.selected_style
        )
        self.current_selected_widget = clicked_widget
    
    def create_slider_widget(self, width, height, active_color, inactive_color, progress=0.66):
        """创建滑块控件 - 简单加粗边框"""
        widget = QWidget()
        widget.setFixedSize(width, height)
        
        # 外层容器 - 加粗边框
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {inactive_color};
                border: 2px solid #c0c0c0;  
                border-radius: 2px;  
            }}
        """)
        
        # 创建进度条覆盖层
        progress_widget = QWidget(widget)
        progress_width = int(width * progress)
        
        # 考虑3px边框，内边距
        border_width = 3
        inner_width = width - border_width * 2
        inner_height = height - border_width * 2
        
        # 计算进度在内层的宽度
        inner_progress_width = int(inner_width * progress)
        
        progress_widget.setGeometry(border_width, border_width, 
                                inner_progress_width, 
                                inner_height)
        
        progress_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {active_color};
                border: none;
                border-radius: 3px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
        """)
        
        return widget
    
    def create_bottom_area(self):
        """创建底部区域（分页按钮 + 功能按钮）"""
        widget = QWidget()
        
        # 底部背景渐变 - 占据完整宽度
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
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # === 1. 分页按钮（4个，高15宽120）===
        pager_widget = self.create_pager_buttons()
        layout.addWidget(pager_widget, stretch=0)
        
        # === 2. 功能按钮（8个，165x78）===
        bottom_buttons = self.create_bottom_buttons()
        layout.addWidget(bottom_buttons, stretch=0)
        
        widget.setLayout(layout)
        return widget
    
    def create_pager_buttons(self):
        """创建分页按钮（4个，高15宽120）- 无文字，选中整按钮变蓝"""
        widget = QWidget()
        # 增加分页按钮区域的高度
        widget.setFixedHeight(12)  # 垂直空间
        
        # 分页按钮区域的背景渐变（与底部区域一致）
        widget.setStyleSheet("""
            QWidget {
                background-color: #CBCBCB;
                border-top: 1px solid #AAAAAA;
            }
        """)
        
        # 创建水平布局容器
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        
        # 4个分页按钮 - 无文字
        self.pager_buttons = []
        
        for i in range(4):
            btn = QPushButton("")  # 空文字
            btn.setFixedSize(160, 10)  # 宽160，高10
            
            # 默认第一个选中（蓝色按钮）
            if i == 0:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #003cff;  /* 蓝色背景 */
                        border: 1px solid #004488;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                    QPushButton:pressed {
                        background-color: #0055AA;
                    }
                """)
                btn.setChecked(True)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #000000;  /* 黑色背景 */
                        border: 1px solid #333333;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                    QPushButton:pressed {
                        background-color: #333333;
                    }
                """)
            
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.on_pager_button_clicked(idx))
            
            container_layout.addWidget(btn)
            self.pager_buttons.append(btn)
        
        container.setLayout(container_layout)
        
        # 主布局，让容器居中
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 2, 0, 2)
        main_layout.addStretch()
        main_layout.addWidget(container)
        main_layout.addStretch()
        
        widget.setLayout(main_layout)
        return widget
    
    def create_bottom_buttons(self):
        """创建底部8个功能按钮 - 简化版"""
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
        page1 = QWidget()
        layout1 = QHBoxLayout(page1)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(1)
        
        buttons_config = [
            {"text": "M", "icon": None},
            {"text": "S", "icon": None},
            {"text": "F", "icon": None},
            {"text": "探测功能", "icon": "探测功能.png"},  # 修改为图片文件
            {"text": "原点管理", "icon": "原点管理.png"},  # 修改为图片文件
            {"text": "", "icon": None},
            {"text": "3D-ROT", "icon": "3D-ROT.png"},      # 修改为图片文件
            {"text": "刀具表", "icon": "刀具表.png"}       # 修改为图片文件
        ]
        
        for config in buttons_config:
            btn = self.create_bottom_button(config["text"], config["icon"])
            layout1.addWidget(btn)
        
        self.bottom_stacked_widget.addWidget(page1)
        
        # 第2-4页（空按钮）
        for page_num in range(2, 5):
            page = QWidget()
            layout = QHBoxLayout(page)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(1)
            
            for i in range(8):
                btn = self.create_bottom_button("")
                layout.addWidget(btn)
            
            self.bottom_stacked_widget.addWidget(page)
        
        # 主布局
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.bottom_stacked_widget)
        
        return widget
    
    def create_bottom_button(self, text, icon_filename=None):
        """创建底部按钮 - 支持本地图片"""
        # 使用QLabel
        label = QLabel()
        label.setFixedSize(160, 100)
        label.setAlignment(Qt.AlignCenter)
        label.setCursor(Qt.PointingHandCursor)  # 手型光标
        
        # 构建HTML内容
        html_content = self.create_button_html(text, icon_filename)
        
        if html_content:
            label.setText(html_content)
        
        # 样式
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

    def create_button_html(self, text, icon_filename):
        """创建按钮的HTML内容 - 支持本地图片"""
        if not text and not icon_filename:
            return ""
        
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 判断是否有图标
        has_icon = bool(icon_filename and icon_filename.lower().endswith('.png'))
        
        # 构建文字部分
        text_html = ""
        if text:
            if text.isalpha() and len(text) == 1:
                # 单字母按钮（M、S、F） - 根据是否有图标调整样式
                if has_icon:
                    # 有图标时：文字在上，使用较小字体
                    text_html = f"<div style='font-size: 20pt; font-weight: bold;'>{text}</div>"
                else:
                    # 无图标时：文字居中，使用较大字体
                    text_html = f"<div style='font-size: 25pt; font-weight: bold;'>{text}</div>"
            elif self.has_chinese(text):
                # 中文按钮
                chinese_chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
                if chinese_chars:
                    if len(chinese_chars) == 4:  # 四个汉字，分两行
                        line1 = f"{chinese_chars[0]}{chinese_chars[1]}"
                        line2 = f"{chinese_chars[2]}{chinese_chars[3]}"
                        text_html = f"""
                            <div style='font-size: 16pt; font-weight: bold; line-height: 1;'>
                                <div>{line1}</div>
                                <div>{line2}</div>
                            </div>
                        """
                    else:  # 两个汉字或其他
                        lines = []
                        for i in range(0, len(chinese_chars), 2):
                            line = ''.join(chinese_chars[i:i+2])
                            lines.append(f"<span style='font-size: 17pt; font-weight: bold;'>{line}</span>")
                        chinese_html = "<br>".join(lines)
                        text_html = f"<div style='line-height: 1.0;'>{chinese_html}</div>"
            else:
                # 英文或混合文字（如3D-ROT）
                text_html = f"<div style='font-size: 17pt; font-weight: bold;'>{text}</div>"
        
        # 构建图片部分
        img_html = ""
        if icon_filename:
            # 检查是否是图片文件（以.png结尾）
            if icon_filename.lower().endswith('.png'):
                icon_path = os.path.join(current_dir, icon_filename)
                if os.path.exists(icon_path):
                    try:
                        import base64
                        with open(icon_path, "rb") as img_file:
                            encoded_image = base64.b64encode(img_file.read()).decode('ascii')
                        
                        # 图片容器：固定高度，图片自适应保持比例
                        img_html = f"""
                            <div style='
                                margin-top: 5px; 
                                height: 45px; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center;
                                overflow: hidden;
                            '>
                                <img src='data:image/png;base64,{encoded_image}' 
                                    style='
                                        max-height: 100%;
                                        max-width: 100%;
                                        object-fit: contain;
                                    '>
                            </div>
                        """
                    except Exception as e:
                        print(f"加载图片 {icon_filename} 失败: {e}")
                        # 失败时使用占位符
                        img_html = "<div style='font-size: 24pt; margin-top: 10px;'>📷</div>"
                else:
                    # 图片不存在
                    print(f"图片文件不存在: {icon_filename}")
                    img_html = "<div style='font-size: 24pt; margin-top: 10px;'>❓</div>"
            else:
                # 不是png文件，当作emoji处理
                img_html = f"<div style='font-size: 24pt; margin-top: 10px;'>{icon_filename}</div>"
        
        # 根据是否有图标决定布局方式
        if has_icon:
            # 有图标：文字在上，图片在下
            return f"""
                <div style='
                    text-align: center; 
                    padding: 5px;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                '>
                    <div>{text_html}</div>
                    <div>{img_html}</div>
                </div>
            """
        else:
            # 无图标：文字居中（垂直和水平都居中）
            return f"""
                <div style='
                    text-align: center; 
                    padding: 5px;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                '>
                    <div>{text_html}</div>
                </div>
            """

    def has_chinese(self, text):
        """判断是否包含汉字"""
        if not text:
            return False
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    def create_special_button(self, button_type):
        """创建特殊格式的按钮"""
        if button_type == 2:  # 第二个按钮："T 5" + Z标签
            # 创建容器
            container = QWidget()
            container.setFixedSize(187, 30)
            
            # 布局
            layout = QHBoxLayout(container)
            layout.setContentsMargins(10, 0, 0, 0)  # 右边距为0
            layout.setSpacing(0)
            
            # T 5 标签
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
            
            # Z标签
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
            
            # 容器样式
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
            
            return container
        
        else:
            # 其他按钮使用QPushButton
            btn = QPushButton()
            btn.setFixedSize(187, 30)
            
            # 设置按钮文字
            if button_type == 1:
                btn = QPushButton()
                btn.setFixedSize(187, 30)
                
                # 添加图标
                coord_icon_path = os.path.join(os.path.dirname(__file__), "坐标.png")
                if os.path.exists(coord_icon_path):
                    # 先用QPixmap加载并缩放
                    pixmap = QPixmap(coord_icon_path)
                    scaled_pixmap = pixmap.scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    icon = QIcon(scaled_pixmap)
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(25, 25))
                    
                    btn.setText(" 0")
                else:
                    btn.setText("📊 0")
                
                btn.setStyleSheet("""
                    QPushButton {
                        border: 1px solid #969696;
                        border-radius: 10px;
                        background: qlineargradient(
                            x1: 0.5, y1: 0,
                            x2: 0.5, y2: 1,
                            stop: 0 #FDFDFD,
                            stop: 0.5 #EEEEEE,
                            stop: 1 #DDDDDD
                        );
                        font-size: 14pt;
                        font-weight: bold;
                        color: #0000D9;
                        text-align: left;
                        padding-left: 10px; 
                    }
                    QPushButton:pressed {
                        border: 1px solid #868686;
                        background: qlineargradient(
                            x1: 0.5, y1: 0,
                            x2: 0.5, y2: 1,
                            stop: 0 #EDEDED,
                            stop: 0.5 #DEDEDE,
                            stop: 1 #CDCDCD
                        );
                    }
                """)
            elif button_type == 3:
                btn.setText("S  0")
            elif button_type == 4:
                btn.setText("F  0mm/min")
            elif button_type == 5:
                btn.setText("Over  100%")
            elif button_type == 6:
                btn.setText("M  5/9")
            
            # 按钮样式
            btn.setStyleSheet("""
                QPushButton {
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
                    color: #0000D9;
                    text-align: left;
                    padding-left: 5px; 
                }
                QPushButton:pressed {
                    border: 1px solid #868686;
                    background: qlineargradient(
                        x1: 0.5, y1: 0,
                        x2: 0.5, y2: 1,
                        stop: 0 #EDEDED,
                        stop: 0.5 #DEDEDE,
                        stop: 1 #CDCDCD
                    );
                }
            """)
            
            return btn


    def on_display_item_clicked(self, widget):
        """显示项被点击时的处理"""
        # 如果已经选中，则取消选中
        if self.selected_display_item == widget.item_id:
            self.deselect_display_item(widget.item_id)
            self.selected_display_item = None
        else:
            # 取消之前选中的项
            if self.selected_display_item is not None:
                self.deselect_display_item(self.selected_display_item)
            
            # 选中当前项
            self.select_display_item(widget.item_id)
            self.selected_display_item = widget.item_id

    def select_display_item(self, item_id):
        """选中显示项 - 只改变value背景颜色"""
        if item_id in self.display_items:
            widget = self.display_items[item_id]
            # 只修改value部分的背景颜色为#83a3e3渐变
            widget.value_widget.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 28pt;
                    font-weight: bold;
                    padding-left: 20px;
                    qproperty-alignment: AlignLeft | AlignVCenter;
                    background: qlineargradient(
                        x1: 0.5, y1: 0,
                        x2: 0.5, y2: 1,
                        stop: 0 #A0C0FF,     /* 顶部浅蓝色 */
                        stop: 0.3 #83a3e3,   /* 中间#83a3e3 */
                        stop: 1 #83a3e3      /* 底部#83a3e3 */
                    );
                    border-top-right-radius: 2px;
                    border-bottom-right-radius: 2px;
                }
            """)

    def deselect_display_item(self, item_id):
        """取消选中显示项 - 恢复value背景颜色"""
        if item_id in self.display_items:
            widget = self.display_items[item_id]
            # 恢复value部分的原始渐变样式
            widget.value_widget.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 28pt;
                    font-weight: bold;
                    padding-left: 20px;
                    qproperty-alignment: AlignLeft | AlignVCenter;
                    background: qlineargradient(
                        x1: 0.5, y1: 0,
                        x2: 0.5, y2: 1,
                        stop: 0 #FFFFFF,
                        stop: 0.3 #DEDEDE,
                        stop: 1 #DEDEDE
                    );
                    border-top-right-radius: 2px;
                    border-bottom-right-radius: 2px;
                }
            """)
    
    def on_pager_button_clicked(self, index):
        """分页按钮点击事件"""
        # 更新所有分页按钮样式
        for i, btn in enumerate(self.pager_buttons):
            if i == index:
                # 选中状态（蓝色按钮）
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0000E9;  /* 蓝色背景 */
                        border: 1px solid #004488;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                    QPushButton:pressed {
                        background-color: #0055AA;
                    }
                """)
                btn.setChecked(True)
            else:
                # 未选中状态（黑色按钮）
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #000000;  /* 黑色背景 */
                        border: 1px solid #333333;
                        border-radius: 3px;
                        margin: 0;
                        padding: 0;
                    }
                    QPushButton:pressed {
                        background-color: #333333;
                    }
                """)
                btn.setChecked(False)
        
        # 切换底部按钮页面
        if hasattr(self, 'bottom_stacked_widget'):
            self.bottom_stacked_widget.setCurrentIndex(index)
    
    def switch_top_tab(self, index):
        """切换顶部标签 - 动态调整比例"""
        # 记录当前选中的标签
        self.current_top_tab = index
        
        # 切换内容
        if self.right_content:
            self.right_content.setCurrentIndex(index)
        
        # 更新顶部标签样式和布局比例
        self.update_top_tab_layout()
    
    def update_top_tab_layout(self):
        """更新顶部标签的布局比例 - 修改为弹性系数方式"""
        # 清除当前中心布局中的所有项
        while self.center_layout.count():
            item = self.center_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        # 根据当前选中的标签重新布局
        if self.current_top_tab == 0:  # 手动操作选中
            # 手动操作占70%，编程占30%
            self.center_layout.addWidget(self.manual_tab_btn, stretch=7)
            self.center_layout.addWidget(self.program_tab_btn, stretch=3)
            
            # 更新按钮样式
            self.manual_tab_btn.setStyleSheet("""
                QPushButton {
                    color: #0000E9;  /* 蓝色文字 */
                    font-size: 20pt;
                    font-weight: 200;
                    text-align: left;
                    padding-left: 5px;
                    margin: 0;
                    background-color: #DDDDDD;
                    border-top: 1px solid #FFFFFF;  /* 上边框 - 白色细边框 */
                    border-left: 1px solid #FFFFFF;  /* 左边框 - 白色细边框 */
                    border-right: 1px solid #FFFFFF;  /* 右边框 - 白色细边框 */
                    border-bottom: none;  /* 下边框 - 无边框 */
                    border-top-left-radius: 5px;  /* 左上角圆角 */
                    border-top-right-radius: 0px;  /* 右上角直角 */
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                }
                QPushButton:pressed {
                    background-color: #CCCCCC;
                }
            """)
            
            self.program_tab_btn.setStyleSheet("""
                QPushButton {
                    color: #000000;  /* 黑色文字 */
                    font-size: 20pt;
                    font-weight: 200;
                    text-align: left;
                    padding-left: 5px;
                    margin: 0;
                    background-color: #999999;
                    border-top: 1px solid #FFFFFF;  /* 上边框 - 白色细边框 */
                    border-left: 1px solid #FFFFFF;  /* 左边框 - 白色细边框 */
                    border-right: 1px solid #FFFFFF;  /* 右边框 - 白色细边框 */
                    border-bottom: none;  /* 下边框 - 无边框 */
                    border-top-left-radius: 0px;  /* 左上角直角 */
                    border-top-right-radius: 5px;  /* 右上角圆角 */
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                }
                QPushButton:pressed {
                    background-color: #888888;
                }
            """)
            
        else:  # 编程选中
            # 编程占70%，手动操作占30%
            self.center_layout.addWidget(self.manual_tab_btn, stretch=3)
            self.center_layout.addWidget(self.program_tab_btn, stretch=7)
            
            # 更新按钮样式
            self.manual_tab_btn.setStyleSheet("""
                QPushButton {
                    color: #000000;  /* 黑色文字 */
                    font-size: 20pt;
                    font-weight: 200;
                    text-align: left;
                    padding-left: 5px;
                    margin: 0;
                    background-color: #999999;
                    border-top: 1px solid #FFFFFF;  /* 上边框 - 白色细边框 */
                    border-left: 1px solid #FFFFFF;  /* 左边框 - 白色细边框 */
                    border-right: 1px solid #FFFFFF;  /* 右边框 - 白色细边框 */
                    border-bottom: none;  /* 下边框 - 无边框 */
                    border-top-left-radius: 5px;  /* 左上角圆角 */
                    border-top-right-radius: 0px;  /* 右上角直角 */
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                }
                QPushButton:pressed {
                    background-color: #888888;
                }
            """)
            
            self.program_tab_btn.setStyleSheet("""
                QPushButton {
                    color: #0000E9;  /* 蓝色文字 */
                    font-size: 20pt;
                    font-weight: 200;
                    text-align: left;
                    padding-left: 5px;
                    margin: 0;
                    background-color: #DDDDDD;
                    border-top: 1px solid #FFFFFF;  /* 上边框 - 白色细边框 */
                    border-left: 1px solid #FFFFFF;  /* 左边框 - 白色细边框 */
                    border-right: 1px solid #FFFFFF;  /* 右边框 - 白色细边框 */
                    border-bottom: none;  /* 下边框 - 无边框 */
                    border-top-left-radius: 0px;  /* 左上角直角 */
                    border-top-right-radius: 5px;  /* 右上角圆角 */
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                }
                QPushButton:pressed {
                    background-color: #CCCCCC;
                }
            """)

# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = TNC640DynamicRatioUI()
    window.show()
    
    print("✅ TNC640 动态比例界面已启动")
    print("✅ 修改内容:")
    print("   1. 右侧垂直按钮区域（150px宽，只延伸到中间内容区域）")
    print("   2. 底部区域独立占据完整窗口宽度")
    print("   3. 底部8个功能按钮（165px宽）")
    print("   4. 顶部标签动态比例：选中的占70%，未选中的占30%")
    print("   5. 手动操作页面全新布局：")
    print("      - 85px高灰色背景区域（#ECECEC）")
    print("      - 位置显示标题框（#FCFCFC到#E2E2E2渐变，带边框）")
    print("      - 坐标显示区域（X/Y/Z/A + C/S1）")
    print("      - 38x38按钮区域")
    print("      - 5个140x20按钮区域")
    print("      - 滑块区域（305x20渐变滑块 + 文字标签）")
    
    sys.exit(app.exec_())