"""主窗口"""
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from src.config.sizes import SIZES
from .top_panel import TopPanel
from .right_panel import RightPanel
from .bottom_panel import BottomPanel
from .pages.manual_page import ManualPage
from .pages.program_page import ProgramPage

class MainWindow(QMainWindow):
    """主窗口类"""
    def __init__(self):
        super().__init__()
        self.current_top_tab = 0  # 0=手动操作, 1=编程
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口
        self.setWindowTitle("TNC640 数控系统")
        self.setGeometry(100, 100, SIZES["WINDOW_WIDTH"], SIZES["WINDOW_HEIGHT"])
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === 中间主内容区域 ===
        middle_area = self.create_middle_area()
        main_layout.addWidget(middle_area, stretch=1)
        
        # === 底部区域 ===
        bottom_area = self.create_bottom_area()
        main_layout.addWidget(bottom_area, stretch=0)
        
        central_widget.setLayout(main_layout)
        
        # 应用样式
        self.setStyleSheet("QMainWindow { background-color: #FFFFFF; }")
    
    def create_middle_area(self):
        """创建中间主内容区域"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 左侧主内容区域
        left_main_widget = self.create_left_main_content()
        layout.addWidget(left_main_widget, stretch=1)
        
        # 右侧垂直按钮区域
        right_buttons_widget = RightPanel()
        layout.addWidget(right_buttons_widget, stretch=0)
        
        return widget
    
    def create_left_main_content(self):
        """创建左侧主内容区域"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 顶部标签
        self.top_panel = TopPanel()
        self.top_panel.manual_tab_btn.clicked.connect(lambda: self.switch_top_tab(0))
        self.top_panel.program_tab_btn.clicked.connect(lambda: self.switch_top_tab(1))
        
        layout.addWidget(self.top_panel, stretch=5)
        
        # 中间内容区域
        self.content_stacked = QStackedWidget()
        
        # 手动操作页面
        manual_page = ManualPage()
        self.content_stacked.addWidget(manual_page)
        
        # 编程页面
        program_page = ProgramPage()
        self.content_stacked.addWidget(program_page)
        
        layout.addWidget(self.content_stacked, stretch=36)
        
        return widget
    
    def create_bottom_area(self):
        """创建底部区域"""
        return BottomPanel()
    
    def switch_top_tab(self, index):
        """切换顶部标签"""
        self.current_top_tab = index
        self.top_panel.switch_tab(index)
        self.content_stacked.setCurrentIndex(index)