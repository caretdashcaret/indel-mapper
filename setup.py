from setuptools import setup

setup(
    name='indel-mapper',

    version='0.1',
    scripts=['indel-mapper']

    description='A Python project to visualize indels near Cas9 cutsites.'
    long_description='This package uses a SAM (Sequence Alignment Map) file and a reference CSV with the reference, N20, and PAM to output all the indels directly next to the Cas9 cutsite.'


)
