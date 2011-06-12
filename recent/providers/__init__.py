PROVIDERS = ['feed', 'statusnet', 'xmpp']

def get_class(id):
    if id == 'feed':
        import recent.providers.feed
        return recent.providers.feed.FeedProvider
    elif id == 'statusnet':
        import recent.providers.statusnet
        return recent.providers.statusnet.StatusnetProvider
    elif id == 'xmpp':
        import recent.providers.xmpp
        return recent.providers.xmpp.XMPPProvider
    return None
