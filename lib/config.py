import configparser

class RecentConf:
    '''RecentConf is a wrapper class for python configparser'''
    def __init__(self, path):
        '''\
Creates and returns a new RecentConf instance

  path -> the path to the config file

The file is parsed immediately.'''
        self.path = path
        self.parser = configparser.RawConfigParser()
        self.parser.read(self.path)

    def get(self, id, key, default=None):
        '''\
Returns the value of <key> in the section <id>

  id -> the config section
  key -> the key in the section
  default -> the return value if the value of key is not defined'''
        try:
            return self.parser.get(id, key)
        except:
            return default

    def index(self):
        '''\
Returns a list of the names of all source sections

It will all ignore sections without a "type" definition and the
"general" section.'''
        sections = list(self.parser.sections())
        if 'general' in sections:
            sections.remove('general')
        res = []
        for section in sections:
            if self.get(section, 'type'):
                res.append(section)
        return res
    
