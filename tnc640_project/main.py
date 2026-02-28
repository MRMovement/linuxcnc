import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    """程序主入口"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    print("✅ TNC640 数控系统已启动")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()