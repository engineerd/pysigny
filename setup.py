import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name="pysigny",
    version="0.0.1",
    author="Radu Matei",
    author_email="root@radu.sh",
    description="Python reference implementation for CNAB Security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license,
    url="https://github.com/engineerd/pysigny",
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'click>=7.0',
        'securesystemslib>=0.12.0',
        'tuf>=0.12.1',
    ],
    entry_points={'console_scripts': ['pysigny=pysigny.pysigny:cli']},
)