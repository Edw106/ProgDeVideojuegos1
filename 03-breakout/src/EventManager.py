class EventManager:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def register_to(self, observable):
        observable.register(self)

    def unregister_from(self, observable):
        observable.unregister(self)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event, *args, **kwargs):
        for observer in list(self.observers):
            observer.on_event(event, *args, **kwargs)

    def on_event(self, event, *args, **kwargs):
        pass