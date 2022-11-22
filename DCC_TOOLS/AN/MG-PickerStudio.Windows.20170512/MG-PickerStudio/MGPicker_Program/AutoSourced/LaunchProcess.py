import subprocess
import os

def MGP_LoadProcess(program, args=[]):
    if not program or not os.path.isfile(program):
        return False
    theArgs = [program]
    theArgs.extend(args)
    try:
        subprocess.Popen(theArgs)
    except Exception as e:
        print 'Error loading program %s: %s' % (program, e.value)
        return False

    return True