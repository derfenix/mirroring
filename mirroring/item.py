# -*- coding: utf-8 -*-
"""
.. module: manager
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from __future__ import unicode_literals
import logging

import os
import requests
from requests.exceptions import ConnectionError

from mirroring.processors import Processors
from mirroring.utils import cached_property


class StopProcessing(Exception):
    pass


class BadStatus(StopProcessing):
    pass


def gen_tree(path):
    path = os.path.split(path)[0].split(os.sep)
    pp = u'/'
    for p in path:
        pp += p + '/'
        if not os.access(pp, 4):
            os.mkdir(pp)


class Item(object):
    url = None
    visited = []
    save_root = None
    enc = None
    base_url = None

    _bad_urls = (
        'mailto:', 'javascript:', '//', 'tel:', '#'
    )

    def __init__(self, url, visited):
        for u in self._bad_urls:
            if url.startswith(u):
                raise StopProcessing()

        self.url = url
        url = self.base_url + url.replace(self.base_url, '')
        self.fetch_url = url
        self.visited = visited
        self.enc = None

    @cached_property
    def processor(self):
        p = Processors()
        processor = p[self.mimetype]
        if processor:
            res = self._fetch['res']
            processor.base_url = self.base_url
            return processor(self.url, res, self.mimetype)
        else:
            logging.error('No proccessor for {0}'.format(self.mimetype))
            raise StopProcessing()

    @classmethod
    def set_save_root(cls, save_root):
        cls.save_root = save_root

    @classmethod
    def set_base_url(cls, base_url):
        cls.base_url = base_url

    def save(self):
        save_path = self.save_path
        gen_tree(save_path)
        content = self.processor.content
        if self.mimetype.startswith('text') or self.mimetype == 'application/javascript':
            try:
                content = unicode(self.content).encode('utf-8')
            except:
                pass
        with file(save_path, 'w+') as h:
            h.write(content)
        return

    @cached_property
    def _fetch(self):
        try:
            res = requests.get(self.fetch_url)
        except ConnectionError:
            raise StopProcessing()

        if res.status_code != 200:
            raise BadStatus()

        content_type = res.headers['content-type']

        if res.encoding:
            self.enc = res.encoding.lower()
        else:
            self.enc = None

        if content_type.startswith('text') or content_type == 'application/javascript':
            content = res.text
            if self.enc != 'utf-8' and self.enc != 'utf8':
                content = unicode(content).encode('utf-8')
        else:
            content = res.content

        return {'res': res, 'content': content, 'mimetype': content_type}

    @cached_property
    def content(self):
        return self.processor.content

    @cached_property
    def mimetype(self):
        return self._fetch['mimetype']

    @cached_property
    def urls(self):
        urls = self.processor.files
        return [url for url in urls if url not in self.visited]

    @cached_property
    def save_path(self):
        save_path = self.processor.gen_save_path()
        save_path = self.save_root + save_path
        return save_path
