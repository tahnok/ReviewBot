from setuptools import setup, find_packages

PACKAGE_NAME = "ReviewBot"
VERSION = "0.1"


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="ReviewBot, the automated code reviewer",
    author="Steven MacLeod",
    author_email="steven@smacleod.ca",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'reviewbot = reviewbot.celery:main'
        ],
        'reviewbot.tools': [
            'BuildBot = reviewbot.tools.buildbot:BuildBot',
            'pep8 = reviewbot.tools.pep8:pep8Tool',
        ],
    },
    install_requires=[
        'buildbot>=0.8.7',
        'celery>=3.0',
        'pep8>=0.7.0',
    ],)
