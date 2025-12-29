from setuptools import setup, find_packages

setup(
    name="HVC_Neural_Data_Generator",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas"
    ],
    description="A tool to generate and plot neural data for HVC neurons",
    author="Fatima Di-a",
    url="https://github.com/FatimaDi-a/HVC-Neural-Data-Generator",
)
