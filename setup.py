from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyflacmeta',
    version='0.0.1',
    description='Pure Python3 FLAC Metadata Reader'
    long_description=readme,
    author='Isaac Zafuta',
    author_email='isaac@zafuta.com',
    url='https://github.com/isaaczafuta/pyflacmeta',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
