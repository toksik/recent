import lib.providers
import lib.deps
import lib.notifier

INTERVAL = {'instant':0, 'minute':60, 'halfhour':1800, 'hour':36000,
            'halfday':43200, 'day':86400}

class Notification:
    def __init__(self, provider, title, id, author=None, link=None, body=None,
                 tags=None):
        self.provider = provider
        self.title = title
        self.author = author
        self.link = link
        self.body = body
        self.id = id
        if not tags:
            self.tags = ['new', 'unread']
        else:
            self.tags = tags

class Manager:
    def __init__(self, config, state):
        self.providers = {}
        self.deps = {}
        self.notifiers = []
        self.active = []
        self.config = config
        self.state = state

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
        for notifier in self.notifiers:
            notifier._notify(obj)

    def update(self):
        for provider in self.active:
            provider._update()
