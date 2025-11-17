import os
import string
import random
from utils.data_manager import DataManager

class UIDManager:
    def __init__(self, event_map, uid_file):
        if not os.path.exists(uid_file):
            with open(uid_file, 'w', encoding='utf-8') as f:
                f.write('')

        self.event_map = event_map
        self.uid_file = uid_file
        self.uid_set = self.convert_uid_file_to_set()
        #  self.uid_set = ('1', '2', '3', '4')

    def convert_uid_file_to_set(self):
        uid_set = set()
        with open(self.uid_file, 'r', encoding='utf-8') as f:
            data = f.readlines()
            for d in data:
                uid_set.add(d.strip())

        return uid_set

    def write_set_to_uid_file(self):
        with open(self.uid_file, 'w', encoding='utf-8') as f:
            for uid in self.uid_set:
                f.write(uid)
                f.write('\n')

    def add_new_uid_to_set(self, uid):
        self.uid_set.add(uid)

    def remove_uid_from_set(self, uid):
        if uid in self.uid_set:
            self.uid_set.remove(uid)

    def search_uid_in_set(self, data):

        if len(data) == 3:
            time, event, _ = data
        elif len(data) == 2:
            time, event = data
        else:
            return None

        for uid, (t, e, _) in self.event_map.items():
            if time == t and event == e:
                return uid
        return None

    def search_uid_in_event_map(self, uid):
        return uid in self.event_map.keys()

    def search_uid_in_uid_set(self, uid):
        return uid in self.uid_set

    def try_generate_uid(self, data):
        tentative_uid = self.search_uid_in_set(data)
        if not tentative_uid:
            random_uid = self._generate_random_uid(10)

            # 检查uid是否已经存在
            while self.search_uid_in_uid_set(random_uid):
                random_uid = self._generate_random_uid(10)

            self.add_new_uid_to_set(random_uid)
            return random_uid
        else:
            return tentative_uid

    def _generate_random_uid(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def update_uid(self):

        '''
        一般不会用到这个函数，假设一切架构合理的话
        '''

        for uid in self.uid_set:
            if not self.search_uid_in_event_map(uid):
                self.remove_uid_from_set(uid)


if __name__ == '__main__':
    data_manager = DataManager('data/data.txt')
    uid_manager = UIDManager(data_manager.event_map, 'data/uid.txt')
    uid_manager.try_generate_uid(('2026', 'dojw'))
    uid_manager.write_set_to_uid_file()

