import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandaspgs",
    version="0.9.0",
    author="Cao Tianze",
    author_email="hnrcao@qq.com",
    description="A Python package for easy retrieval of PGS Catalog data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caotianze/pandaspgs",
    project_urls={
        "Bug Tracker": "https://github.com/caotianze/pandaspgs/issues",
    },
    classifiers=[
        "Development Status :: 4 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['pandaspgs'],
    python_requires=">=3.10",
    install_requires=['pandas>=1.5.3', 'requests>=2.28.1', 'progressbar2>=4.2.0', 'cachetools>=5.3.0'],
    license="MIT",
    keywords=['pgs', 'genomics', 'snp', 'bioinformatics','pandas'],
    package_data={
        "": ["*.csv","*.txt"]
    }
)
