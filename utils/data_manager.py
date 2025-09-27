import os

class DataManager:
    def __init__(self, data_file):
        if not os.path.exists(data_file):
            with open(data_file, 'w') as f:
                f.write('')

        self.data_file = data_file
        self.event_map = self.read_data()

    def read_data(self) -> dict:

        updated_event_map = dict()

        with open(self.data_file, 'r') as f:
            data = f.readlines()
            for d in data:
                if d.strip() == '':
                    continue
                uid, time, event, priority, finished = self._parse_data(d)
                updated_event_map[uid] = (time, event, priority, finished)

        return updated_event_map

    @property
    def all_events(self) -> list:
        return self.event_map.values()

    def write_data(self) -> None:

        '''
        注意先读文件再写，要不然有空数据覆盖的风险
        '''

        with open(self.data_file, 'w') as f:
            for uid, (time, event, priority, finished) in self.event_map.items():
                data = f'{uid};;++{time};;++{event};;++{priority};;++{finished}\n'
                f.write(data)

    def _parse_data(self, data):
        return data.strip().split(';;++')

    def get(self, uid, default=None):
        return self.event_map.get(uid, default)

    def set(self, uid, data):
        self.event_map[uid] = data

if __name__ == '__main__':
    data_manager = DataManager('data/data.txt')
    event_map = {'1': ('2025', 'fjowejfi', '1'), '2': ('2026', 'dojw', '1'), '3': ('2027', 'woqj', '2'), '4': ('2028', 'fjowejfi', '3')}
    print(data_manager.event_map)
    data_manager.read_data()
    print(data_manager.event_map)
    data_manager.write_data()
