def get_class(id):
    if id == 'x11':
        import lib.notifier.x11notify
        return lib.notifier.x11notify.X11Notifier
    return None
