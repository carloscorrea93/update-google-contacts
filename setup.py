from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='update-google-contacts-mx',
    version='0.0.1',
    author='Carlos Correa',
    author_email='carlosx-34@hotmail.com',
    description='Script to update google contacts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/carloscorrea93/update-google-contacts',
    keywords=['google', 'contacts'],
    python_requires='>=3.8',
    install_requires=[],
)