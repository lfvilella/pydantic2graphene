import pathlib
import setuptools
import re


description = (
    "Easy way to convert pydantic2graphene models to graphene objects."
)
long_description = description

ROOT_DIR = pathlib.Path(__file__).resolve().parent
try:
    long_description = (ROOT_DIR / "README.md").read_text()
except FileNotFoundError:
    pass

version_txt = (ROOT_DIR / "pydantic2graphene" / "version.py").read_text()
version = re.search(r"v\d+(\.\d+)+", version_txt).group()

requirements = [
    "graphene>=1.1,<=2.1.9",
    "pydantic>=1.0,<=1.8.2",
]

github_url = "https://github.com/lfvilella/pydantic2graphene"

setuptools.setup(
    name="pydantic2graphene",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
    ],
    keywords=["python", "api", "graphql", "graphene", "pydantinc"],
    author="Luis Felipe Vilella",
    author_email="vilella.luisfelipe@gmail.com",
    url=github_url,
    download_url=f"{github_url}/archive/{version}.tar.gz",
    license="MIT",
    packages=["pydantic2graphene"],
    package_data={"pydantic2graphene": ["py.typed"]},
    python_requires=">=3.6,<=3.9",
    install_requires=requirements,
)
