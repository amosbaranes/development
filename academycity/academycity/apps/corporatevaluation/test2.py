# Example of redirect stdout
import sys

class Printer:
    def __init__(self):
        self.contents = []

    def write(self, value):
        self.contents.append(value)

printer = Printer()
sys.stdout = printer

print('This should be saved in printer')

sys.stdout = sys.__stdout__

print('This should be printed to stdout')

print(printer.contents)