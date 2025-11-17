class EventContentManager:

    def __init__(self, event_str):
        self.event_str = event_str

    def newline_to_n(self):
        self.event_str = self.event_str.replace('\n', '\\n')

    def n_to_newline(self):
        self.event_str = self.event_str.replace('\\n', '\n')

    @property
    def event_len(self):
        return len(self.event_str)
