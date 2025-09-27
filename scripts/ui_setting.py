from PyQt5.QtWidgets import (
    QVBoxLayout, QDialog, QCheckBox, QDialogButtonBox
)

class SettingsDialog(QDialog):
    def __init__(self, parent=None, keep_on_top=True, event_reminder=True):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.resize(300, 200)
        self.keep_on_top = keep_on_top
        self.event_reminder = event_reminder

        layout = QVBoxLayout()

        # 设置项 1：保持悬浮
        self.chk_keep_on_top = QCheckBox("保持悬浮在顶层")
        self.chk_keep_on_top.setChecked(self.keep_on_top)
        layout.addWidget(self.chk_keep_on_top)

        self.chk_event_reminder = QCheckBox("事件提醒")
        self.chk_event_reminder.setChecked(self.event_reminder)
        layout.addWidget(self.chk_event_reminder)

        # 底部按钮（确定/取消）
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_settings(self):
        return {
            "keep_on_top": self.chk_keep_on_top.isChecked(),
            "event_reminder": self.chk_event_reminder.isChecked()
        }
    
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        settings = dialog.get_settings()
        print(settings)
    sys.exit(app.exec_())