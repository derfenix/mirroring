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

mirroring http://site.to.mirroring /save/path/ proc_count

    proc_count is optional, by default = cpu_count * 2

As python module
----------------

from mirroring.main import run
run('http://site.to.mirroring', '/save/path')
