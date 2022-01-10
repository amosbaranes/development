# Example of threading

from threading import Thread
import time

def example(times):
	for i in range(times):
		print(i)
		time.sleep(1)

# Create Thread
thread = Thread(target=example, args=(5,))

# Start Thread
thread.start()

time.sleep(2)
print("This is printed in the main thread")

# Waiting thread to be done
thread.join()