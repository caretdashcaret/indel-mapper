from setuptools import setup, find_packages

setup(
    name='indel-mapper',

    version='0.1',

    description='A Python project to visualize indels near Cas9 cutsites.',
    long_description='This package uses a SAM (Sequence Alignment Map) file and a reference CSV with the reference, N20, and PAM to output all the indels directly next to the Cas9 cutsite.',

    url='https://github.com/caretdashcaret/indel-mapper',

    author='Jenny Cheng and Harry Schwartz',
    author_email='jenny@caretdashcaret.com',

    license='GPLv3+',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],

    install_requires=['pysam'],

    packages=find_packages(exclude=["tests"]),

    entry_points={
        # For script, install indelmapper.py's main as indelmapper
        'console_scripts': [
            'indel-mapper=indel_mapper_lib.cmdline:main',
        ],
    },

    keywords=['crispr cas9 indels'],

    python_requires='>=3',
)
