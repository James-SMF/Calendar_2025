

import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, 
    QMessageBox, QListWidgetItem, QAbstractItemView, QShortcut, QPushButton, 
    QLineEdit, QSpinBox, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEvent, QEasingCurve
from PyQt5.QtGui import QColor, QFont, QKeySequence
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from utils.time_formatter import TimeFormatter
from utils.event_content_manager import EventContentManager
from utils.theme_manager import ThemeManager
from utils.config_loader import ConfigLoader
from scripts.event_scheduler import EventScheduler
from scripts.ui_setting import SettingsDialog


class UIManifester(QWidget):
    def __init__(self, data_manager, event_len):
        # 初始化
        super().__init__()
        self.data_manager = data_manager
        self.event_scheduler = EventScheduler(self.data_manager)

        # ================= Settings =====================

        self.config = ConfigLoader().config
        self.theme = self.config['theme']
        self.keep_on_top = self.config['keep_on_top']
        self.event_reminder = self.config['event_reminder']

        # ================================================

        # ==================== UI =====================

        self.setWindowTitle("黄鼹鼠日历2025")
        self.setGeometry(700, 40, 700, 440)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.setDuration(300)


        # 主题管理
        self.theme_manager = ThemeManager(self.theme, self)
        self.theme_color_map = self.theme_manager.set_theme_color()

        self.dlg = SettingsDialog(self, self.config)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.left_layout = QVBoxLayout()

        # 左侧事件列表
        monospace_font = QFont("Noto Sans CJK SC", 14, QFont.Normal)
        monospace_font.setBold(True)

        self.event_list = QListWidget()
        self.event_list.setFont(monospace_font)
        self.event_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.event_list.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.event_list.setDragEnabled(False)
        self.event_list.setAcceptDrops(False)
        self.event_list.setDefaultDropAction(Qt.IgnoreAction)

        self.event_list.currentItemChanged.connect(self.show_event_detail)
        self.event_list.itemClicked.connect(self.show_event_detail)
        self.event_list.installEventFilter(self)
        self.left_layout.addWidget(self.event_list, 2)

        # 一键清理过期事件
        self.cleanup_outdated_btn = self.theme_manager.create_btn("一键清理过期事件")

        self.cleanup_outdated_btn.clicked.connect(self.cleanup_outdated_events)
        self.left_layout.addWidget(self.cleanup_outdated_btn)

        # 过滤下拉菜单
        self.filter_combo = self.theme_manager.create_filter_combo()
        self.filter_combo.addItems([
            "显示全部事件",
            "仅显示高优先级",
            "仅显示未完成事件",
            "仅显示未来事件"
        ])
        self.filter_combo.currentIndexChanged.connect(lambda: self.load_events(2))
        self.left_layout.addWidget(self.filter_combo)

        # 排序下拉菜单
        self.sort_combo = self.theme_manager.create_filter_combo()
        self.sort_combo.addItems([
            "按时间排序",
            "按优先级排序"
        ])
        self.sort_combo.currentIndexChanged.connect(lambda: self.load_events(2))
        self.left_layout.addWidget(self.sort_combo)

        main_layout.addLayout(self.left_layout, 2)

        # 右侧时间+事件+priority的输入窗口定义
        right_layout = QVBoxLayout()

        info_and_setting_layout = QHBoxLayout()
        self.mode_label = QLabel("当前模式: 新建")
        self.mode_label.setStyleSheet(f"color: {self.theme_color_map['new']}; font-weight: bold;")
        self.btn_settings = self.theme_manager.create_btn("⚙️ 设置")
        self.btn_settings.setFixedSize(70, 30)
        self.btn_settings.clicked.connect(self.open_settings)

        info_and_setting_layout.addWidget(self.mode_label)
        info_and_setting_layout.addWidget(self.btn_settings)

        self.time_input = self.theme_manager.create_line_edit('时间，如 2025-11-16 17:56')
        self.event_input = self.theme_manager.create_text_edit("事件描述")
        self.priority_input = self.theme_manager.create_spin_box(1, 10, 3)

        # 操作按钮
        btn_layout = QHBoxLayout()
        self.new_btn = self.theme_manager.create_btn("+")
        self.new_btn.setToolTip("新建事件")
        self.new_btn.setFixedWidth(36)

        self.save_btn = self.theme_manager.create_btn("保存")
        self.delete_btn = self.theme_manager.create_btn("删除事件")
        self.check_btn = self.theme_manager.create_btn("切换完成/未完成状态")

        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.check_btn)

        self.new_btn.clicked.connect(self.on_new)
        self.save_btn.clicked.connect(self.on_save)
        self.delete_btn.clicked.connect(self.on_delete)
        self.check_btn.clicked.connect(self.on_check)

        # 组装右侧功能
        right_layout.addLayout(info_and_setting_layout)
        right_layout.addWidget(self.theme_manager.create_label("时间"))
        right_layout.addWidget(self.time_input)
        right_layout.addWidget(self.theme_manager.create_label("事件"))
        right_layout.addWidget(self.event_input)
        right_layout.addWidget(self.theme_manager.create_label("优先级(1-10)"))
        right_layout.addWidget(self.priority_input)
        right_layout.addLayout(btn_layout)

        main_layout.addLayout(right_layout, 3)
        self.setLayout(main_layout)

        save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        save_shortcut.activated.connect(self.on_save)

        # ================================================

        # ================ Global Vars ===================

        self.creating = True
        self.current_uid = None
        self.timestr = None
        self.reminded_events = set()  # 记录已提醒过的事件 UID
        self.event_len = event_len
        self.remove_reminded_events = set()
        self.operation_lock = threading.Lock()

        self.load_events()
        self.on_new()

        # 定时器：每分钟检测一次
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_upcoming_events)
        self.timer.start(60 * 1000)  # 每60秒触发

        self.event_refresh_timer = QTimer(self)
        self.event_refresh_timer.timeout.connect(self.load_events)
        self.event_refresh_timer.start(100 * 1000)

        QApplication.instance().focusChanged.connect(self.on_focus_changed)


    def animate_opacity(self, target_opacity: float, duration: int = 300):
        """渐变动画修改窗口透明度（保留 anim 避免被回收）"""
        # 停掉正在运行的动画，防止冲突
        try:
            if getattr(self, "anim", None) is None:
                self.anim = QPropertyAnimation(self, b"windowOpacity")
                self.anim.setEasingCurve(QEasingCurve.InOutQuad)
            self.anim.stop()
        except Exception:
            pass

        self.anim.setDuration(duration)
        self.anim.setStartValue(self.windowOpacity())
        self.anim.setEndValue(target_opacity)
        self.anim.start()

    def changeEvent(self, event):
        """
        监听窗口激活状态变化：
        - QEvent.ActivationChange 在窗口被激活/失活时触发（更可靠于 focusInEvent）
        """
        if event.type() == QEvent.ActivationChange:
            if self.isActiveWindow():
                # 窗口变成活动窗口（获得焦点）
                self.animate_opacity(1.0)
            else:
                # 窗口失去活动状态
                self.animate_opacity(0.3)
        super().changeEvent(event)

    def cleanup_outdated_events(self):
        """一键清理过期事件"""
        now = datetime.now()
        events = self.event_scheduler.get_all()
        expired_uids = []

        for uid, (time_str, _, _, _) in events.items():
            event_time = TimeFormatter(time_str).parse_time()
            if event_time < now:  # 已过期
                expired_uids.append(uid)

        if not expired_uids:
            QMessageBox.information(self, "提示", "当前没有过期的事件。")
            return

        # 二次确认弹窗
        reply = QMessageBox.question(
            self,
            "确认清理",
            f"共检测到 {len(expired_uids)} 个过期事件，是否删除？\n\n此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for uid in expired_uids:
                try:
                    self.event_scheduler.delete(uid)
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"删除事件失败: {e}")
                    return

            self.load_events()
            QMessageBox.information(self, "完成", f"已清理 {len(expired_uids)} 个过期事件。")

    def on_new(self):

        """切换到新建模式，清空输入框"""

        with self.operation_lock:
            self.clear_inputs()
            self.creating = True

            # 取消列表选择，聚焦到时间输入（更直观）
            self.event_list.clearSelection()
            self.time_input.setFocus()
            self.save_btn.setText("新建保存")

            self.mode_label.setText("当前模式: 新建")
            self.mode_label.setStyleSheet(f"color: {self.theme_color_map['new']}; font-weight: bold;")

    def precheck_and_get_uid(self):
        """保存：根据当前模式执行 add 或 update"""
        time = self.time_input.text().strip()
        time_formatter = TimeFormatter(time)
        self.timestr = time_formatter.timestr

        if self.timestr is None or len(self.timestr) != 12:
            QMessageBox.warning(self, "错误", "时间格式不正确")
            return None

        event = self.event_input.toPlainText().strip()
        event_manager = EventContentManager(event)
        event_manager.newline_to_n()
        event = event_manager.event_str

        # 暴力但是天才的想法
        if len(event) < self.event_len:
            event = event + (' ' * 10)

        priority = int(self.priority_input.value())

        if not priority > 0 and priority < 10:
            QMessageBox.warning(self, "错误", "优先级应该在1到10之间")
            return None

        if not event:
            QMessageBox.warning(self, "错误", "事件不能为空")
            return None

        if self.creating:  # 新建
            uid = self.event_scheduler.add_event(self.timestr, event, priority)
        else:              # 更新
            uid = self.current_uid
            finished = self.event_scheduler.get_finished_status(uid)
            self.event_scheduler.update_event(uid, (self.timestr, event, priority, finished))

        return uid
    
    def on_focus_changed(self, old_widget, new_widget):
        input_widgets = []
        
        # 安全地收集输入框
        if hasattr(self, 'time_input') and self.time_input:
            input_widgets.append(self.time_input)
        if hasattr(self, 'event_input') and self.event_input:
            input_widgets.append(self.event_input)
        if hasattr(self, 'priority_input') and self.priority_input:
            input_widgets.append(self.priority_input) 

        if hasattr(self, 'creating') and self.creating:
            return

        if new_widget in input_widgets and old_widget == self.event_list:
            if hasattr(self, 'mode_label') and self.mode_label.text() != "当前模式: 编辑":
                self.switch_to_edit_mode()

    def switch_to_edit_mode(self):
        """切换到编辑模式"""
        # self.creating = False
        if hasattr(self, 'save_btn'):
            self.save_btn.setText("更新保存")
        if hasattr(self, 'mode_label'):
            self.mode_label.setText("当前模式: 编辑")
            self.mode_label.setStyleSheet(f"color: {self.theme_color_map['edit']}; font-weight: bold;")

    def on_save(self):
        with self.operation_lock:
            uid = self.precheck_and_get_uid()

            self.select_item_by_uid(uid)
            if uid:
                self.clear_inputs()
            self.creating = True
            self.save_btn.setText("新建保存")

            self.mode_label.setText("当前模式: 新建")
            self.mode_label.setStyleSheet(f"color: {self.theme_color_map['new']}; font-weight: bold;")

        self.load_events()

    def on_delete(self, preset_uid=None):
        current_row = self.event_list.currentRow()

        with self.operation_lock:
            if preset_uid is None or not preset_uid:
                selected_items = self.event_list.selectedItems()
                if not selected_items:
                    QMessageBox.warning(self, "提示", "请先选中要删除的事件")
                    return

                for item in selected_items:
                    uid = item.data(Qt.UserRole)
                    try:
                        self.event_scheduler.delete(uid)
                    except Exception as e:
                        QMessageBox.warning(self, "错误", f"删除失败: {e}")
                        return
            else:
                uid = preset_uid
                try:
                    self.event_scheduler.delete(uid)
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"删除失败: {e}")
                    return

            self.clear_inputs()
            self.creating = True
            self.save_btn.setText("新建保存")

            self.mode_label.setText("当前模式: 新建")
            self.mode_label.setStyleSheet(f"color: {self.theme_color_map['new']}; font-weight: bold;")

        self.load_events()

        if current_row >= self.event_list.count():
            current_row = self.event_list.count() - 1

        self.event_list.setCurrentRow(current_row)
        self.event_list.scrollToItem(self.event_list.item(current_row))
        item = self.event_list.item(current_row)
        if item:
            self.show_event_detail(item, prev='keep_mode')

    def on_check(self):
        with self.operation_lock:
            selected_items = self.event_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "提示", "请先选中要标记完成/未完成的事件")
                return
            
            selected_uids = []
            for item in selected_items:
                uid = item.data(Qt.UserRole)
                selected_uids.append(uid)
                try:
                    finished_status = int(self.event_scheduler.get_finished_status(uid))
                    self.event_scheduler.set_finished_status(uid, int(not finished_status))
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"标记失败: {e}")
                    return

        self.load_events()
        self.restore_selection(selected_uids)     # 恢复刚刚选中的焦点

    
    def restore_selection(self, selected_uids):
        if not selected_uids:
            return

        for i in range(self.event_list.count()):
            item = self.event_list.item(i)

            if item.data(Qt.UserRole) in selected_uids:
                item.setSelected(True)

                if len(selected_uids) == 1:
                    self.event_list.setCurrentItem(item)
                    self.event_list.scrollToItem(item)

                break

    def sort_eventlist(self, sort_key=0):
        self.event_list.clear()
        events = self.event_scheduler.get_all()
        event_list = []

        for uid, (time, event, priority, finished) in events.items():
            event_list.append((time, uid, event, priority, finished))

        event_list.sort(key=lambda x: int(x[sort_key]))
        return event_list

    def load_events(self, filter_priority=2):
        with self.operation_lock:
            # 0 = 按时间, 1 = 按优先级
            sort_mode = self.sort_combo.currentIndex() if hasattr(self, "sort_combo") else 0
            event_list = self.sort_eventlist(sort_key=0 if sort_mode == 0 else 3)

            for time, uid, event, priority, finished in event_list:
                if hasattr(self, "filter_combo") and self.filter_combo.currentIndex() != 0:
                    filter_mode = self.filter_combo.currentIndex()
                    if filter_mode == 1 and int(priority) > filter_priority:
                        continue
                    elif filter_mode == 2 and int(finished) == 1:
                        continue
                    elif filter_mode == 3:
                        now = datetime.now()
                        event_time = TimeFormatter(time).parse_time()
                        if event_time < now:
                            continue

                # if len(event) > 10:
                #     event = event[:self.event_len] + "..."

                display_time = f'{time[-8:-6]}-{time[-6:-4]} {time[-4:-2]}:{time[-2:]}'
                display_event = event.replace("\\n", " ")
                display_text = f"{display_time}   {display_event[:self.event_len]}"
                item = QListWidgetItem(display_text)

                # 隐藏uid
                item.setData(Qt.UserRole, uid)

                if int(priority) <= 2:
                    item.setForeground(QColor(self.theme_color_map['highlight']))
                else:
                    item.setForeground(QColor(self.theme_color_map['normal']))

                if int(finished) == 1:
                    item.setBackground(QColor(self.theme_color_map['completed']))

                self.event_list.addItem(item)

            item_to_remove_from_reminded_event = set()
            for (uid, timestr) in self.reminded_events:
                now = datetime.now()
                event_time = TimeFormatter(timestr).parse_time()
                if event_time < now:
                    item_to_remove_from_reminded_event.add((uid, timestr))

            for (uid, timestr) in item_to_remove_from_reminded_event:
                self.reminded_events.remove((uid, timestr))

    def show_event_detail(self, item, prev=None):

        '''
        点击列表中某个事件，显示事件详情
        '''

        if item is None:
            return

        uid = item.data(Qt.UserRole)

        try:
            time, event, priority, _ = self.event_scheduler.get(uid)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"读取事件失败: {e}")
            return

        event_manager = EventContentManager(event)
        event_manager.n_to_newline()
        event_manager.cleanup_str()
        event = event_manager.event_str

        time_formatter = TimeFormatter(time)
        time = time_formatter.format_time()
        self.time_input.setText(time)
        self.event_input.setText(event)
        self.priority_input.setValue(int(priority))
        self.current_uid = uid
        self.creating = False
        self.save_btn.setText("更新保存")

        if prev is None:
            self.mode_label.setText("当前模式: 编辑")
            self.mode_label.setStyleSheet(f"color: {self.theme_color_map['edit']}; font-weight: bold;")
        else:
            self.mode_label.setText("当前模式: 预览")
            self.mode_label.setStyleSheet(f"color: {self.theme_color_map['view']}; font-weight: bold;")

    def clear_inputs(self):

        """清空输入框并重置状态"""

        self.time_input.clear()
        self.event_input.clear()
        self.priority_input.setValue(3)
        self.current_uid = None
        self.creating = True
        self.event_list.clearSelection()


    def select_item_by_uid(self, uid):
        """在列表中选中指定 uid 的项（如果存在）"""
        for i in range(self.event_list.count()):
            item = self.event_list.item(i)
            if item.data(Qt.UserRole) == uid:
                self.event_list.setCurrentItem(item)
                return

    def check_upcoming_events(self):
        if self.event_reminder == False:
            return

        now = datetime.now()
        events = self.event_scheduler.get_all()

        for uid, (time_str, event, priority, finished) in events.items():
            time_formatter = TimeFormatter(time_str)
            event_time = time_formatter.parse_time()

            if (uid, time_str) in self.reminded_events or int(finished) == 1:
                continue

            delta = event_time - now
            if timedelta(minutes=1) <= delta <= timedelta(minutes=15):
                self.reminded_events.add((uid, time_str))  # 标记已提醒
                self.show_event_reminder(uid, event_time, event, priority, finished)

        # 不能直接删除字典里的项，所以需要先记录，后删除
        for uid in self.remove_reminded_events:
            self.on_delete(uid)

        self.remove_reminded_events.clear()


    def show_event_reminder(self, uid, event_time, event, priority, finished):
        msg = self.theme_manager.create_message_box()
        msg.setWindowTitle("事件提醒")
        msg.setText(
            f"事件即将开始：\n\n"
            f"{event_time.strftime('%Y-%m-%d %H:%M')}\n{event}\n\n"
            f"将在 15 分钟后开始。"
        )

        confirm_btn = msg.addButton("确认", QMessageBox.AcceptRole)
        delay_btn = msg.addButton("延后一小时", QMessageBox.ActionRole)
        delete_btn = msg.addButton("删除事件", QMessageBox.RejectRole)

        msg.exec_()

        if msg.clickedButton() == confirm_btn:
            return  # 不做操作
        elif msg.clickedButton() == delay_btn:
            new_time = datetime.now() + timedelta(hours=1)
            new_time_str = new_time.strftime("%Y%m%d%H%M")

            # 更新数据库里的事件（和 reminded_events 里的事件是独立的，没啥关系）
            self.event_scheduler.update_event(uid, (new_time_str, event, priority, finished))
            self.load_events()

            # 仅 match uid 即可，不需要管时间
            self.reminded_events = set((a, b) for (a, b) in self.reminded_events if a != uid)

        elif msg.clickedButton() == delete_btn:
            self.remove_reminded_events.add(uid)
            self.reminded_events.remove((uid, event_time.strftime("%Y%m%d%H%M")))


    def eventFilter(self, source, event):
        """事件过滤器：捕获 QListWidget 的按键事件"""
        if source == self.event_list and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Space:
                self.on_check()
                return True  # 阻止事件继续传播
            elif event.key() == Qt.Key_N:  
                self.on_new()
                return True
            elif event.key() == Qt.Key_W:
                self.move_selection_up()
                return True
            elif event.key() == Qt.Key_S:
                self.move_selection_down()
                return True
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.time_input.setFocus()
                self.creating = False
                self.save_btn.setText("更新保存")
                self.mode_label.setText("当前模式: 编辑")
                self.mode_label.setStyleSheet(f"color: {self.theme_color_map['edit']}; font-weight: bold;")
                return True
            elif event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
                self.on_delete()
                return True
    
        # 对于其他事件，调用父类处理
        return super().eventFilter(source, event)
    

    def move_selection_up(self):
        current_row = self.event_list.currentRow()
        if current_row > 0:
            new_row = current_row - 1
            self.event_list.setCurrentRow(new_row)
            self.event_list.scrollToItem(self.event_list.item(new_row))
            item = self.event_list.item(new_row)
            if item:
                self.show_event_detail(item, prev='keep_mode')

    def move_selection_down(self):
        current_row = self.event_list.currentRow()
        if current_row < self.event_list.count() - 1:
            new_row = current_row + 1
            self.event_list.setCurrentRow(new_row)
            self.event_list.scrollToItem(self.event_list.item(new_row))
            item = self.event_list.item(new_row)
            if item:
                self.show_event_detail(item, prev='keep_mode')


    def keyPressEvent(self, event):
        if self.time_input.hasFocus() or self.event_input.hasFocus() or self.priority_input.hasFocus():
            if event.key() == Qt.Key_Escape:
                self.event_list.setFocus()   # 焦点回到左侧列表
                self.mode_label.setText("当前模式: 预览")
                self.mode_label.setStyleSheet(f"color: {self.theme_color_map['view']}; font-weight: bold;")

        super().keyPressEvent(event)


    def open_settings(self):
        if self.dlg.exec_():
            settings = self.dlg.get_settings()
            self.keep_on_top = settings["keep_on_top"]
            self.event_reminder = settings['event_reminder']
            self.theme = settings['theme']
            self.theme_manager.theme = self.theme
            self.apply_keep_on_top()
            self.apply_event_reminder()
            self.apply_theme()

    def apply_keep_on_top(self):
        """根据设置应用窗口是否置顶"""
        print('apply_keep_on_top', self.keep_on_top)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.keep_on_top)
        self.show()  # 重新显示以应用 flag

    def apply_event_reminder(self):
        if self.event_reminder:
            self.timer.start(60 * 1000)
        else:
            self.timer.stop()

    def apply_theme(self):
        """安全地应用主题变更"""
        # 更新主题管理器
        self.theme_manager.theme = self.theme
        self.theme_color_map = self.theme_manager.set_theme_color()
        
        # 更新主窗口样式
        if self.theme == 'dark':
            self.setStyleSheet(f"background-color: {self.theme_color_map['main_bg_color']};")
        else:
            self.setStyleSheet("")  # 重置为默认样式
        
        # 更新所有UI组件样式
        self.update_ui_styles()
        
        # 保持当前状态
        self.load_events()  # 重新加载事件以更新颜色

    def update_ui_styles(self):
        """更新所有UI组件的样式"""
        # 更新按钮样式
        for btn in [self.cleanup_outdated_btn, self.new_btn, self.save_btn, 
                    self.delete_btn, self.check_btn, self.btn_settings]:
            btn.setStyleSheet(self.theme_manager.get_button_style())
        
        # 更新输入框样式
        self.time_input.setStyleSheet(self.theme_manager.get_line_edit_style())
        self.event_input.setStyleSheet(self.theme_manager.get_text_edit_style())
        self.priority_input.setStyleSheet(self.theme_manager.get_spin_box_style())
        
        # 更新下拉菜单样式
        self.filter_combo.setStyleSheet(self.theme_manager.get_combo_box_style())
        self.sort_combo.setStyleSheet(self.theme_manager.get_combo_box_style())
        
        # 更新标签样式
        for label in self.findChildren(QLabel):
            if label not in [self.mode_label]:  # 特殊标签单独处理
                label.setStyleSheet(self.theme_manager.get_label_style())
        
        # 更新特殊标签
        self.update_mode_label_style()
        
        # 更新列表样式
        self.event_list.setStyleSheet(self.theme_manager.get_list_widget_style())


    def update_mode_label_style(self):
        """更新模式标签的特殊样式"""
        if self.creating:
            color = self.theme_color_map['new']
        elif self.event_list.currentItem() is not None:
            color = self.theme_color_map['edit']
        else:
            color = self.theme_color_map['view']
        
        self.mode_label.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    manager = DataManager('data/data.txt')
    window = UIManifester(manager, 10)
    window.show()
    sys.exit(app.exec_())
