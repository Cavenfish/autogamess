import setuptools

setuptools.setup(
    name="autogamess",
    version="1.1.56",
    author="Brian C. Ferrari",
    author_email="brianf1996@knights.ucf.edu",
    description="This is a python module for automating Raman calculations using GAMESS(us).",
    url="https://github.com/Cavenfish/autogamess",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "pandas", "basis_set_exchange", "PeriodicElements",
                      "openpyxl", "matplotlib", "xlrd", "xlsxwriter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
