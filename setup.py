import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

dependency_links = [
    'http://github.com/pbs/django-cms/tarball/support/2.3.x#egg=django-cms-2.3.5pbs',
    'http://github.com/pbs/django-filer/tarball/master_pbs#egg=django-filer-0.9pbs',
]

setup(
    name='cmsplugin-image',
    version='0.0.6',
    description='PBS Image Field type for Django CMS',
    long_description = open(README_PATH, 'r').read(),
    author='PBS Audience Facing Team',
    author_email='tpg-pbs-userfacing@threepillarglobal.com',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    setup_requires = ['s3sourceuploader',],
    dependency_links=dependency_links,
    install_requires=(
      'PIL',
      'Django>=1.3,<1.4.8',
      'django-polymorphic==0.2',
      'django-cms>=2.3.5pbs, <2.3.6',
      'django-filer>=0.9pbs, <0.9.1',
    ),
)
