import feedparser as fp


def get_new(url):
    d = fp.parse(url)
    string = ''
    string += d.entries[0].title + '\n' + '------------------' + '\n'
    string += d.entries[0].link + '\n' + '------------------' + '\n'
    string += d.entries[0].description + '\n' + '------------------' + '\n'
    string += d.entries[0].category
    return string
