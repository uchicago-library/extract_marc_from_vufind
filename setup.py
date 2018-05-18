from setuptools import setup

setup(
    name="marcExtraction",
    author="Tyler Danstrom",
    author_email="tdanstrom@uchicago.edu",
    version="0.5.0",
    license="LGPL3.0",
    description="An application to extract MARC records from the catalog",
    keywords="python3.6 iiif-presentation manifests marc",
    packages=['marcextraction'],
    classifiers=[
        "License :: OSI Approved :: GNU Library or Lesser " +
        "General Public License (LGPL)",
        "Development Status :: 5 - Alpha/Prototype",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires = [
	'lxml',
        'pymarc',
        'pysolr',
        'requests'
    ]
)
