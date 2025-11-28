from PyQt5.QtWidgets import (QPushButton, QDialogButtonBox, QComboBox, QMessageBox,
                             QTextEdit, QLineEdit, QLabel, QSpinBox, QCheckBox, QApplication)
from PyQt5.QtGui import QPalette

class ThemeManager:
    def __init__(self, theme, UI_manifester):

        app = QApplication.instance() or QApplication([])
        self.default_bg_color = app.palette().color(QPalette.Window).name()

        self.theme_color_map = {
            'main_bg_color': None,
            'highlight': None,
            'completed': None,
            'new': None,
            'edit': None,
            'view': None,
            'less_urgent': None,
            'normal': None,
            'btn_border': None,
            'btn_border_hover': None,
            'btn_border_pressed': None,
            'hover': None,
            'pressed': None,
            'selection_bg': None,
            'abstractvieww_bg': None,
            'label': None,
            'drop_down_arrow_path': None,
            "drop_up_arrow_path": None
        }

        self.theme = theme
        self.UI_manifester = UI_manifester

    def set_theme_color(self):
        if self.theme == 'light':
            self.theme_color_map['main_bg_color'] = self.default_bg_color
            self.theme_color_map['highlight'] = "#C05664"
            self.theme_color_map['completed'] = "#8FBCDF"
            self.theme_color_map['new'] = "#6813A4"
            self.theme_color_map['edit'] = "#58A1AB"
            self.theme_color_map['view'] = "gray"
            self.theme_color_map['normal'] = "black"
            self.theme_color_map['btn_border'] = '1px solid #3E3E3E'
            self.theme_color_map['btn_border_hover'] = '1px solid #7E8E9E'
            self.theme_color_map['btn_border_pressed'] = '1px solid #0A0A0A'
            self.theme_color_map['hover'] = "#C7C7C7"
            self.theme_color_map['pressed'] = "#9E9E9E"
            self.theme_color_map['selection_bg'] = "#9295A3"
            self.theme_color_map['abstractvieww_bg'] = "white"
            self.theme_color_map['label'] = "black"
            self.theme_color_map['drop_down_arrow_path'] = "url('./img/black_down_arrow.png')"
            self.theme_color_map['drop_up_arrow_path'] = "url('./img/black_up_arrow.png')"
        elif self.theme == 'dark':
            self.theme_color_map['main_bg_color'] = "#292929"
            self.theme_color_map['highlight'] = "#CC99A0"
            self.theme_color_map['completed'] = "#21534B"
            self.theme_color_map['new'] = "#B973EB"
            self.theme_color_map['edit'] = "#58A1AB"
            self.theme_color_map['view'] = "#CCCCCC"
            self.theme_color_map['normal'] = "white"
            self.theme_color_map['btn_border'] = '1px solid #9E9E9E'
            self.theme_color_map['btn_border_pressed'] = "1px solid #EEEEEE"
            self.theme_color_map['btn_border_hover'] = '1px solid #CACACA'
            self.theme_color_map['hover'] = "#313131"
            self.theme_color_map['pressed'] = "#707070"
            self.theme_color_map['selection_bg'] = "#8087A8"
            self.theme_color_map['abstractvieww_bg'] = "#383B39"
            self.theme_color_map['label'] = "white"
            self.theme_color_map['drop_down_arrow_path'] = "url('./img/white_down_arrow.png')"
            self.theme_color_map['drop_up_arrow_path'] = "url('./img/white_up_arrow.png')"

        self.set_main_bg_color()

        return self.theme_color_map
    
    def set_main_bg_color(self):
        self.UI_manifester.setStyleSheet(f"background-color: {self.theme_color_map['main_bg_color']};")

    def create_btn(self, txt):
        
        '''
        通用的主界面按钮款式设置
        '''

        generated_btn = QPushButton(txt)
        generated_btn.setStyleSheet(f'''
            QPushButton {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.theme_color_map['hover']};
                border: {self.theme_color_map['btn_border_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme_color_map['pressed']};
                border: {self.theme_color_map['btn_border_pressed']};
            }}
        ''')

        return generated_btn
    
    def create_dialog_btn_box(self):
        
        '''
        通用的对话框选项按钮款式设置
        '''

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setStyleSheet(f"""
            QDialogButtonBox QPushButton {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 5px 15px;
            }}
            QDialogButtonBox QPushButton:hover {{
                background-color: {self.theme_color_map['hover']};
            }}
            QDialogButtonBox QPushButton:pressed {{
                background-color: {self.theme_color_map['pressed']};
            }}
        """)

        return buttons
    
    def create_filter_combo(self):
        filter_combo = QComboBox()
        filter_combo.setStyleSheet(f"""
            QComboBox {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QComboBox::drop-down {{
                border-left:{self.theme_color_map['btn_border']};
            }}
            QComboBox::down-arrow {{
                image: {self.theme_color_map['drop_down_arrow_path']};
                width: 12px;
                height: 12px;
            }}
            QComboBox:hover {{
                border-color: {self.theme_color_map['btn_border_hover']};
                background-color: {self.theme_color_map['hover']};
            }}
            QComboBox QListView {{
                selection-background-color: {self.theme_color_map['selection_bg']};
                background-color: {self.theme_color_map['abstractvieww_bg']};
                color: {self.theme_color_map['normal']};
                padding: 2px;
            }}
        """)

        return filter_combo
    
    def create_text_edit(self, txt):
        text_edit = QTextEdit()
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QTextEdit:focus {{
                border: {self.theme_color_map['btn_border_pressed']};
            }}
            QTextEdit:hover {{
                border: {self.theme_color_map['btn_border_hover']};
                background-color: {self.theme_color_map['hover']};
            }}
            QTextEdit[placeholderText]:not(:focus) {{
                color: {self.theme_color_map['hover']};
            }}
        """)

        text_edit.setPlaceholderText(txt)

        return text_edit
    
    def create_line_edit(self, txt):
        line_edit = QLineEdit()
        line_edit.setStyleSheet(f"""
            QLineEdit {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QLineEdit:focus {{
                border: {self.theme_color_map['btn_border_pressed']};
            }}
            QLineEdit:hover {{
                border: {self.theme_color_map['btn_border_hover']};
                background-color: {self.theme_color_map['hover']};
            }}
            QLineEdit[placeholderText]:not(:focus) {{
                color: {self.theme_color_map['hover']};
            }}
        """)

        line_edit.setPlaceholderText(txt)

        return line_edit
    
    def create_label(self, txt):
        label = QLabel(txt)
        label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme_color_map['label']};
            }}
        """)

        return label
    
    def create_spin_box(self, range_lower, range_upper, default_value):
        spin_box = QSpinBox()
        spin_box.setRange(range_lower, range_upper)
        spin_box.setValue(default_value)

        spin_box.setStyleSheet(f"""
            QSpinBox {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QSpinBox::focus {{
                border: {self.theme_color_map['btn_border_pressed']};
            }}
            QSpinBox::hover {{
                border: {self.theme_color_map['btn_border_hover']};
            }}
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 15px;
                background-color: {self.theme_color_map['main_bg_color']};
                border-left: {self.theme_color_map['btn_border']};
                border-top: {self.theme_color_map['btn_border']};
                border-bottom: {self.theme_color_map['btn_border']};
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 15px;
                background-color: {self.theme_color_map['main_bg_color']};
                border-left: {self.theme_color_map['btn_border']};
                border-top: {self.theme_color_map['btn_border']};
                border-bottom: {self.theme_color_map['btn_border']};
            }}
            QSpinBox::up-arrow {{
                image: {self.theme_color_map['drop_up_arrow_path']};
                width: 12px;
                height: 12px;
            }}
            QSpinBox::down-arrow {{
                image: {self.theme_color_map['drop_down_arrow_path']};
                width: 12px;
                height: 12px;
            }}
            QSpinBox::up-button:hover {{
                background-color: {self.theme_color_map['hover']};
            }}
            QSpinBox::down-button:hover {{
                background-color: {self.theme_color_map['hover']};
            }}
            QSpinBox::up-button:pressed {{
                background-color: {self.theme_color_map['pressed']};
            }}
            QSpinBox::down-button:pressed {{
                background-color: {self.theme_color_map['pressed']};
            }}
        """)

        return spin_box
    
    def create_checkbox(self, txt):
        checkbox = QCheckBox(txt)
        checkbox.setStyleSheet(f"""
            QCheckBox {{
                spacing: 5px;
                color: {self.theme_color_map['normal']};
                font-size: 15px;
            }}
        """)

        return checkbox
    
    def create_message_box(self):
        message_box = QMessageBox()
        message_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.theme_color_map['main_bg_color']};
            }}
            QMessageBox QLabel {{
                color: {self.theme_color_map['normal']};
                background-color: {self.theme_color_map['main_bg_color']};
            }}
            QMessageBox QPushButton {{
                color: {self.theme_color_map['normal']};
                background-color: {self.theme_color_map['main_bg_color']};
                border: {self.theme_color_map['btn_border']};
                padding: 5px 10px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {self.theme_color_map['hover']};
                border: {self.theme_color_map['btn_border_hover']};
            }}
            QMessageBox QPushButton:pressed {{
                background-color: {self.theme_color_map['pressed']};
                border: {self.theme_color_map['btn_border_pressed']};
            }}
        """)

        return message_box
    


    # ========================= Getters ==============================

    def get_button_style(self):
        return f'''
            QPushButton {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.theme_color_map['hover']};
                border: {self.theme_color_map['btn_border_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme_color_map['pressed']};
                border: {self.theme_color_map['btn_border_pressed']};
            }}
        '''
    
    def get_dialog_btn_box_style(self):
        return f'''
            QDialogButtonBox QPushButton {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 5px 15px;
            }}
            QDialogButtonBox QPushButton:hover {{
                background-color: {self.theme_color_map['hover']};
            }}
            QDialogButtonBox QPushButton:pressed {{
                background-color: {self.theme_color_map['pressed']};
            }}
        '''

    def get_line_edit_style(self):
        return f"""
            QLineEdit {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QLineEdit:focus {{
                border: {self.theme_color_map['btn_border_pressed']};
            }}
            QLineEdit:hover {{
                border: {self.theme_color_map['btn_border_hover']};
                background-color: {self.theme_color_map['hover']};
            }}
        """

    def get_text_edit_style(self):
        return f"""
            QTextEdit {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QTextEdit:focus {{
                border: {self.theme_color_map['btn_border_pressed']};
            }}
            QTextEdit:hover {{
                border: {self.theme_color_map['btn_border_hover']};
                background-color: {self.theme_color_map['hover']};
            }}
        """

    def get_combo_box_style(self):
        return f"""
            QComboBox {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QComboBox::drop-down {{
                border-left:{self.theme_color_map['btn_border']};
            }}
            QComboBox::down-arrow {{
                image: {self.theme_color_map['drop_down_arrow_path']};
                width: 12px;
                height: 12px;
            }}
            QComboBox:hover {{
                border-color: {self.theme_color_map['btn_border_hover']};
                background-color: {self.theme_color_map['hover']};
            }}
            QComboBox QListView {{
                selection-background-color: {self.theme_color_map['selection_bg']};
                background-color: {self.theme_color_map['abstractvieww_bg']};
                color: {self.theme_color_map['normal']};
                padding: 2px;
            }}
        """

    def get_spin_box_style(self):
        return f"""
            QSpinBox {{
                color: {self.theme_color_map['normal']};
                border: {self.theme_color_map['btn_border']};
                padding: 3px;
            }}
            QSpinBox::focus {{
                border: {self.theme_color_map['btn_border_pressed']};
            }}
            QSpinBox::hover {{
                border: {self.theme_color_map['btn_border_hover']};
            }}
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 15px;
                background-color: {self.theme_color_map['main_bg_color']};
                border-left: {self.theme_color_map['btn_border']};
                border-top: {self.theme_color_map['btn_border']};
                border-bottom: {self.theme_color_map['btn_border']};
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 15px;
                background-color: {self.theme_color_map['main_bg_color']};
                border-left: {self.theme_color_map['btn_border']};
                border-top: {self.theme_color_map['btn_border']};
                border-bottom: {self.theme_color_map['btn_border']};
            }}
            QSpinBox::up-arrow {{
                image: {self.theme_color_map['drop_up_arrow_path']};
                width: 12px;
                height: 12px;
            }}
            QSpinBox::down-arrow {{
                image: {self.theme_color_map['drop_down_arrow_path']};
                width: 12px;
                height: 12px;
            }}
            QSpinBox::up-button:hover {{
                background-color: {self.theme_color_map['hover']};
            }}
            QSpinBox::down-button:hover {{
                background-color: {self.theme_color_map['hover']};
            }}
            QSpinBox::up-button:pressed {{
                background-color: {self.theme_color_map['pressed']};
            }}
            QSpinBox::down-button:pressed {{
                background-color: {self.theme_color_map['pressed']};
            }}
        """

    def get_label_style(self):
        return f"""
            QLabel {{
                color: {self.theme_color_map['label']};
            }}
        """

    def get_list_widget_style(self):
        return f"""
            QListWidget {{
                background-color: {self.theme_color_map['abstractvieww_bg']};
                color: {self.theme_color_map['normal']};
            }}
            QListWidget::item:selected {{
                background-color: {self.theme_color_map['selection_bg']};
            }}
        """
    
    def get_checkbox_style(self):
        return f'''
            QCheckBox {{
                spacing: 5px;
                color: {self.theme_color_map['normal']};
                font-size: 15px;
            }}
        '''