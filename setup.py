from os import path
import os
from codecs import open
from setuptools import setup, find_packages
import os.path
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, './README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the requirements
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = list(set(f.read().split('\n')) - set(['', '\n']))


# Get the requirements
with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()


setup(
    name='instabotnet',
    version=version,

    description='Instagram readable yaml rpc api for easy instagram scheduling and promotion',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Tommaso De Rossi',
    author_email='daer.tommy@gmail.com',
    license='Apache Software License 2.0',

    url='https://github.com/rpc-botnets/instagram-botnet',
    keywords=['instagram', 'bot', 'api', 'botnet'],
    install_requires=[
        *requirements,
    ],
    package_data={'': ['*.yaml', '*.json', '*.yml']},
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        # 'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Information Technology',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['instabotnet'],
)

