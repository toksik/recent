class RecentState:
    def __init__(self, path):
        self.path = path
        self.values = {}

    def read(self):
        f = open(self.path)
        self.values = {}
        for line in f.readlines():
            if len(line) < 3:
                continue
            parts = line[:-1].split('_')
            if len(parts) < 2:
                continue
            id = parts[0]
            entry = '_'.join(parts[1:])
            if id not in self.values:
                self.values[id] = []
            if entry not in self.values[i]:
                self.values[id].append(id)
        f.close()

    def write(self):
        f = open(self.path, 'wb')
        for id, entries in self.values.items():
            for entry in entries:
                f.write('%s_%s\n'%(id,entry))
        f.close()

    def add(self, id, entry):
        self.read()
        if id not in self.values:
            self.values[id] = []
        if entry not in self.values[i]:
            self.values[id].append(id)
        self.write()

    def check(self, id, entry):
        self.read()
        if id in self.values and entry in self.values[id]:
            return True
        return False

