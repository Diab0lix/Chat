import subprocess

with open('whoami.txt', 'w') as file:
    proc = subprocess.run(['whoami'], stdout=file)
