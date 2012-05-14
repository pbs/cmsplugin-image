import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

setup(
    name='cmsplugin-image',
    version='0.0.1',
    description='PBS Image Field type for Django CMS',
    long_description = open(README_PATH, 'r').read(),
    author='PBS Audience Facing Team',
    author_email='tpg-pbs-userfacing@threepillarglobal.com',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    setup_requires = ['s3sourceuploader',],
)
