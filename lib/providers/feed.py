import lib.providers.base
import lib.markup

from urllib.request import HTTPBasicAuthHandler, HTTPError, build_opener
import feedparser

class FeedProvider(lib.providers.base.Provider):
    name = 'Feed'
    deps = ['internet']
    config_keys = ['url', 'user', 'password', 'realm']
    def update(self):
        if not self.config['url']:
            return None
        auth = HTTPBasicAuthHandler()
        if self.config['realm'] and self.config['user'] \
           and self.config['password']:
            auth.add_password(realm=self.config['realm'],
                              user=self.config['user'],
                              passwd=self.config['password'])
        opener = build_opener(auth)
        try:
            resp = opener.open(self.config['url'])
        except HTTPError:
            return False
        p = feedparser.parse(resp)
        if not p.entries:
            return False
        author = p.feed.title
        for entry in p.entries:
            if 'link' not in entry or 'title' not in entry \
                   or self.manager.is_done(self.id, entry.link):
                continue
            link = entry.link
            id = entry.link
            title = entry.title
            body = None
            if 'content' in entry and entry.content:
                if entry.content[0].type == 'text/html':
                    body = lib.markup.html_to_log(entry.content[0].value)
                else:
                    body = entry.content[0].value
            n = Notification(provider=self.name, id=id, title=title,
                             author=author, link=link, body=body)
            self.manager.notify(n)
