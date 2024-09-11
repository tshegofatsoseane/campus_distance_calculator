from setuptools import setup, find_packages

setup(
    name='campus_distance_calculator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'googlemaps',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'calculate_distances=distance_calculator.main:calculate_distances',
        ],
    },
)
