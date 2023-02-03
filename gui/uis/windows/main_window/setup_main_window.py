from .functions_main_window import *


class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.edt_select_labels_path = None
        self.edt_select_pt_path = None
        self.btn_select_pt_path = None
        self.btn_select_yaml_path = None
        self.edt_select_yaml_path = None
        self.btn_select_voc_path = None
        self.edt_select_voc_path = None
        self.icon_file = None
        self.btn_select_images_path = None
        self.edt_select_images_path = None
        self.settings = None
        self.themes = None
        self.btn_select_labels_path = None
        self.btn_start_auto_inference = None
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # 加载自动标注库
        # self.auto_inference = Auto_inference()

    # 添加左侧菜单
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon": "icon_home.svg",
            "btn_id": "btn_home",
            "btn_text": "主页",
            "btn_tooltip": "主页",
            "show_top": True,
            "is_active": True
        },
    ]

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("阿斯顿 to PyOneDark")

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # 加载主题颜色
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # PAGES
        # ///////////////////////////////////////////////////////////////
        # 单行输入框输入数据集路径
        self.edt_select_images_path = PyLineEdit(
            text=self.settings['images_path'],
            place_holder_text="数据集路径",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.edt_select_images_path.setMinimumHeight(35)
        self.ui.load_pages.center_page_layout.addWidget(self.edt_select_images_path)

        # 选择数据集
        self.btn_select_images_path = PyPushButton(
            text="选择数据集",
            radius=8,
            color="#FFFFFF",
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.btn_select_images_path.setMinimumHeight(35)

        self.ui.load_pages.center_page_layout.addWidget(self.btn_select_images_path)

        # 单行输入框输入数据集路径
        self.edt_select_voc_path = PyLineEdit(
            text=self.settings['voc_path'],
            place_holder_text="Voc标签文件路径",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.edt_select_voc_path.setMinimumHeight(35)
        self.ui.load_pages.center_page_layout.addWidget(self.edt_select_voc_path)

        # 选择保存Voc标签文件路径
        self.btn_select_voc_path = PyPushButton(
            text="选择保存Voc标签文件路径",
            radius=8,
            color="#FFFFFF",
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.btn_select_voc_path.setMinimumHeight(35)

        self.ui.load_pages.center_page_layout.addWidget(self.btn_select_voc_path)

        # 配置文件(.yaml)路径
        self.edt_select_yaml_path = PyLineEdit(
            text=self.settings['yaml_path'],
            place_holder_text="配置文件(.yaml)文件路径",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.edt_select_yaml_path.setMinimumHeight(35)
        self.ui.load_pages.center_page_layout.addWidget(self.edt_select_yaml_path)

        # 选择配置文件
        self.btn_select_yaml_path = PyPushButton(
            text="选择配置文件(.yaml)",
            radius=8,
            color="#FFFFFF",
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.btn_select_yaml_path.setMinimumHeight(35)

        self.ui.load_pages.center_page_layout.addWidget(self.btn_select_yaml_path)

        # 选择推理模型
        self.edt_select_pt_path = PyLineEdit(
            text=self.settings['model_path'],
            place_holder_text="推理模型(.pt)文件路径",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.edt_select_pt_path.setMinimumHeight(35)
        self.ui.load_pages.center_page_layout.addWidget(self.edt_select_pt_path)

        # 选择推理模型
        self.btn_select_pt_path = PyPushButton(
            text="选择推理模型(.pt)",
            radius=8,
            color="#FFFFFF",
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.btn_select_pt_path.setMinimumHeight(35)

        self.ui.load_pages.center_page_layout.addWidget(self.btn_select_pt_path)

        # 选择标注类别文件(.txt)
        self.edt_select_labels_path = PyLineEdit(
            text=self.settings['labels_path'],
            place_holder_text="标注类别文件(.txt)文件路径",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.edt_select_labels_path.setMinimumHeight(35)
        self.ui.load_pages.center_page_layout.addWidget(self.edt_select_labels_path)

        # 选择标注类别文件
        self.btn_select_labels_path = PyPushButton(
            text="选择标注类别文件(.txt)",
            radius=8,
            color="#FFFFFF",
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.btn_select_labels_path.setMinimumHeight(35)

        self.ui.load_pages.center_page_layout.addWidget(self.btn_select_labels_path)

        # 开始自动标注
        self.btn_start_auto_inference = PyPushButton(
            text="开始自动标注",
            radius=8,
            color="#FF4300",
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.btn_start_auto_inference.setMinimumHeight(35)

        self.ui.load_pages.center_page_layout.addWidget(self.btn_start_auto_inference)

        # 设置信号
        self.btn_select_images_path.clicked.connect(self.select_images_path)
        self.btn_select_voc_path.clicked.connect(self.select_voc_path)
        self.btn_select_yaml_path.clicked.connect(self.select_yaml_path)
        self.btn_select_pt_path.clicked.connect(self.select_pt_path)
        self.btn_select_labels_path.clicked.connect(self.select_labels_path)
        self.btn_start_auto_inference.clicked.connect(self.inference)
        return self

    # 选择数据集
    def select_images_path(self):
        # filepath = QFileDialog.getExistingDirectory(None, "选择数据集", "../")
        print(self)
        # if len(filepath) > 1:
        #     self.setup_gui()

    def select_voc_path(self):
        pass

    def select_yaml_path(self):
        pass

    def select_pt_path(self):
        pass

    def select_labels_path(self):
        pass

    def inference(self):
        pass

    # RESIZE GRIPS AND CHANGE POSITION
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
