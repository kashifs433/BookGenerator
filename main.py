import threading
import subprocess
import os
import sys

def run_bookgen():
    subprocess.run([sys.executable, os.path.join("API", "BookGenAPIEngine.py")])

def run_bookq():
    subprocess.run([sys.executable, os.path.join("Queues", "BookQ.py")])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bookgen)
    t2 = threading.Thread(target=run_bookq)

    t1.start()
    t2.start()

    t1.join()
    t2.join()