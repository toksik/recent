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
        self.active = False

    def activate(self):
        pass

    def _activate(self):
        if self.active:
            return
        for dep in self.deps:
            if not self.manager.deps[dep].check():
                return
        self.active = True
        self.activate()

    def deactivate(self):
        pass

    def _deactivate(self):
        if not self.active:
            return
        self.active = False
        self.deactivate()

    def update(self):
        pass

    def _update(self):
        if int(time.time())-self.last_update < self.interval:
            return False
        self.last_update = int(time.time())
        for dep in self.deps:
            if not self.manager.deps[dep].check():
                self._deactivate()
                return False
        self._activate()
        return self.update()
