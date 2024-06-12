from setuptools import setup, find_packages

setup(
    name='distance_calculator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'googlemaps',
        'django',
    ],
    entry_points={
        'console_scripts': [
            'calculate_distances=distance_calculator.cli:calculate_distances',
        ],
    },
)
