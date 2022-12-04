from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # Package name:
    name="qrypto",

    # Package number (initial):
    version="0.0.1",

    # Package author details:
    author="Adrián Muñoz Perera, Jorge Rivero Dones",
    author_email="pereradrian@gmail.com, jorivero83@gmail.com",

    # Packages
    packages=["qrypto"],

    # Include additional files into the package
    include_package_data=False,

    # Details
    url="https://github.com/pereradrian/qrypto",

    #
    # license="LICENSE.txt",
    description="A package to download data from www.coinmarketcap.com",

    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LICENSE',

    # Dependent packages (distributions)
    install_requires=[
        "typing==3.7.4.3",
        "numpy==1.21.6",
        "requests==2.28.1",
        "dateparser==1.1.4",
        "pandas==1.3.5"
    ],
)