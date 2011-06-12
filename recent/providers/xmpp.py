import recent.providers.base
import recent.markup.markup
from recent.manager import Notification

import sleekxmpp

class XMPPProvider(recent.providers.base.Provider):
    name = 'XMPP'
    deps = ['inet']
    config_keys = ['jid', 'password', 'priority']
    xmpp = None
    def session_handler(self, event):
        if not self.xmpp:
            return
        self.xmpp.get_roster()
        if self.config['priority'].isnumeric():
            self.xmpp.send_presence(ppriority=int(self.config['priority']))
        else:
            self.xmpp.send_presence()

    def message_handler(self, msg):
        if msg['type'] == 'chat':
            m = recent.markup.markup.LogMarkup()
            fm = recent.markup.markup.FormattingMarkup(newlines=False)
            fm.put_text(msg['body'])
            fm.parse(m)
            body = m.buff
            n = Notification(provider=self.name, id=msg['id'], title=body,
                             author=msg['from'].user)
            self.manager.notify(n)
    
    def activate(self):
        self.xmpp = sleekxmpp.ClientXMPP(self.config['jid'],
                                         self.config['password'])
        self.xmpp.add_event_handler('session_start', self.session_handler)
        self.xmpp.add_event_handler('message', self.message_handler)
        self.xmpp.register_plugin('xep_0030')
        self.xmpp.register_plugin('xep_0004')
        self.xmpp.register_plugin('xep_0060')
        self.xmpp.register_plugin('xep_0199')
        self.xmpp.connect()
        self.xmpp.process(threaded=True)

    def deactivate(self):
        if self.xmpp:
            self.xmpp.disconnect()
