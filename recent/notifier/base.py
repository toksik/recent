class Notifier:
    id = 'none'
    deps = []
    config_keys = []
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

    def notify(self, obj):
        pass

    def _notify(self, obj):
        for dep in self.deps:
            if not self.manager.deps[dep].check():
                return False
        return self.notify(obj)
