# @我是指针* 记得B站点个关注谢谢
# 2023-02-02 - 2023-02-03
# 使用了Pyside6 模板使用了One-dark

import json
import os
import sys

from gui.core.json_settings import Settings
from gui.uis.windows.main_window import *
from qt_core import *

# DPI 缩放
os.environ["QT_FONT_DPI"] = "96"


# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # SETUP MAIN WINDOw
        self.dragPos = None
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        self.setup = SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # 修改配置
    def write_setting(self):
        setting1 = json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        fp = open("./settings.json", mode="w", encoding="utf-8")
        fp.write(setting1)
        fp.close()

    # 选择数据集
    def select_images_path(self):
        filepath = QFileDialog.getExistingDirectory(self, "选择数据集", "./")
        if len(filepath) > 1:
            self.setup.edt_select_images_path.setText(filepath)
            self.settings['images_path'] = filepath
            self.write_setting()

    # 选择Voc输出
    def select_voc_path(self):
        filepath = QFileDialog.getExistingDirectory(self, "选择Voc输出目录", "./")
        if len(filepath) > 1:
            self.setup.edt_select_voc_path.setText(filepath)
            self.settings['voc_path'] = filepath
            self.write_setting()

    # 选择yaml配置
    def select_yaml_path(self):
        filepath, _ = QFileDialog.getOpenFileNames(self, '打开(.yaml)', './', 'yolov5配置文件 (*.yaml)')
        if len(filepath) >= 1:
            self.setup.edt_select_yaml_path.setText(filepath[0])
            self.settings['yaml_path'] = filepath[0]
            self.write_setting()

    # 选择推理模型
    def select_pt_path(self):
        filepath, _ = QFileDialog.getOpenFileNames(self, '打开(.pt)', './', 'yolov5模型文件 (*.pt)')
        if len(filepath) >= 1:
            self.setup.edt_select_pt_path.setText(filepath[0])
            self.settings['model_path'] = filepath[0]
            self.write_setting()

    # 选择标签类别
    def select_labels_path(self):
        filepath, _ = QFileDialog.getOpenFileNames(self, '打开(.txt)', './', 'yolov5标签文件 (*.txt)')
        if len(filepath) >= 1:
            self.setup.edt_select_labels_path.setText(filepath[0])
            self.settings['labels_path'] = filepath[0]
            self.write_setting()

    # 推理 请修改这里的"yolov5" 是你的conda虚拟环境名称，如果没有请直接使用python运行auto_inference.py
    def inference(self):
        # 我是指针*制作 感谢支持
        self.write_setting()
        current_path = os.path.abspath('./')  # 获取当前绝对路径
        pan = current_path[0:1]  # 获取盘符
        os.popen(f'start cmd /K "{pan}: && cd {current_path} && activate yolov5 && python auto_inference.py"')

    # 调整大小事件
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos


if __name__ == "__main__":
    # APP
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    window = MainWindow()

    # 运行APP
    sys.exit(app.exec())
