import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autogamess",
    version="0.0.5",
    author="Brian C. Ferrari",
    author_email="brianf1996@knights.ucf.edu",
    description="This is a python module for automating Raman calculations using GAMESS(us).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cavenfish/autogamess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
