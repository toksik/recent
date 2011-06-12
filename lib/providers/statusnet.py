import lib.providers.base
import lib.markup
from lib.manager import Notification

import feedparser

class StatusnetProvider(lib.providers.base.Provider):
    name = 'Statusnet'
    deps = ['inet']
    config_keys = ['api', 'user', 'deny_tags']
    interval = 60
    config_doc = '''
The statusnet provider can get new messages from identi.ca or other statusnet
servers.

For an account at identi.ca use

 api="https://identi.ca/api"

The \'api\' and the \'user\' keys are required.

If you want to filter out some tags set the \'deny_tags\' option to an
comma-seperated list of these tags.
'''
    def is_valid(self, tags):
        if self.config['deny_tags']:
            denied = [s.strip() for s in self.config['allow_tags'].split(',')]
            for tag in tags:
                if tag in denied:
                    return False
        return True
                
    def update(self):
        feed = feedparser.parse(self.config['api']+\
                '/statuses/friends_timeline/%s.atom'%self.config['user'])
        new_entries = []
        for entry in feed.entries:
            id = ''
            if 'id' in entry:
                id = entry.id
            author = ''
            if 'author' in entry:
                author = entry.author
            body = ''
            if 'content' in entry and entry.content and \
                   'value' in entry.content[0]:
                if entry.content[0].type == 'text/html':
                    body = lib.markup.html_to_log(entry.content[0].value,
                                                  reformat=False,
                                                  newlines=False)
                else:
                    body = entry.content[0].value
            link = ''
            if 'link' in entry:
                link = entry.link
            if 'tags' in entry:
                tags = []
                for tag in entry.tags:
                    if 'term' in tag:
                        tags.append(tag.term)
                if not self.is_valid(tags):
                    continue
            if not self.manager.state.check(self.id, id):
                new_entries.append(Notification(provider=self.name, id=id,
                                        title=body, author=author, link=id))
        for entry in new_entries[::-1]:
            self.manager.state.add(self.id, entry.id)
            self.manager.notify(entry)
