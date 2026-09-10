class EventManager:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event):
        for observer in list(self.observers):
            observer.on_event(event)

    def on_event(self, event):
        pass