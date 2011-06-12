def get_class(id):
    if id == 'x11':
        import recent.notifier.x11notify
        return recent.notifier.x11notify.X11Notifier
    elif id == 'tmux':
        import recent.notifier.tmux
        return recent.notifier.tmux.TmuxNotifier
    return None
