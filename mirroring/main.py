#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
.. module: main
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import logging
import multiprocessing
import sys
import signal

from mirroring.item import Item, StopProcessing


logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.DEBUG)


def proccess(lnk):
    visited = set()
    try:
        item = Item(lnk, visited)
        item.save()
        logger.info(lnk)
        return item.urls
    except StopProcessing:
        pass


def run(base, save_root, proc_count=None):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Item.set_save_root(save_root)
    Item.set_base_url(base)
    visited = set()

    if not proc_count:
        proc_count = multiprocessing.cpu_count() * 2

    if isinstance(base, (str, unicode)):
        links = [[base, ]]
    else:
        links = [base]

    while links:
        pool = multiprocessing.Pool(proc_count)
        try:
            work = []
            links_ = []
            for link_ in links:
                if link_:
                    links_ += link_
            for l in links_:
                if l not in visited:
                    visited.add(l)
                    work.append(l)
            links = []
            r = []
            for i in xrange(0, proc_count):
                r = pool.map_async(proccess, work[i::proc_count])
                links += r.get()

        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            sys.exit(0)
        else:
            pool.close()
            pool.join()

        # pool.close()
        # pool.join()


if __name__ == "__main__":
    pc = int(sys.argv[3]) if len(sys.argv) > 3 else None
    run(sys.argv[1], sys.argv[2], pc)