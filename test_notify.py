import pync
import time

print("Waiting 3 seconds...")
time.sleep(3)
pync.notify("Test notification from Pomodoro!", title="Pomodoro")
