import subprocess
import time

while 1:
    p = subprocess.Popen(['python3', 'src/examples/rainbow.py'])
    time.sleep(3)
    p.terminate()
    time.sleep(2)

    p = subprocess.Popen(['python3', 'src/examples/marnie.py'])
    p.wait()
    time.sleep(0.2)

    p = subprocess.Popen(['python3', 'src/examples/nostromo.py'])
    p.wait()
    time.sleep(0.2)

    p = subprocess.Popen(['python3', 'src/examples/lorem_ipsum.py'])
    p.wait()
    time.sleep(0.2)