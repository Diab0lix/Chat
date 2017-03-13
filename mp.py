import threading as th
import random

lock = th.Lock()
dice = []

def compute():
    with lock:
        result = random.randint(1, 6)
        dice.append(result)

for i in range(1000):
    thread = th.Thread(target = compute)
    thread.start()

thread.join()

moyenne = sum(dice)/len(dice)
print(moyenne)
