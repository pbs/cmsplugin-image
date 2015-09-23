import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

DEPENDENCIES = [
    'django-cms-smartsnippets',
    'django-filer',
]


DEPENDENCY_LINKS = [
    'http://github.com/pbs/django-cms-smartsnippets/tarball/master#egg=django-cms-smartsnippets-0.5.0.dev',
]


setup(
    name='cmsplugin-image',
    version='1.1.0',
    description='PBS Image Field type for Django CMS',
    long_description=open(README_PATH, 'r').read(),
    author='PBS Audience Facing Team',
    author_email='tpg-pbs-userfacing@threepillarglobal.com',
    install_requires=DEPENDENCIES,
    dependency_links=DEPENDENCY_LINKS,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
)
