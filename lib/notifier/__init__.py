def get_class(id):
    if id == 'x11':
        import lib.notifier.x11notify
        return lib.notifier.x11notify.X11Notifier
    elif id == 'tmux':
        import lib.notifier.tmux
        return lib.notifier.tmux.TmuxNotifier
    return None
