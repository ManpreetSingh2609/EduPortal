from setuptools import setup, find_packages

setup(
    name='EduPortal',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'selenium',
        'multiprocessing'
        # Add other dependencies here
    ],
    # Other setup arguments
)