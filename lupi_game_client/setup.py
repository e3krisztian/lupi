# coding: utf-8

"""
    Lupi Game API

    # Least Unique Positive Integer (Lupi)  Lupi is a fun game, that has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.  ## The Rules of the Game  - Lupi is a multiplayer game - each player picks a positive integer - the lowest unique integer wins   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "lupi-game-client"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Lupi Game API",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Lupi Game API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Unlicense",
    long_description="""\
    # Least Unique Positive Integer (Lupi)  Lupi is a fun game, that has been studied a lot and has some maths behind how people behave and what really is optimal in some respect.  ## The Rules of the Game  - Lupi is a multiplayer game - each player picks a positive integer - the lowest unique integer wins   # noqa: E501
    """
)
