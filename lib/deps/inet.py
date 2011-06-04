import subprocess

from lib.deps.base import Dependency

class InetDep(Dependency):
    id = 'inet'
    def check(self):
        p = subprocess.Popen(['ping','google.com','-c','1'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        res = p.stdout.read()
        if b'1 received' in res:
            return True
        return False
