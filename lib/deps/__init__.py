def get_class(id):
    if id == 'inet':
        import lib.deps.inet
        return lib.deps.inet.InetDep
    return None
