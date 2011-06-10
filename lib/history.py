from lib.manager import Notification

class RecentLog:
    def __init__(self, path):
        self.path = path
        self.entries = []

    def read(self):
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
                    self.entries.append(Notification(provider, title, id,
                                        author, link, body, tags))
                    mode = 0
        f.close()

    def write(self):
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
        print(item.body.strip().encode('utf-8'))
        self.read()
        self.entries.append(item)
        self.write()
