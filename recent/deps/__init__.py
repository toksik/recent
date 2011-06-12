def get_class(id):
    if id == 'inet':
        import recent.deps.inet
        return recent.deps.inet.InetDep
    elif id == 'x11':
        import recent.deps.x11
        return recent.deps.x11.X11Dep
    return None
