# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucu-fit-intart1-adversarial_search",
    version="0.0.1",
    author="Agustín Castillo, Leonardo Val",
    author_email="agustin.castllo@ucu.edu.uy, lval@ucu.edu.uy",
    description="Adversarial search framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ucu-fit-intart1/adversarial_search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.5',
)
