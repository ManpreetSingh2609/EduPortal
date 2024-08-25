from setuptools import setup, find_packages

setup(
    name='EduPortal',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'selenium',
        'waitress'
        # Add other dependencies here
    ],
    # Other setup arguments
)