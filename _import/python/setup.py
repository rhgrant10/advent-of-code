import setuptools

setuptools.setup(
    name="aoc",
    version="0.1.0",
    url="https://github.com/rhgrant10/advent-of-code_python",

    author="Robert Grant",
    author_email="rhgrant10@gmail.com",

    description="Advent of Code solutions in Python.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'advent-of-code-data==0.4.2',
    ],

    entry_points={
        'console_scripts': [
            'aoc=aoc.__main__:main',
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
