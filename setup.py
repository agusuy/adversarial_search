# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucu-fit-intart1-adversarial_search",
    version="0.0.1",
    author="Agustín Castillo, Leonardo Val",
    author_email="agustin.castllo@ucu.edu.uy, lval@ucu.edu.uy",
    description="A small example package",
    long_description="Adversarial search framework used in course 'Inteligencia Artificial 1' at UCU",
    long_description_content_type="text/markdown",
    url="https://github.com/ucu-fit-intart1/adversarial_search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)