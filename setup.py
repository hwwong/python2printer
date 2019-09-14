import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python2printer",
    version="0.0.1",
    author="HW Wong",
    author_email="hw_wong168@yahoo.com.hk",
    description="Direct output text or drawing to printer with Python code directly!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hwwong/python2printer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Windows :: OS Independent",
    ],
    python_requires='>=3.6',
)