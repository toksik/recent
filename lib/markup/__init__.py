import lib.markup.html_markup
import lib.markup.markup

def html_to_log(text):
    hm = html_markup.HTMLMarkup(text)
    c = markup.FormattingMarkup()
    hm.parse(c)
    m = markup.LogMarkup()
    c.parse(m)
    return m.buff
