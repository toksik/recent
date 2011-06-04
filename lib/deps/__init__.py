def get_class(id):
    if id == 'inet':
        import lib.deps.inet
        return lib.deps.inet.InetDep
    elif id == 'x11':
        import lib.deps.x11
        return lib.deps.x11.X11Dep
    return None
