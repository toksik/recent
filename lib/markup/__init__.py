import lib.markup.html_markup
import lib.markup.markup

def html_to_log(text, newlines=True, reformat=True):
    '''Converts html code to log markup'''
    hm = html_markup.HTMLMarkup(text)
    m = markup.LogMarkup()
    if reformat:
        c = markup.FormattingMarkup(newlines=newlines)
        hm.parse(c)
        c.parse(m)
    else:
        hm.parse(m)
    if not newlines:
        return m.buff.replace('\n',' ')
    return m.buff
