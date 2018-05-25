
# marcExtraction

This is a Python library that allows a consumer to extract MARC records from 

1. a file exported to disk
1. a VuFind API

# Quick start

1. ```git cone git@github.com:uchicago-library/extract_marc_from_vufind```
1. ```cd extract_marc_from_vufind```
1. ```python -m venv venv```
1. ```source venv/bin/activate```
1. ```pip install -r requirements.txt```
1. ```python setup.py develop```

And you are ready to start hacking new functionality to the code base. Don't forget to follow good branching and open source citizen etiquette when you're doing it though!

# How to Use the Library


If you are looking to find some particular subset of a bunch of MARC records that you have on-disk, you can do something like the following.

```python
>>> from marcextraction.interfaces import OnDiskSearcher
>>> searcher = OnDiskSearcher(location='/path/to/a/bunch/of/marc/record/files')
>>> results = searcher.search('banana', '245', ['a'])
```

This example will do the following

1. Instantiate an instance of OnDiskSearcher with a list of valid MARC records at /path/to/a/bunch/of/marc/record/files
1. Perform a search on the MARC records for any record with banana in MARC field '245', subfield 'a'.

Still, you might be in an organization using OLE. In which case, you could do something like this.
```python
>>> from marcextraction.interfaces import SolrIndexSearcher
>>> searcher = SolrIndexSearcher('http://your.domain/path/to/index', 'ole', 'ole')
>>> results = searcher.search('banana', '245', ['a'], rows=100)
```
This example does the same thing as the earlier example except this time it's searching a SOLR index. 

If you want to extract a particular MARC record from OLE, do the following:

```python
>>> from marcextraction.interfaces import OLERecordFinder
>>> getter = OLERecordFinder(100134, 'domain.of.ole.sru.app', 'http', '/path/to/app'
>>> getter.get_record()
``````

## Internal Project Management

- [Brainstorming document](https://docs.google.com/document/d/18leMBOiPCnQujR2gOBjDCPajI7-t_AzWJxglH34QjFw/edit?usp=sharing)

## Additional Links

- [MARC21 Bibliographic Data]()https://www.loc.gov/marc/bibliographic/) for the field and subfield labels to use when looking up a particular field
- [readthedocs documentation](http://extract-marc-from-vufind.readthedocs.io/en/latest/index.html)

## Author

- verbalhanglider (tdanstrom@uchicago.edu)
