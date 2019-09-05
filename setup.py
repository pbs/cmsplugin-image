import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

DEPENDENCIES = [
    "django-filer >= 0.9pbs, <0.9.1"
]


setup(
    name='cmsplugin-image',
    version='2.0.0',
    description='PBS Image Field type for Django CMS',
    long_description=open(README_PATH, 'r').read(),
    author='PBS Audience Facing Team',
    author_email='tpg-pbs-userfacing@threepillarglobal.com',
    install_requires=DEPENDENCIES,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
)
