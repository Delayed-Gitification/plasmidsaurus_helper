from setuptools import setup

setup(
    name="plasmidsaurus_helper",
    version="0.2",
    description="A convenience tool for identifying low-confidence bases and reindexing fasta files from "
                "nanopore plasmid sequencing tools such as plasmidsaurus, full circle etc",
    author="Oscar Wilkins",
    author_email="oscar.wilkins@crick.ac.uk",
    packages=["plasmidsaurus_helper"],
    install_requires=["dnaio", "argparse"],
    entry_points={
        'console_scripts': [
            'plasmidsaurus_helper = plasmidsaurus_helper.main:main',
        ],
    },
)