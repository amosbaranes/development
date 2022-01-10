from queue import Queue, Empty
from threading import Thread, current_thread


class PrinterStreamer:
    def __init__(self):
        self.queues = {}

    def add_target(self, target, args):
        thread = Thread(target=target, args=args)
        queue = self.register(thread)
        return queue, thread

    def start(self, thread):
        thread.start()
        queue = self.queues[thread.name]
        while thread.is_alive():
            try:
                item = queue.get_nowait()
                yield f'data:{item}\n\n'
            except Empty:
                pass
        yield 'End'
        self.clean(thread)

    def write(self, value):
        '''handle stdout'''
        queue = self.queues.get(current_thread().name)
        if queue:
            queue.put(value)
        else:
            sys.__stdout__.write(value)

    def flush(self):
        '''Django would crash without this'''
        pass

    def register(self, thread):
        '''register a Thread'''
        queue = Queue()
        self.queues[thread.name] = queue
        return queue

    def clean(self, thread):
        '''delete a Thread'''
        del self.queues[thread.name]


class Printer:
    def __init__(self):
        self.queues = {}

    def write(self, value):
        '''handle stdout'''
        queue = self.queues.get(current_thread().name)
        if queue:
            queue.put(value)
        else:
            sys.__stdout__.write(value)

    def flush(self):
        '''Django would crash without this'''
        pass

    def register(self, thread):
        '''register a Thread'''
        queue = Queue()
        self.queues[thread.name] = queue
        return queue

    def clean(self, thread):
        '''delete a Thread'''
        del self.queues[thread.name]


class Steamer:
    def __init__(self, target, printer_, args):
        self.thread = Thread(target=target, args=args)
        self.queue = printer_.register(self.thread)
        self.printer = printer_

    def start(self):
        self.thread.start()
        while self.thread.is_alive():
            try:
                item = self.queue.get_nowait()
                yield f'data:{item}\n\n'
            except Empty:
                pass
        yield 'End'
        self.printer.clean(self.thread)

