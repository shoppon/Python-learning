import subprocess
from time import sleep

sp = subprocess.Popen('timeout 1000 /tmp/defunct.sh',
                      shell=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
sp.communicate()

sleep(1000)
