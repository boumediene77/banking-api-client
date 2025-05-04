from setuptools import setup, find_packages

setup(
    name="banking-api-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.7.0",
    ],
    python_requires=">=3.7",
    author="Boumediene MAROUF ",
    author_email="boumedienemar@gmail.com",
    description="A library to consume the Banking API",
    keywords="banking, api, client",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
