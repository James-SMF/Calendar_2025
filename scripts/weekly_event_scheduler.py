class WeeklyEventScheduler:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.uid_manager = UIDManager(self.data_manager.event_map, 'data/uid.txt')

    def add_event(self, time, event, priority):
        data = (time, event, priority)
        uid = self.uid_manager.try_generate_uid(data)
        self.data_manager.event_map[uid] = data
        self.update_event()

    def search_event(self, time, event, priority):
        for uid, (t, e, p) in self.data_manager.event_map.items():
            if time == t and event == e and priority == p:
                return uid
        return None

    def remove_event(self, time, event, priority):
        pass

    def update_event(self):
        self.uid_manager.write_set_to_uid_file()
        self.data_manager.write_data()
