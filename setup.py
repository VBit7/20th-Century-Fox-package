from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='foxbot',
    version='2.0.1',
    description='Implement personal contacts terminal bot',
    url='https://github.com/onikitenko12/20th-Century-Fox.git',
    author='20th Century Fox',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",    
    license='MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['foxbot = foxbot.main:main']},
)
