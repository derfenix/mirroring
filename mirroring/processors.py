# -*- coding: utf-8 -*-
"""
.. module: processors
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import logging
import hashlib

import os
from lxml import html
from lxml.etree import XMLSyntaxError
import re

from mirroring.utils import cached_property


class Processor(object):
    content_type = None
    base_url = None

    def __init__(self, url, res, content_type=None):
        self._url = url
        if res.encoding:
            enc = res.encoding
            self.enc = enc.lower()
        else:
            enc = False
            self.enc = None

        if content_type.startswith('text') \
                or content_type == 'application/javascript':
            content = res.text
            if self.enc != 'utf-8':
                content = unicode(content).encode('utf-8')
        else:
            content = res.content

        if bool(enc):
            try:
                content = content.replace(enc, 'utf-8')
            except Exception as e:
                print e
                pass

        self.content = content

        if content_type is not None:
            self.content_type = content_type

        _bar = self.files

    @cached_property
    def url(self):
        return self._get_url()

    def _get_url(self):
        return self._url

    @cached_property
    def path(self):
        return self._get_path()

    def _get_path(self):
        return self.url

    @cached_property
    def files(self):
        return self._get_files()

    # noinspection PyMethodMayBeStatic
    def _get_files(self):
        return []

    @staticmethod
    def _gen_image_name(url):
        url = url.split(u'?')[-1]
        md = hashlib.md5()
        md.update(unicode(url).encode('utf-8'))
        return md.hexdigest() + '.jpg'

    def gen_save_path(self):
        return self.url.replace(self.base_url, '')


class CssProcessor(Processor):
    content_type = 'text/stylesheet'

    def _get_files(self):
        regex = re.compile('url\([\'"]?([a-z0-9_/.-]*)[\'"]?\)')
        files = regex.findall(self.content)
        files_ = set()
        for f in files:
            f = f.replace(f, f.replace(self.base_url, ''))
            f = os.path.split(self._url.replace(self.base_url, ''))[0] + '/' + f
            files_.add(f)
        return files_


class HtmlProcessor(Processor):
    content_type = 'text/html'

    def _get_files(self):
        try:

            h = html.fromstring(self.content)
        except XMLSyntaxError:
            logging.exception(u"Failed to parse `{0}".format(self._url))
            return []
        hrefs = h.xpath('//a/@href')
        rels = h.xpath('//link/@href')
        scripts = h.xpath('//script/@src')
        images = h.xpath('//img/@src')

        res = set()

        links = hrefs + rels + scripts

        for link in links:
            if (link.startswith('http://') or link.startswith('https://')) \
                    and not link.startswith(self.base_url):
                continue
            if self.enc != 'utf-8':
                link = unicode(link).encode('utf-8')
            self.content = self.content.replace(link, link.replace(self.base_url, ''))
            res.add(link)

        for link in set(images):
            if (link.startswith('http://') or link.startswith('https://')) \
                    and not link.startswith(self.base_url):
                continue
            if self.enc != 'utf-8':
                link = unicode(link).encode('utf-8')
            self.content = self.content.replace(link, link.replace(self.base_url, ''))
            if link.find('?') >= 0:
                link = link.replace(self.base_url, '')
                img_link = link.split('?')
                img_link[-1] = self._gen_image_name(link)
                img_link = u'/'.join(img_link)
                print link, img_link
                self.content = self.content.replace(link.replace('&', '&amp;'), img_link)
            res.add(link)
        return res

    def gen_save_path(self):
        url = super(HtmlProcessor, self).gen_save_path()
        if url.endswith('/') or url == self.base_url or url == '' \
                or not os.path.splitext(url)[1]:
            return unicode(url) + u'/index.html'
        return url


class JsProcessor(Processor):
    def _get_files(self):
        regex = re.compile('[\'"]([^.]*\.(?:gif|jpg|png|jpeg))[\'"]')
        return regex.findall(self.content)


class ImageProcessor(Processor):
    def gen_save_path(self):
        url = super(ImageProcessor, self).gen_save_path()
        if url.find('?') >= 0:
            url_ = url.split('?')
            url_[-1] = self._gen_image_name(url)
            return '/'.join(url_)
        return url


class Processors(object):
    _processors = {
        'text/html': HtmlProcessor,
        'text/css': CssProcessor,
        '.*/javascript': JsProcessor,
        'image/.*': ImageProcessor,
    }

    def __getitem__(self, item):
        for regex, value in self._processors.items():
            if re.match(regex, item):
                return value
        return None
