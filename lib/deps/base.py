import time

class Dependency:
    id = 'none'
    deps = []
    interval = 60
    def __init__(self, manager):
        self.manager = manager
        self.last_check = 0
        self.last_resp = False

    def check(self):
        return False

    def _check(self):
        if int(time.time)-self.last_check < self.interval:
            return 
        for dep in self.deps:
            if not self.manager.deps[dep].check():
                self.last_resp = False
                return False
        self.last_resp = self.check()
        return self.last_resp
