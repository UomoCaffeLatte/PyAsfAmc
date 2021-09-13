from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="asfamc-parser",
    version="0.0.1",
    description="generic asf/amc parser following standard version 1.1.",
    long_description_content_type="text/markdown",
    long_description=README,
    py_modules=["asfamcparser"],
    package_dir={"":"AsfAmcParser"},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries",
    ],
    url="https://github.com/UomoCaffeLatte/AMCParser",
    author="Nikhil Reji",
    author_email="Nikhil.Reji@live.co.uk",
)