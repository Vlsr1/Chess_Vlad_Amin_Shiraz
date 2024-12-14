from setuptools import setup, find_packages

setup(
    name='chess_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-chess',
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'chess_server=chess_project.server:start_server',
            'chess_client=chess_project.client:main',
        ],
    },
)

