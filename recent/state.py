class RecentState:
    '''Class that maintains a file for marking news posts as old'''
    def __init__(self, path):
        '''\
Returns a new RecentState instance the uses the given <path>

  path -> the path of the state file

It will be read on deamand.'''
        self.path = path
        self.values = {}

    def read(self):
        '''Read the state file and store all ids in self.values'''
        f = open(self.path, 'rb')
        self.values = {}
        for line in f.readlines():
            if len(line) < 3:
                continue
            parts = line[:-1].split(b'_')
            if len(parts) < 2:
                continue
            id = parts[0].decode('utf-8')
            entry = b'_'.join(parts[1:])
            entry = entry.decode('utf-8')
            if id not in self.values:
                self.values[id] = []
            if entry not in self.values[id]:
                self.values[id].append(entry)
        f.close()

    def write(self):
        '''Write all ids in self.values to the file'''
        f = open(self.path, 'wb')
        for id, entries in self.values.items():
            for entry in entries:
                text = '%s_%s\n'%(id,entry)
                f.write(text.encode('utf-8'))
        f.close()

    def add(self, id, entry):
        '''\
Mark a id as old

  id -> the provider\'s id
  entry -> the post\'s id

The file will be parsed before to ensure consistency'''
        id = id.replace('_', '-')
        self.read()
        if id not in self.values:
            self.values[id] = []
        if entry not in self.values[id]:
            self.values[id].append(entry)
        self.write()

    def check(self, id, entry):
        '''\
Indicates whether the id is marked as old

  id -> the provider\'s id
  entry -> the post\'s id

The file is parsed each time check() is called.'''
        id = id.replace('_', '-')
        self.read()
        if id in self.values and entry in self.values[id]:
            return True
        return False

