import time
import threading
import signal

import lib.providers
import lib.deps
import lib.notifier

INTERVAL = {'instant':0, 'minute':60, 'halfhour':1800, 'hour':36000,
            'halfday':43200, 'day':86400}

class Notification:
    def __init__(self, provider, title, id, author=None, link=None, body=None,
                 tags=None):
        self.provider = provider
        if not isinstance(self.provider, str):
            self.provider = self.provider.decode('utf-8')
        self.title = title
        if not isinstance(self.title, str):
            self.title = self.title.decode('utf-8')
        if not author:
            author = ''
        self.author = author
        if not isinstance(self.author, str):
            self.author = self.author.decode('utf-8')
        if not link:
            link = ''
        self.link = link
        if not isinstance(self.link, str):
            self.link = self.link.decode('utf-8')
        if not body:
            body = ''
        self.body = body
        if not isinstance(self.body, str):
            self.body = self.body.decode('utf-8')
        self.id = id
        if not isinstance(self.id, str):
            self.id = self.id.decode('utf-8')
        if not tags:
            tags = ['new', 'unread']
        self.tags = []
        for tag in tags:
            if not isinstance(tag, str):
                self.tags.append(tag.decode('utf-8'))
            else:
                self.tags.append(tag)        

class Manager:
    def __init__(self, config, state, log):
        self.lock = threading.Lock()
        self.providers = {}
        self.deps = {}
        self.notifiers = []
        self.active = []
        self.config = config
        self.state = state
        self.log = log
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)

    def terminate(self, *args):
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        for provider in self.active:
            provider._deactivate()
        exit(0)

    def get_new_deps(self, dep_list):
        deps = {}
        for dep in dep_list:
            if dep in deps or dep in self.deps:
                continue
            dep_cls = lib.deps.get_class(dep)
            if not dep_cls:
                return 
            deps[dep] = dep_cls
        while True:
            new_deps = {}
            for item in deps.values():
                for dep in item.deps:
                    if dep in new_deps or dep in deps or dep in self.deps:
                        continue
                    dep_cls = lib.deps.get_class(dep)
                    if not dep_cls:
                        return
                    new_deps[dep] = dep_cls
            if not new_deps:
                break
            for dep, dep_cls in new_deps.items():
                deps[dep] = dep_cls
        return deps

    def load_providers(self):
        for id in self.config.index():
            type = self.config.get(id, 'type')
            cls = lib.providers.get_class(type)
            if not cls:
                continue
            config = {}
            for key in cls.config_keys:
                config[key] = self.config.get(id, key, '')
            deps = self.get_new_deps(cls.deps)
            if deps == None:
                continue
            for dep, dep_cls in deps.items():
                self.deps[dep] = dep_cls(self)
            self.providers[id] = cls(id, self, config)
            interval = self.config.get(id, 'interval')
            if interval:
                if interval.isnumeric():
                    self.providers[id].interval = int(interval)
                elif interval in INTERVAL:
                    self.providers[id].interval = INTERVAL[interval]
            self.active.append(self.providers[id])
            self.providers[id]._activate()
            
    def load_notifiers(self):
        notifiers = self.config.get('general', 'notifiers')
        if not notifiers:
            notifiers = ['x11', 'tmux']
        else:
            notifiers = [i.strip() for i in notifiers.split(',')]
        for id in notifiers:
            cls = lib.notifier.get_class(id)
            if not cls:
                continue
            config = {}
            for key in cls.config_keys:
                config[key] = self.config.get('general', id+'_'+key, '')
            deps = self.get_new_deps(cls.deps)
            if deps == None:
                continue
            for dep, dep_cls in deps.items():
                self.deps[dep] = dep_cls(self)
            self.notifiers.append(cls(self, config))

    def notify(self, obj):
        self.lock.acquire()
        self.log.add(obj)
        start = time.time()
        for notifier in self.notifiers:
            notifier._notify(obj)
        if self.config.get('general','notify_time','').isnumeric():
            wait_time = float(self.config.get('general','notify_time'))
        else:
            wait_time = 4.0
        diff = time.time() - start
        if diff < wait_time:
            time.sleep(wait_time - diff)
        self.lock.release()

    def update(self):
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)
        for provider in self.active:
            provider._update()
