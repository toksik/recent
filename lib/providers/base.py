class Provider:
    name = 'None'
    deps = []
    config_keys = []
    interval = 4
    def __init__(self, id, manager, config):
        self.id = id
        self.manager = manager
        self.config = config

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self):
        pass

    def _update(self):
        for dep in self.deps:
            if not self.manager.deps[dep].check():
                return False
        return self.update(self):
