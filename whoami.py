import subprocess

with open('out.txt', 'w') as file:
    proc = subprocess.run(['whoami'], stdout=file)
