import recent.markup.html_markup
import recent.markup.markup

def html_to_log(text, newlines=True, reformat=True):
    '''Converts html code to log markup'''
    hm = recent.markup.html_markup.HTMLMarkup(text)
    m = recent.markup.markup.LogMarkup()
    if reformat:
        c = recent.markup.markup.FormattingMarkup(newlines=newlines)
        hm.parse(c)
        c.parse(m)
    else:
        hm.parse(m)
    if not newlines:
        return m.buff.replace('\n',' ')
    return m.buff
