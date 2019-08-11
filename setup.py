from setuptools import setup


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version='0.4.1'

setup(
    name='geotools',
    version=version,
    author='Yruama42',
    author_email='amauryval@gmail.com',
    download_url='https://github.com/yruama42/geo_tools',
    install_requires=requirements,
    license='GPL V3'
)