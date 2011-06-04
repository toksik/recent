def get_class(id):
    if id == 'feed':
        import lib.providers.feed
        return lib.providers.feed.FeedProvider
    return None
