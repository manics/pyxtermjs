#!/usr/bin/env python3

from setuptools import find_packages, setup  # noqa E402

EXCLUDE_FROM_PACKAGES = ["tests"]


with open("README.md") as f:
    README = f.read()


VERSION = "0.1.0"


setup(
    name="terminado-single",
    version=VERSION,
    author="Simon Li",
    author_email="orpheus+devel@gmail.com",
    description="interactive terminal in the browser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cs01/pyxtermjs",
    license="License :: OSI Approved :: MIT License",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=[
        "xterm",
        "xterm.js",
        "javascript",
        "terminal-emulators",
        "browser",
        "tty",
        "pty",
        "console",
        "terminal",
    ],
    entry_points={"console_scripts": ["terminado = terminado_single.app:main"]},
    extras_require={},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["terminado>=0.9.0, <1.0.0"],
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
