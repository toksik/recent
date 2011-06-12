PROVIDERS = ['feed', 'statusnet', 'xmpp']

def get_class(id):
    if id == 'feed':
        import lib.providers.feed
        return lib.providers.feed.FeedProvider
    elif id == 'statusnet':
        import lib.providers.statusnet
        return lib.providers.statusnet.StatusnetProvider
    elif id == 'xmpp':
        import lib.providers.xmpp
        return lib.providers.xmpp.XMPPProvider
    return None
