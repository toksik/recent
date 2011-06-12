import configparser

def default_config():
    import lib.providers
    buff = '''\
## Syntax:
# The config file is structured using section. A section always begins with
#
#  [section_name]
#
# It may contain some key=value definions. Different data types are not
# supported (evey value is a string), but there are multiple ways of defining
# them.
#
#  key=value
#  key="value"
#
# Unknown keys are ignored. Lines starting with a \'"\' are comments.
#
## The \'general\' section
# Unlike any other sections the \'general\' section is not used to configure a
# provider, but for common options like how long notifications are displayed.
# Also notifiers are configured in this section with the syntax
#
#  notifier_key="value"
#
# Example:
#
#  x11notify_display="1"
#
# Keys in the general section:
#  notifiers -> a comma-seperated list of enabled notifiers (possible values
#               are \'x11\' and \'tmux\')
#  notify_time -> a float that specifies how long notifications are displayed
#                 (in seconds)
#
# Keys of notifiers:
#  x11notify_display -> the display that is used to show notifications on
#
# Example configuration:
#
#  [general]
#  notifiers="x11,tmux"
#  notify_time="8.0"
#
## Providers
# A Provider is a module that fetches news from a specific kind of source.
# For instance the \'feed\' provider can download rss and atom feeds and
# extract new items from it.
#
# Each source (e.g. a rss feed) is configured in it\'s very own section.
# Which provider will be used to handle it is defined by the \'type\' key.
# To fetch a rss feed e.g. at http://example.com/feed.rss the section would
# look like this:
#
#  [examplefeed]
#  type="feed"
#  url="http://example.com/feed.rss"
#
# As in the example, the section name can be anything, but must not contain any
# newlines and has to be unique.
#
'''
    for id in lib.providers.PROVIDERS:
        provider = lib.providers.get_class(id)
        if not provider:
            continue
        buff = buff + '## The provider "%s"\n'%id
        buff = buff + '# All config keys are:\n'
        buff = buff + '#  type="%s"\n'%id
        buff = buff + '#  interval\n'
        for key in provider.config_keys:
            buff = buff + '#  %s\n'%key
        buff = buff + '#\n'
        if provider.config_doc:
            for line in provider.config_doc.strip().split('\n'):
                buff = buff + '# %s\n'%line
            buff = buff + '#\n'
    return buff
        
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
    
