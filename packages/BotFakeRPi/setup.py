#!/usr/bin/env python
from setuptools import setup


setup(
    name='bot_fake_rpi',
    version='0.1',
    author='Tiago & Abid',
    author_email='Tiago_caza@hotmail.com',
    description=(
        'Develop for Raspberry Pi on Windows or other systems '
        'that don\'t have RPi.GPIO libraries.'),
    long_description=open('README.md').read(),
    keywords='GPIO, RPi, Bot_Fake_RPi',
    include_package_data=True,
    packages=['BotFakeRPi'],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Hardware'],
    install_requires=['numpy']
)
