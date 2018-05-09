import sys
from os.path import dirname, join
from pip.req import parse_requirements
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'hsstock/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]


setup(
    name='HSStock',
    version=version,
    description='HS Quantum Exchange',
    author='HU Jiabao',
    author_email='',
    scripts=[''],
    classifiers=[],
    keywords='Quantum Exchange',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements,
    url='',
    license='Apache License 2.0',
    package_data={'': ['*.*']},
    include_package_data=True,
    zip_safe=True,
    project_urls={
        "Bug Tracker": "",
        "Documentation": "",
        "Source Code": "",
    },
    #entry_points={'blogtool.parsers': '.rst = some_module:SomeClass'},
    #python_requires,
    #setup_requires
    #dependency_links
    #namespace_packages
    #test_suite
    #test_require
    #test_loader
    #eager_resources
    #use_2to3
    #covert_2to3_doctests
    #use_2to3_fixers
)
