"""顶部标签面板"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from src.utils.image_loader import load_pixmap
from src.config import sizes

class TopPanel(QWidget):
    """顶部标签面板"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_tab = 0  # 0=手动操作, 1=编程
        self.manual_tab_btn = None
        self.program_tab_btn = None
        self.center_layout = None
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #DDDDDD;
                border-radius: 5px;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 0, 5, 5)
        main_layout.setSpacing(0)
        
        # 标签按钮容器
        tab_container = QWidget()
        tab_container.setStyleSheet("background-color: transparent;")
        
        tab_layout = QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        # 中间标签区域
        center_widget = QWidget()
        center_widget.setStyleSheet("background-color: transparent;")
        self.center_layout = QHBoxLayout(center_widget)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)
        
        # 创建标签按钮
        self.create_tab_buttons()
        
        # 初始布局
        self.update_layout()
        
        center_widget.setLayout(self.center_layout)
        tab_layout.addWidget(center_widget, stretch=1)
        tab_container.setLayout(tab_layout)
        main_layout.addWidget(tab_container, stretch=0)
        main_layout.addStretch()
    
    def create_tab_buttons(self):
        """创建标签按钮"""
        # 手动操作按钮
        self.manual_tab_btn = self.create_tab_button("手动操作.png", "手动操作", 0)
        
        # 编程按钮
        self.program_tab_btn = self.create_tab_button("编程.png", "编程", 1)
    
    def create_tab_button(self, icon_file, text, tab_id):
        """创建单个标签按钮"""
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setMinimumHeight(sizes.SIZES["TOP_TAB_HEIGHT"])
        
        # 创建按钮布局
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(5, 0, 0, 0)
        btn_layout.setSpacing(10)
        
        # 图标
        pixmap = load_pixmap(icon_file, 47, 47)
        if pixmap:
            icon_label = QLabel()
            icon_label.setPixmap(pixmap)
        else:
            icon_label = QLabel("📝" if tab_id == 0 else "📄")
            icon_label.setStyleSheet("font-size: 20pt;")
        
        # 文字
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                color: #0000E9;
                font-size: 20pt;
                font-weight: 200;
                background-color: transparent;
            }
        """)
        
        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()
        
        btn.setLayout(btn_layout)
        
        # 连接信号
        if tab_id == 0:
            btn.clicked.connect(lambda: self.switch_tab(0))
            btn.setChecked(True)
        else:
            btn.clicked.connect(lambda: self.switch_tab(1))
        
        return btn
    
    def switch_tab(self, tab_id):
        """切换标签"""
        self.current_tab = tab_id
        self.update_layout()
    
    def update_layout(self):
        """更新布局"""
        # 清除当前布局
        while self.center_layout.count():
            item = self.center_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        # 根据当前标签重新布局
        if self.current_tab == 0:
            self.center_layout.addWidget(self.manual_tab_btn, stretch=7)
            self.center_layout.addWidget(self.program_tab_btn, stretch=3)
            self.update_button_styles(selected=0)
        else:
            self.center_layout.addWidget(self.manual_tab_btn, stretch=3)
            self.center_layout.addWidget(self.program_tab_btn, stretch=7)
            self.update_button_styles(selected=1)
    
    def update_button_styles(self, selected):
        """更新按钮样式"""
        manual_style = self.get_button_style(selected == 0, is_left=True)
        program_style = self.get_button_style(selected == 1, is_left=False)
        
        self.manual_tab_btn.setStyleSheet(manual_style)
        self.program_tab_btn.setStyleSheet(program_style)
    
    def get_button_style(self, is_selected, is_left):
        """获取按钮样式"""
        if is_selected:
            color = "#0000E9"
            bg_color = "#DDDDDD"
        else:
            color = "#000000"
            bg_color = "#999999"
        
        if is_left:
            border_radius = "border-top-left-radius: 5px; border-top-right-radius: 0px;"
        else:
            border_radius = "border-top-left-radius: 0px; border-top-right-radius: 5px;"
        
        return f"""
            QPushButton {{
                color: {color};
                font-size: 20pt;
                font-weight: 200;
                text-align: left;
                border: none;
                margin: 0;
                background-color: {bg_color};
                border-top: 1px solid #FFFFFF;
                border-left: 1px solid #FFFFFF;
                border-right: 1px solid #FFFFFF;
                border-bottom: none;
                {border_radius}
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
            QPushButton:pressed {{
                background-color: #CCCCCC;
            }}
        """