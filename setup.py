import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')

DEPENDENCIES = [
      'PIL>=1.1.7',
      'Django>=1.3,<1.4.8',
      'django-polymorphic==0.2',
      'django-cms>=2.3.5pbs, <2.3.6',
      'django-filer>=0.9pbs, <0.9.1',
      'django-cms-smartsnippets>=0.1.21',
      'django-admin-extend>=0.0.1',
]

DEPENDENCY_LINKS = [
    'http://github.com/pbs/django-cms/tarball/support/2.3.x#egg=django-cms-2.3.5pbs',
    'http://github.com/pbs/django-filer/tarball/master_pbs#egg=django-filer-0.9pbs',
    'git+ssh://git@github.com/pbs/django-cms-smartsnippets.git#egg=django-cms-smartsnippets-0.1.21',
    'git+ssh://git@github.com/pbs/django-admin-extend.git#egg=django-admin-extend-0.0.1',
]

setup(
    name='cmsplugin-image',
    version='0.0.7',
    description='PBS Image Field type for Django CMS',
    long_description = open(README_PATH, 'r').read(),
    author='PBS Audience Facing Team',
    author_email='tpg-pbs-userfacing@threepillarglobal.com',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    setup_requires = ['s3sourceuploader',],
    dependency_links=DEPENDENCY_LINKS,
    install_requires=DEPENDENCIES,
)
