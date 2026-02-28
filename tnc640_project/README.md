# TNC640 数控系统仿真界面

这是一个基于 PyQt5 的 TNC640 数控系统仿真界面项目。

## 项目结构

tnc640_project/
├── main.py # 程序入口
├── requirements.txt # 依赖包
├── images/ # 图片资源目录
│ ├── 手动操作.png
│ ├── 编程.png
│ └── ...
├── src/ # 源代码目录
│ ├── ui/ # UI相关
│ │ ├── main_window.py # 主窗口
│ │ ├── top_panel.py # 顶部标签面板
│ │ ├── right_panel.py # 右侧按钮面板
│ │ ├── bottom_panel.py # 底部面板
│ │ └── pages/ # 页面
│ │ ├── manual_page.py # 手动操作页面
│ │ └── program_page.py# 编程页面
│ ├── widgets/ # 自定义小部件
│ │ ├── buttons.py # 按钮组件
│ │ ├── displays.py # 显示组件
│ │ └── sliders.py # 滑块组件
│ ├── utils/ # 工具函数
│ │ ├── image_loader.py # 图片加载
│ │ ├── style_helper.py # 样式助手
│ │ └── text_utils.py # 文本工具
│ └── config/ # 配置
│ ├── colors.py # 颜色配置
│ ├── sizes.py # 尺寸配置
│ └── paths.py # 路径配置
└── README.md # 说明文档

## 功能特点

1. **模块化设计**：代码按照功能模块分离，便于维护和扩展
2. **动态比例布局**：顶部标签根据选中状态动态调整比例（70%/30%）
3. **多页面切换**：支持手动操作和编程页面切换
4. **自定义组件**：丰富的自定义UI组件
5. **本地图片支持**：支持加载本地图片资源

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt