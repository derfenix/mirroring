SYSTEM REQUIREMENTS
===================

libxml-devel
libxslt-devel
python >= 2.7
python-pip


INSTALLATION
============

pip install /path/to/mirroring-0.1.tar.gz


USAGE
=====

As shell command
----------------

mirroring http://site.to.mirroring /save/path/ depth

    depth is optional, by default = infinity

As python module
----------------

from mirroring import Worker
worker = Worker('http://site.to.mirroring', '/save/path', 10)
worker.process()

        10 - mirroring depth, by default = infinity