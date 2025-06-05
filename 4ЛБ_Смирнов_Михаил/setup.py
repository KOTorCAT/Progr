from setuptools import setup, find_packages

setup(
    name="currency_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'jinja2>=3.1.2'
    ],
)   