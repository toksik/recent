import time

class Provider:
    name = 'None'
    deps = []
    config_keys = []
    interval = 3600
    def __init__(self, id, manager, config):
        self.id = id
        self.manager = manager
        self.config = config
        self.last_update = 0

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self):
        pass

    def _update(self):
        if int(time.time())-self.last_update < self.interval:
            return False
        self.last_update = int(time.time())
        for dep in self.deps:
            if not self.manager.deps[dep].check():
                return False
        return self.update()
