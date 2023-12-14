import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
name='matcher',
version='0.0.1',
author='JaeHo Bahng',
author_email='jaeho127@gmail.com',
description='match names to score',
long_description=long_description,
long_description_content_type='text/markdown',
packages=setuptools.find_packages(),
python_requires='>=3.6',
extras_requres={"dev": ["pytest", "flake8", "autopep8"]},
)