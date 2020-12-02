from setuptools import setup, find_packages


with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='wumpus',
    version='0.0.1',
    description='Generic grid game framework for wumpus',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Guillem Pitarch Rodrigo',
    author_email='guipirod@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6', install_requires=['pytest']
)
