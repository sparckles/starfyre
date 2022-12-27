
# store shall also be a global variable
class Store:
    def __init__(self):
        self.store = {}
        # every store is a dict
        # that will contain the key to value
        # key is the a randomly generated string
        # value is the data
        # then we have a list of observers
        # for every key
        self.observers = {}

    def add_observer(self, key, observer):
        if key not in self.observers:
            self.observers[key] = []
        self.observers[key].add(observer)

    def remove_observer(self, key, observer):
        if key in self.observers:
            self.observers[key].remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def set_data(self, key, initial_data):
        self.store[id] = initial_data
        self.notify_observers()

    def get_data(self, key, component, default=None):
        self.add_observer(key, component)
        return self.store.get(key, default)
