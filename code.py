#  -*- coding: utf-8 -*-
""" Project: service | File: code.py | Created: 9/23/23, 1:33 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import logging
import time
from random import randint
from threading import Thread


class Task(Thread):
    """
    Class Task
    """

    def __init__(self, name: str, priority: int = 1):
        super().__init__()
        self.name = name
        self.priority = priority
        self._callback = None

    def set_callback(self, fn_in: object) -> None:
        """
        :param fn_in: object
        """
        self._callback = fn_in

    def run(self) -> None:
        """
        Start task
        """
        logging.debug('%s priority %s - STARTED', self.name, self.priority)
        time.sleep(randint(2, 4))  # payload imitation
        logging.debug('%s  priority %s - FINISHED', self.name, self.priority)
        if self._callback:
            self._callback()


class Resource:
    """
    Class Resource
    """
    STOPPED = 0
    STARTED = 1

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._state = self.STOPPED

    def can_processing(self) -> bool:
        """
        :return: Resource state
        """
        return self._state == self.STOPPED

    def start_processing(self, task: Task) -> None:
        """
        :param task:
        :return: None
        """
        if self._state == self.STARTED:
            # can`t start started Resource
            return None
        if task is None:
            # can`t start None Task
            return None
        # Set Resource state to STARTED
        self._state = self.STARTED
        logging.debug('%s start processing %s priority %s set to - BUSY',
                      self.name, task.name, task.priority)
        # set callback
        task.set_callback(self.stop_processing)
        task.start()

        return None

    def stop_processing(self) -> None:
        """
        # Set Resource state to STOPPED
        """
        logging.debug('%s set to - FREE', self.name)
        self._state = self.STOPPED


class Queue:
    """
    Class custom Queue
    """

    def __init__(self):
        self._task_list = []

    def count(self) -> int:
        """
        :return: count of Task in queue
        """
        return len(self._task_list)

    def add(self, item: Task) -> None:
        """
        :param item: task class instance
        """
        self._task_list.append(item)

    def remove(self, item: Task) -> None:
        """
        :param item: task class instance
        """
        self._task_list.remove(item)

    def ready(self) -> [Task, None]:
        """
        Return task with minimal value of priority
        :return: task with high priority
        """
        l_sorted = sorted(self._task_list, key=lambda t: t.priority)
        return l_sorted[0] if l_sorted else None


class Scheduler(Thread):
    """
    Class Scheduler
    Works permanent
    Works in Thread
    """

    def __init__(self, queue: Queue):
        super().__init__()
        self._queue = queue
        self._resources = {}
        self._resource_cursor = 0
        self._processing = True
        self.start()  # auto start

    def add_resource(self, key: int, value: Resource) -> None:
        """
        add Resource to Scheduler
        :param key:
        :param value:
        """
        self._resources[key] = value

    def get_resource(self) -> [Resource, None]:
        """
        :return: free resource
        """
        for idx, item in self._resources.items():
            if item.can_processing() and idx == self._resource_cursor:
                return item
        return None

    def run(self) -> None:
        """
        Start scheduler
        """
        logging.info('Scheduler is started')
        while self._processing:
            # sleep
            time.sleep(1)
            logging.debug('Scheduler is started')

            # get ready Resource
            resource = self.get_resource()
            if resource is None:
                logging.warning('Please add Resource')
                continue

            # get ready Task
            task = self._queue.ready()
            if task is None:
                logging.warning('Please add Task')
                continue

            # set Task to Resource
            logging.debug('%s linked %s priority %s', resource.name, task.name, task.priority)
            resource.start_processing(task)
            self._queue.remove(task)

            # increment Resource cursor for balancing
            self._resource_cursor += 1
            if self._resource_cursor > len(self._resources) - 1:
                self._resource_cursor = 0

    def finish(self) -> None:
        """
        Stop scheduler
        """
        self._processing = False


class Generator(Thread):
    """
    Task generator
    """
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.idx = 0
        self.start()  # auto start

    def run(self):
        """
        Generator processing
        """
        while True:
            priority = randint(1, 5)
            name = f'Task_{self.idx}'
            task = Task(name, priority)
            logging.info('%s priority %s CREATED', task.name, task.priority)
            self.queue.add(task)
            self.idx += 1
            time.sleep(randint(1, 2))


if __name__ == '__main__':
    # init logging
    logging.basicConfig(filename='code.log', level=logging.DEBUG,
                        format='%(asctime)15s - %(levelname)s - %(message)s')
    logging.info('Start program')

    # init Task Queue
    task_queue = Queue()

    # init & start Scheduler. Set queue to scheduler
    scheduler = Scheduler(task_queue)

    # init Resource
    resource_0 = Resource('Resource_0')
    resource_1 = Resource('Resource_1')

    # add Resource to Scheduler
    scheduler.add_resource(0, resource_0)
    scheduler.add_resource(1, resource_1)

    # init & start Task Generator. Set queue to generator
    generator = Generator(task_queue)
