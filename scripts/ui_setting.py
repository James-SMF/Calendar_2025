from PyQt5.QtWidgets import (
    QVBoxLayout, QDialog, QApplication, QWidget
)
import os

class SettingsDialog(QDialog):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.resize(300, 200)
        self.parent = parent

        self.keep_on_top = config["keep_on_top"]
        self.event_reminder = config["event_reminder"]
        self.theme = config["theme"]
        self.original_theme = self.theme

        if hasattr(parent, 'theme_manager'):
            self.theme = parent.theme_manager.theme
            self.original_theme = self.theme

        self.theme_manager = parent.theme_manager
        self.theme_color_map = self.theme_manager.set_theme_color()

        layout = QVBoxLayout()

        # 设置项 1：保持悬浮
        self.chk_keep_on_top = self.theme_manager.create_checkbox("保持悬浮")
        self.chk_keep_on_top.setChecked(self.keep_on_top)
        layout.addWidget(self.chk_keep_on_top)
        
        # 设置项 2：事件提醒
        self.chk_event_reminder = self.theme_manager.create_checkbox("事件提醒")
        self.chk_event_reminder.setChecked(self.event_reminder)
        layout.addWidget(self.chk_event_reminder)
        layout.addSpacing(50)

        # 设置项 3：主题
        self.theme_label = self.theme_manager.create_label("色彩主题")
        layout.addWidget(self.theme_label)

        self.theme_combo_box = self.theme_manager.create_filter_combo()
        self.theme_combo_box.addItems(['light', 'dark'])
        self.theme_combo_box.setCurrentText(self.theme)  # 使用当前主题
        self.theme_combo_box.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo_box)

        # 底部按钮（确定/取消）
        self.buttons = self.theme_manager.create_dialog_btn_box()
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)
        self.apply_theme(initial=True)

    def reject(self):
        """Cancel时恢复原始主题"""
        if self.theme != self.original_theme:
            self.theme = self.original_theme
            self.parent.theme_manager.theme = self.original_theme
            self.parent.apply_theme()  # 强制父窗口同步
            self.apply_theme()
        super().reject()

    def on_theme_changed(self, new_theme):
        """主题下拉框变化时立即预览效果"""
        self.theme = new_theme
        self.parent.theme_manager.theme = new_theme
        self.apply_theme()

        if hasattr(self, 'parent') and hasattr(self.parent, 'theme_manager'):
            self.parent.theme_manager.set_theme_color()
            # self.parent.apply_theme()

    def apply_theme(self, initial=False):
        """安全应用主题样式"""
        # 完全清除所有现有样式
        self.setStyleSheet("")
        QApplication.instance().setStyleSheet("")

        # 更新主题管理器
        current_theme = self.parent.theme_manager.theme if hasattr(self, 'parent') else self.theme
        self.theme_manager.theme = current_theme
        self.theme_color_map = self.theme_manager.set_theme_color()

        # 更新所有控件的样式
        self.update_widget_styles()
        
        # 应用基础背景色
        base_style = f"""
            QDialog {{
                background-color: {self.theme_color_map['main_bg_color']};
            }}
        """
        self.setStyleSheet(base_style)
        
        # 非首次应用时强制刷新
        if not initial:
            self.repaint()
            QApplication.processEvents()

    def update_widget_styles(self):
        """彻底更新所有控件的样式"""
        # 先清除所有子控件的样式
        for child in self.findChildren(QWidget):
            child.setStyleSheet("")
            child.style().unpolish(child)
            child.style().polish(child)
            child.update()
        
        # 重新应用样式
        checkbox_style = self.theme_manager.get_checkbox_style()
        for checkbox in [self.chk_keep_on_top, self.chk_event_reminder]:
            checkbox.setStyleSheet(checkbox_style)
        
        self.theme_label.setStyleSheet(self.theme_manager.get_label_style())
        self.theme_combo_box.setStyleSheet(self.theme_manager.get_combo_box_style())
        self.buttons.setStyleSheet(self.theme_manager.get_dialog_btn_box_style())

    def get_settings(self):
        settings = {
            "keep_on_top": self.chk_keep_on_top.isChecked(),
            "event_reminder": self.chk_event_reminder.isChecked(),
            "theme": self.theme_combo_box.currentText()
        }
        
        # 保存设置
        with open('./data/settings.config', 'w', encoding='utf-8') as f:
            f.write(str(settings['keep_on_top']) + '\n')
            f.write(str(settings['event_reminder']) + '\n')
            f.write(settings['theme'] + '\n')
        
        return settings