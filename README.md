# Scheduler

Coding.

##Requirements:
Requirements:
- Assume scheduler needs to run permanently
- Assume a constant amount of N resources are available to you.
- Scheduler shall assign task to resource
- Each resource can execute 1 task and the resource is fully occupied until this
task is completed.
- “Resource” implementation incl. interface implementation is up to you.
- Scheduler shall balance the computational resources to all projects equally
(regardless of queue length, lot of activity on one project shall not clog the
processing of others)
- Assume a constant amount of projects: P
- Scheduler can retrieve current resource state; mainly if it is free or busy
(interface is up to you)
- Definition of the “task” representation is up to you, but at least it has to contain
information about the project (e.g. string, or number, ...)
- The tasks are arriving randomly and are available at (fictional) interface you
can call from anywhere within your scheduler:
outside_interface.check_for_new_task() which will return new task (if there is
one available) at representation you have defined
- Once started, the task cannot be paused and neither does it provide
information about its progress status.
- Scheduler shall provide output to console/log informing which task has started
and which ended, as well as any additional useful information
- Code shall be compatible with Python 3.9.7 and shall use Python standard
library only. (no external packages)
- Code shall be properly documented and should be written according to good
coding practices

UnitTest:
- Priority of task shall be represented as an integer, highest priority 1, lowest N.
- It shall serve as a “inverse” weight, meaning in optimal state scheduler shall be
running 4 tasks of prio 1 for 2 tasks of prio 2 and 1 of prio 4.

##
######Created by Dmytro Chernousan 9_22_23
