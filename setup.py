from setuptools import setup, find_packages

setup(
    name='dependency_grapher',
    version='0.1.1',
    author='Shawn Crosby',
    author_email='scrosby@salesforce.com',
    packages=find_packages(),
    license='Keep it real',
    description='Graph Dependencies',
    long_description=open('README.txt').read(),
    scripts=[
             'bin/team_dependencies.py',
             'bin/release_dependencies.py'],
    install_requires=[
        "gus_client >= 0.2.5",
        "pyparsing == 1.5.7",
        "pydot",
    ],
)