import subprocess
import time

while 1:
    p = subprocess.Popen(['python3', 'src/examples/rainbow.py'])

    time.sleep(5)

    p.terminate()

    p = subprocess.Popen(['python3', 'src/examples/marnie.py'])

    time.sleep(5)

    p.terminate()

    p = subprocess.Popen(['python3', 'src/examples/nostromo.py'])

    time.sleep(5)

    p.terminate()

    p = subprocess.Popen(['python3', 'src/examples/lorem_ipsum.py'])

    time.sleep(5)

    p.terminate()