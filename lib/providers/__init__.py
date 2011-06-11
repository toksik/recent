def get_class(id):
    if id == 'feed':
        import lib.providers.feed
        return lib.providers.feed.FeedProvider
    elif id == 'statusnet':
        import lib.providers.statusnet
        return lib.providers.statusnet.StatusnetProvider
    return None
