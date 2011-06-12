import subprocess

from recent.deps.base import Dependency

class X11Dep(Dependency):
    id = 'x11'
    def check(self):
        p = subprocess.Popen(['ps','-A'], stdout=subprocess.PIPE)
        p.wait()
        p_list = p.stdout.read()
        if b'X' in p_list:
            return True
        return False
