from distutils.core import setup

setup(
    name='mirroring',
    version='0.3.3',
    packages=['mirroring'],
    requires=['lxml', 'requests'],
    url='https://www.odesk.com/users/~01286f3481df6273cb',
    license='',
    author='Sergey Kostyuchenko',
    author_email='derfenix@gmail.com',
    description='',
    platforms='any',
    scripts=['scripts/mirroring']
)
