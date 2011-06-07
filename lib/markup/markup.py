from urllib.parse import urlparse

ELEMENT_WORD = 0
ELEMENT_PUNCTUATION = 1
ELEMENT_PRE = 2 # preformatted text
ELEMENT_PARAGRAPH = 3
ELEMENT_NEWLINE = 4
ELEMENT_LINK = 5
ELEMENT_IMAGE = 6

def is_link(text):
    for begin in ['http://', 'https://', 'ftp://', 'ssh:']:
        if text.startswith(begin):
            return True
    return False

def is_path(text):
    dot = -1
    for i in range(0, len(text)):
        if text[i] in [' ', ':', '!', '?', '(', ')', ',']:
            break
        elif text[i] == '.':
            dot = i
    if dot != -1:
        for ext in ['txt', 'zip', 'tar', 'mp3', 'ogg', 'wav', 'flac', 'html',
                    'htm', 'py', 'cpp', 'php']:
            if text[dot:].startswith('.'+ext):
                return True
    for prefix in ['/etc/', '/tmp/', '/usr/', '/var', '/home', '/proc',
                   '/sys/', '/media/', '/mnt/', '/bin/', '/sbin/', '/opt/']:
        if text.startswith(prefix):
            return True
    count = 0
    for i in range(0, len(text)):
        if text[i] == '/':
            count += 1
        elif text[i] in [' ', ':', '!', '?', '(', ')', ',']:
            break
    if count > 1:
        return True
    return False    

def is_shortcut(text):
    for shortcut in ['z.B.', 'usw.', 'u.a.', 'o.g.']:
        if text.startswith(shortcut):
            return True
    return False

class FormattingMarkup:
    def __init__(self):
        self.elements = []
        self.last_ref = 0
        self.last_image = ''

    def put_text(self, text, protect=False):
        if not text:
            return
        if protect:
            self.elements.append((ELEMENT_WORD, text))
            return
        word = ''
        for i in range(0, len(text)):
            if text[i] in [' ', '\n', '\t']:
                if not word:
                    continue
                if is_link(word):
                    self.put_link(word, tmp=True)
                    word = ''
                else:
                    self.elements.append((ELEMENT_WORD, word))
                    word = ''
            elif text[i] in ['.', ',', '!', '?', ':', ';', '(', ')', '/',
                             '"', '\'']:
                if not word:
                    if text[i] == '/' and is_path(text[i:]):
                        word = '/'
                        continue
                    self.elements.append((ELEMENT_PUNCTUATION, text[i]))
                elif is_link(text[i-len(word):]):
                    if text[i] not in ['/', '.', ';', ':']:
                        self.put_link(word, tmp=True)
                        word = ''
                    else:
                        word = word + text[i]
                elif is_path(text[i-len(word):]):
                    word = word + text[i]
                elif text[i] == '.' and text[i-1].isnumeric() \
                         and i < len(text) and text[i+1].isnumeric():
                    word = word + text[i]
                elif text[i] == ',' and text[i-1].isnumeric() \
                         and i < len(text) and text[i+1].isnumeric():
                    word = word + text[i]
                elif is_shortcut(text[i-len(word):]):
                    word = word + text[i]
                else:
                    self.elements.append((ELEMENT_WORD, word))
                    word = ''
                    self.elements.append((ELEMENT_PUNCTUATION, text[i]))
            else:
                word = word + text[i]
        if not word:
            return
        if is_link(word):
            self.put_link(word, tmp=True)
        else:
            self.elements.append((ELEMENT_WORD, word))

    def put_link(self, ref, tmp=False):
        if ref == self.last_image:
            return
        if tmp:
            url = urlparse(ref)
            if url.hostname:
                self.put_text(url.hostname, protect=True)
        self.elements.append((ELEMENT_LINK, ref))
        if tmp:
            self.last_ref = len(self.elements)-1
        else:
            if self.elements[self.last_ref][0] == ELEMENT_LINK \
                   and self.elements[self.last_ref][1] == ref:
                self.elements.pop(self.last_ref)

    def put_image(self, ref, name):
        self.last_image = ref
        self.elements.append((ELEMENT_IMAGE, ref, name))

    def put_paragraph(self):
        if not self.elements:
            return
        if self.elements[-1][0] == ELEMENT_PARAGRAPH:
            return
        if self.elements[-1][0] == ELEMENT_PRE:
            return
        if self.elements[-1][0] == ELEMENT_NEWLINE:
            self.elements.pop(-1)
        self.elements.append((ELEMENT_PARAGRAPH,))

    def put_newline(self):
        if not self.elements:
            return
        if self.elements[-1][0] == ELEMENT_PARAGRAPH:
            return
        if self.elements[-1][0] == ELEMENT_PRE:
            return
        if self.elements[-1][0] == ELEMENT_NEWLINE:
            return
        self.elements.append((ELEMENT_PARAGRAPH,))

    def put_pre(self, text):
        if self.elements and self.elements[-1][0] == ELEMENT_PARAGRAPH \
               or self.elements[-1][0] == ELEMENT_NEWLINE:
            self.elements.pop(-1)
        self.elements.append((ELEMENT_PRE, text))

    def parse(self, out):
        for i in range(0, len(self.elements)):
            item = self.elements[i]
            if item[0] == ELEMENT_WORD:
                if i == 0:
                    out.put_text(item[1])
                elif self.elements[i-1][0] in [ELEMENT_WORD, ELEMENT_LINK,
                                               ELEMENT_IMAGE]:
                    out.put_text(' '+item[1])
                elif self.elements[i-1][0] == ELEMENT_PUNCTUATION:
                    if self.elements[i-1][1] in ['.', ',', '!', '?', ':',
                                                 ';', ')']:
                        out.put_text(' '+item[1])
                    elif self.elements[i-1][1] in ['(', '/', '"', '\'']:
                        out.put_text(item[1])
                else:
                    out.put_text(item[1])
            elif item[0] == ELEMENT_PUNCTUATION:
                if i == 0:
                    out.put_text(item[1])
                elif self.elements[i-1][0] == ELEMENT_WORD:
                    if item[1] in ['.', ',', '!', '?', ':', ';', ')']:
                        out.put_text(item[1])
                    elif item[1] in ['(', '/', '"', '\'']:
                        out.put_text(' '+item[1])
                else:
                    out.put_text(item[1])
            elif item[0] == ELEMENT_LINK:
                out.put_link(item[1])
            elif item[0] == ELEMENT_IMAGE:
                out.put_image(item[1], item[2])
            elif item[0] == ELEMENT_PARAGRAPH:
                out.put_paragraph()
            elif item[0] == ELEMENT_NEWLINE:
                out.put_newline()
            elif item[0] == ELEMENT_PRE:
                out.put_pre(item[1])

class LogMarkup:
    def __init__(self):
        self.buff = ''
        
    def put_text(self, text, protect=False):
        self.buff = self.buff + text

    def put_paragraph(self):
        self.buff = self.buff + '\n\n'

    def put_newline(self):
        self.buff = self.buff + '\n'

    def put_link(self, url, tmp=False):
        self.buff = self.buff + ' [[link %s ]]'%url

    def put_image(self, url, name):
        self.buff = self.buff + ' [[img %s | %s ]]'%(url, name)

    def put_pre(self, text):
        if not text:
            return
        self.buff = self.buff + '\n\n'
        for line in text.split('\n'):
            if not line:
                continue
            self.buff = self.buff + '| %s\n'%line
        self.buff = self.buff + '\n'
        
    def parse(self, out):
        if not self.buff:
            return
        pre = ''
        pgraph = True
        for line in self.buff.split('\n'):
            if not line and not pgraph:
                out.put_paragraph()
                pgraph = True
                continue
            elif not pgraph:
                out.put_newline()
            elif line[0] == '|':
                pre = pre + line[2:]
                continue
            elif pre:
                out.put_pre(pre)
                pre = ''
            offset = 0
            while True:
                next = line.find('[[', offset)
                if next == -1:
                    break
                text = line[offset:next-1]
                if text:
                    out.put_text(text)
                end = line.find(']]', next)
                if line[next+2:next+6] == 'link':
                    url = line[next+3:end-1]
                    out.put_link(url)
                    offset = end+2
                elif line[next+2:next+5] == 'img':
                    split = line.find(' | ', next)
                    url = line[next+3:split]
                    name = line[split+3:end-1]
                    out.put_image(url, name)
                    offset = end+2
                else:
                    out.put_text('[[')
                    offset = next+2
            text = line[offset:]
            if text:
                out.put_text(text)
            pgraph = False
                    
class LogOutputMarkup:
    def __init__(self):
        self.buff = ''
        self.refs = []

    def put_text(self, text):
        self.buff = self.buff + text

    def put_paragraph(self):
        self.buff = self.buff + '\n\n'

    def put_newline(self):
        self.buff = self.buff + '\n'

    def put_link(self, url):
        self.refs.append(url)
        self.buff = self.buff + ' [%i]'%len(self.refs)

    def put_image(self, url, name):
        self.refs.append(url)
        self.buff = self.buff + ' Image %i: "%s"'%(len(self.refs), name)
        
    def put_pre(self, text):
        self.buff = self.buff + '\n\n'
        for line in text.split('\n'):
            self.buff = self.buff + ' | ' + line + '\n'
        self.buff = self.buff + '\n'

class LogOutputColorMarkup:
    def __init__(self):
        self.buff = ''
        self.refs = []

    def put_text(self, text):
        self.buff = self.buff + text

    def put_paragraph(self):
        self.buff = self.buff + '\n\n'

    def put_newline(self):
        self.buff = self.buff + '\n'

    def put_link(self, url):
        self.refs.append(url)
        self.buff = self.buff + ' \033[34m[%i]\033[0m'%len(self.refs)

    def put_image(self, url, name):
        self.refs.append(url)
        self.buff = self.buff + ' \033[36mImage %i: "%s"\033[0m'%(
            len(self.refs), name)
        
    def put_pre(self, text):
        self.buff = self.buff + '\n\n'
        for line in text.split('\n'):
            if not line:
                continue
            self.buff = self.buff + '\033(0x\033(B \033[1m' + line + \
                        '\033[0m\n'
        self.buff = self.buff + '\n'
