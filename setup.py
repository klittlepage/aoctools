# pylint: disable=missing-module-docstring

import setuptools

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='aoctools',
    author='Kelly Littlepage',
    author_email='kelly@klittlepage.com',
    description='A CLI for working with Advent of Code (AOC) problems',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/klittlepage/aoctools',
    download_url='https://github.com/klittlepage/aoctools/archive/0.2.0.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.25.0,<3',
        'python-dotenv>=0.15.0'
    ],
    extras_require={
        'dev': [
            'pylint',
            'mypy',
            'autopep8',
            'pre-commit',
            'wheel'
        ]
    },
    scripts=['bin/aoctools']
)
