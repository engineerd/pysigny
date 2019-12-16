from setuptools import setup

setup(
    name='pysigny',
    version='0.0.1',
    py_modules=['pysigny'],
    install_requires=[
        'Click',
        'securesystemslib',
        'tuf'
    ],
    entry_points='''
        [console_scripts]
        pysigny=pysigny:cli
    ''',
)
