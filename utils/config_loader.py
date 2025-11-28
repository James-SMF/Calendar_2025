import os

class ConfigLoader:
    def __init__(self, config_file='./data/settings.config'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        # 确保设置文件存在
        if not os.path.exists(self.config_file):
            os.makedirs('./data', exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write('True\nTrue\n' + self.theme)

        config_dict = {
            "keep_on_top": True,
            "event_reminder": True,
            "theme": "dark"
        }
        
        # 读取设置（但主题以父窗口为准）
        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = f.readlines()
            config_dict["keep_on_top"] = data[0].strip() == 'True'
            config_dict["event_reminder"] = data[1].strip() == 'True'
            config_dict["theme"] = data[2].strip()

        return config_dict