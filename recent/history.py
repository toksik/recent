from recent.manager import Notification

class RecentLog:
    '''\
The RecentLog class parses and writes history files.

They are used to store the news posts persistently, so that they can be
read later (e.g. by the recent util).'''
    def __init__(self, path):
        '''\
Creates a new RecentLog instance

  path -> the path of the log/history file

The file will be read on demand. After calling read() all
entries in the file can be found in the self.entries property. They
are stored as lib.manager.Notification instances.'''
        self.path = path
        self.entries = []

    def read(self):
        '''Parse the log file and populate self.entries'''
        f = open(self.path, 'rb')
        self.entries = []
        mode = 0
        provider = b''
        author = b''
        title = b''
        link = b''
        body = b''
        tags = []
        for line in f.readlines():
            if mode == 0:
                if b'[' not in line and b']' not in line:
                    continue
                provider = line[1:line.find(b']')]
                if b']:' in line:
                    author = None
                else:
                    author = line[line.find(b']')+2:line.find(b':',
                                  line.find(b']'))]
                title = line[line.find(b':',line.find(b']'))+2:-1]
                link = b''
                body = b''
                tags = []
                mode = 1
            elif mode == 1:
                if line.startswith(b'  '):
                    link = b''
                    body = line[2:]
                    mode = 2
                elif line.startswith(b'<'):
                    link = b''
                    body = b''
                    tags = line[1:line.find(b'>')].split(b' ')
                    id = line[line.find(b'>')+2:-1]
                    self.entries.append(Notification(provider, title, id,
                                        author, link, body, tags))
                    mode = 0
                else:
                    link = line[:-1]
                    mode = 2
            elif mode == 2:
                if line.startswith(b'  '):
                    body = body + line[2:]
                elif line.startswith(b'<'):
                    tags = line[1:line.find(b'>')].split(b' ')
                    id = line[line.find(b'>')+2:-1]
                    body = body.strip() # A dirty fix for newline problems
                    self.entries.append(Notification(provider, title, id,
                                        author, link, body, tags))
                    mode = 0
        f.close()

    def write(self):
        '''\
Write all objects in self.entries to the log file

If there are more than 200 entries the oldest are ignored.'''
        f = open(self.path, 'wb')
        if len(self.entries) > 200:
            self.entries = self.entries[len(self.entries)-200:]
        for item in self.entries:
            if item.author:
                text = '[%s] %s: %s\n'%(item.provider, item.author, item.title)
                f.write(text.encode('utf-8'))
            else:
                text = '[%s]: %s\n'%(item.provider, item.title)
                f.write(text.encode('utf-8'))
            if item.link:
                text = item.link+'\n'
                f.write(text.encode('utf-8'))
            if item.body:
                for line in item.body.split('\n'):
                    text = '  '+line+'\n'
                    f.write(text.encode('utf-8'))
            text = '<'+' '.join(item.tags)+'> %s\n'%item.id
            f.write(text.encode('utf-8'))
        f.close()

    def add(self, item):
        '''\
Add a post to the file

  item -> a Notification instance

The file will be read before adding the item and written instantly'''
        self.read()
        self.entries.append(item)
        self.write()
