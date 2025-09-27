# 本地测试语法：在根目录跑 py -m scripts.event_scheduler

from utils.data_manager import DataManager
from utils.uid_manager import UIDManager

class EventScheduler:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.uid_manager = UIDManager(self.data_manager.event_map, 'data/uid.txt')

    def add_event(self, time, event, priority, finished=0):
        data = (time, event, priority, finished)
        uid = self.uid_manager.try_generate_uid(data)
        self.data_manager.event_map[uid] = data
        self.uid_manager.write_set_to_uid_file()
        self.data_manager.write_data()
        return uid

    def search_event(self, time, event, priority):
        for uid, (t, e, p, _) in self.data_manager.event_map.items():
            if time == t and event == e and priority == p:
                return uid
        return None

    def get(self, uid):
        return self.data_manager.get(uid, None)

    def delete(self, uid):

        event = self.data_manager.get(uid, None)

        if event:
            self.data_manager.event_map.pop(uid)
            self.data_manager.write_data()
            self.uid_manager.remove_uid_from_set(uid)
            self.uid_manager.write_set_to_uid_file()

    def update_event(self, uid, data):
        self.data_manager.set(uid, data)
        self.data_manager.write_data()
        self.uid_manager.add_new_uid_to_set(uid)
        self.uid_manager.write_set_to_uid_file()

    def query_all_events(self):
        return list(self.data_manager.all_events)

    def get_all(self):
        return self.data_manager.event_map
    
    def set_finished_status(self, uid, finished):
        self.data_manager.set(uid, (self.data_manager.get(uid)[0], self.data_manager.get(uid)[1], self.data_manager.get(uid)[2], finished))
        self.data_manager.write_data()

    def get_finished_status(self, uid):
        return self.data_manager.get(uid)[3]

if __name__ == '__main__':
    data_manager = DataManager('data/data.txt')
    event_scheduler = EventScheduler(data_manager)
    event_scheduler.add_event('2023', 'ffwojwejfi', '1')
    print(event_scheduler.query_all_events())

