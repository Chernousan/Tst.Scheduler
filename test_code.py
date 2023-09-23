#  -*- coding: utf-8 -*-
#  """ Project: service | File: test_code.py | Created: 9/23/23, 1:55 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import logging
from time import sleep
from unittest import TestCase
from code import Scheduler, Queue, Resource, Task


class Scheduler_run(TestCase):
    def test_case_1(self):
        logging.basicConfig(filename='test_code.log', level=logging.DEBUG,
                            format='%(asctime)-15s  %(levelname)s - %(message)s')
        logging.info('Start program')

        # init Task queue
        task_queue = Queue()
        # 4 Task with priority 1
        task_1_p_1 = Task('Task_1_p_1', 1)
        task_2_p_1 = Task('Task_2_p_1', 1)
        task_3_p_1 = Task('Task_3_p_1', 1)
        task_4_p_1 = Task('Task_4_p_1', 1)
        # 2 Task with priority 2
        task_5_p_2 = Task('Task_5_p_2', 2)
        task_6_p_2 = Task('Task_6_p_2', 2)
        # 1 Task with priority 4
        task_7_p_4 = Task('Task_7_p_4', 4)

        # randomize Task
        random_task_array = [task_7_p_4, task_5_p_2, task_3_p_1, task_1_p_1, task_4_p_1, task_2_p_1, task_6_p_2]

        # init & start Scheduler
        scheduler = Scheduler(task_queue)

        # init Resource
        resource_0 = Resource('Resource_0')
        resource_1 = Resource('Resource_1')
        resource_2 = Resource('Resource_3')
        # add Resource to Scheduler
        scheduler.add_resource(0, resource_0)
        scheduler.add_resource(1, resource_1)
        scheduler.add_resource(2, resource_2)

        for task_item in random_task_array:
            logging.info(f'{task_item.name} priority {task_item.priority} ADDED to queue ')
            task_queue.add(task_item)

        # waiting processing all task in queue
        while task_queue.count() > 0:
            sleep(1)

        # stop scheduler after finish work
        scheduler.finish()

        self.assertTrue(task_queue.count() == 0, 'Some task is still in queue open')

