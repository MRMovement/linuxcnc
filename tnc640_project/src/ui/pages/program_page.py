"""编程页面"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QTextEdit

class ProgramPage(QWidget):
    """编程页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        
        # 标题
        title_label = QLabel("编程界面")
        title_label.setStyleSheet("""
            QLabel {
                color: #000000; 
                font-size: 24pt; 
                font-weight: bold; 
                padding-bottom: 20px;
            }
        """)
        layout.addWidget(title_label)
        
        # 编程区域
        program_frame = QFrame()
        program_frame.setFrameStyle(QFrame.Box)
        program_frame.setStyleSheet("""
            border: 1px solid #DDDDDD; 
            padding: 20px; 
            min-height: 400px;
        """)
        
        program_layout = QVBoxLayout(program_frame)
        
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
        
        program_layout.addWidget(program_text)
        layout.addWidget(program_frame)
        layout.addStretch()