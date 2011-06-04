import html.parser
import html.entities
import lib.markup

STATE_NONE = 0
STATE_LINK = 1
STATE_PRE = 2
HTML_ENTITIES = {'&quot;':'"',
                 '&lt;':'<',
                 '&gt;':'>',
                 '&amp;':'&',
                 '&apos;':'\''}

SMILEYS = {':-)':':-)', ':)':':-)', ';-)':';-)', ';)':';-)', ':-(':':-(',
           ':(':':-(', 'xD':'xD', 'XD':'xD', ';-(':';-(', ';(':';-('}

def get_smiley(attrs):
    if 'alt' in attrs and attrs['alt'] in SMILEYS:
        return SMILEYS[attrs['alt']]
    elif 'alt' in attrs and 'class' in attrs and attrs['class'] == 'wp-smiley':
        return attrs['alt']
    return None

class HTMLMarkup(html.parser.HTMLParser):
    def __init__(self, buff=None):
        html.parser.HTMLParser.__init__(self)
        self.buff = buff
        self.state = STATE_NONE
        self.link_ref = ''
        self.out = None

    def parse(self, out):
        self.out = out
        self.state = STATE_NONE
        self.link_ref = ''
        self.reset()
        self.feed(self.buff)

    def put_text(self, text):
        for key,value in HTML_ENTITIES.items():
            text = text.replace(key, value)
        self.out.put_text(text)

    def handle_starttag(self, tag, attrs):
        if self.state == STATE_PRE:
            return
        attrs = dict(attrs)
        if tag == 'p':
            self.out.put_paragraph()
        elif tag == 'br':
            self.out.put_newline()
        elif tag == 'a':
            if 'href' in attrs and attrs['href']:
                self.state = STATE_LINK
                self.link_ref = attrs['href']
        elif tag == 'img':
            smiley = get_smiley(attrs)
            if smiley:
                self.out.put_text(smiley, protect=True)
            elif 'src' in attrs:
                if 'alt' in attrs and attrs['alt']:
                    self.out.put_image(attrs['src'], attrs['alt'])
                elif 'title' in attrs and attrs['title']:
                    self.out.put_image(attrs['src'], attrs['title'])
                else:
                    self.out.put_image(attrs['src'], attrs['src'])
        elif tag == 'pre':
            self.state = STATE_PRE

    def handle_endtag(self, tag):
        if self.state == STATE_PRE:
            if tag == 'pre':
                self.state = STATE_NONE
        elif tag == 'a' and self.state == STATE_LINK:
            self.state = STATE_NONE
            self.out.put_link(self.link_ref)
            self.link_ref = ''

    def handle_data(self, data):
        if self.state == STATE_PRE:
            self.out.put_pre(data)
        else:
            self.put_text(data)
