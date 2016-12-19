"""
Setuptools file for jira_extended
"""
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='jira_extended',
    author='marhag87',
    author_email='marhag87@gmail.com',
    url='https://github.com/gillarkod/jira_extended',
    version='0.2.0',
    packages=find_packages(),
    license='MIT',
    description='Module that extends jira with additional functionality',
    long_description='Module that extends jira with additional functionality',
    install_requires=['jira'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
