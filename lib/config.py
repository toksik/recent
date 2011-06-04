import configparser

class RecentConf:
    def __init__(self, path):
        self.path = path
        self.parser = configparser.RawConfigParser()
        self.parser.read(self.path)

    def get(self, id, key, default=None):
        try:
            return self.parser.get(id, key)
        except:
            return default

    def index(self):
        sections = list(self.parser.sections())
        if 'general' in sections:
            sections.remove('general')
        res = []
        for section in sections:
            if self.get(section, 'type'):
                res.append(section)
        return res
    
