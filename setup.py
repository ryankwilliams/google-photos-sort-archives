from setuptools import find_packages, setup

from google_photos_sort_archives import metadata

setup(
    name=metadata.__name__,
    version=metadata.__version__,
    description="A program to organize Google photos archives taken from "
                "Google Takeout",
    url="https://github.com/ryankwilliams/google-photos-sort-archives",
    author="Ryan Williams",
    license="GPLv3",
    install_requires=[
        "click>=7.0"
    ],
    packages=find_packages("."),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "google-photos-sort-archives=google_photos_sort_archives.cli:main"
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ]
)
