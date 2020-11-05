from setuptools import setup, find_packages

setup(
    name="find-office-server",
    version="0.0.1",
    description="The server for FindOffice app",
    packages=find_packages(),
    install_requires=[
        'flask',
        'gunicorn',
        'fire'
    ],
)