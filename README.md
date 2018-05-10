
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

To see the field and subfield labels to use when searching for a particular MARC field, follow the instructions below.

```python
>>> from marcextraction import MarcFieldLookup
>>> mf = MarcFieldLookup
>>> mf.show_valid_lookups()
MARC Field Number: Main Entry - Personal name
        Subfield: Personal name
        Subfield: Numeration
        Subfield: Title and words associated with name
        Subfield: Dates associated with name
        Subfield: Relator term
        Subfield: Date of a work
        Subfield: Miscellaneous information
        Subfield: Attribution qualifier
        Subfield: Form subheading
        Subfield: Language of a work
        Subfield: Number of part/section of a work
        Subfield: Name of part/section work
        Subfield: Fuller form of name
        Subfield: Title of a work
        Subfield: Affiliation
        Subfield: Authority record control number or standard number
        Subfield: REal World Object URI
        Subfield: Relationship
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Main Entry - Corporate Name
        Subfield: Corporate name or jurisdiction name as entry element
        Subfield: Subordinate unit
        Subfield: Location of meeting
        Subfield: Date of meeting or treaty signing
        Subfield: Relator term
        Subfield: Date of a work
        Subfield: Miscellaneous information
        Subfield: Language of a work
        Subfield: Number of part/section/meeting
        Subfield: Name of part/section of a work
        Subfield: Title of a work
        Subfield: Affiliation
        Subfield: Authority record control number or standard number
        Subfield: Real World Object URI
        Subfield: Linkage
        Subfield: Field link and sequence identifier
MARC Field Number: Main Entry - Meeting Name
        Subfield: Meeting name or jurisdiction name as entry element
        Subfield: Location of meeting
        Subfield: Date of meeting or treaty signing
        Subfield: Subordinate unit
        Subfield: Date of a work
        Subfield: Miscellaneous information
        Subfield: Form subheading
        Subfield: Language of a work
        Subfield: Number of part/section/meeting
        Subfield: Name of a part/section of a work
        Subfield: Name of meeting following jurisdiction name entry element
        Subfield: Title of a work
        Subfield: Affiliation
        Subfield: Authority record control number or standard number
        Subfield: Real World Object URI
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Main Entry - Uniform Title
        Subfield: Uniform title
        Subfield: Date of treaty signing
        Subfield: Date of work
        Subfield: Miscellaneous information
        Subfield: Medium
        Subfield: Form subheading
        Subfield: Language of a work
        Subfield: Medium of performance for music
        Subfield: Number of part/section of a work
        Subfield: Arranged statement for music
        Subfield: Name of part/section of a work
        Subfield: Key for music
        Subfield: Version
        Subfield: Title of a work
        Subfield: Authority record control number or standard number
        Subfield: Real World Object URI
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Abbreviated Title
        Subfield: Abbreviated title
        Subfield: Qualifying information
MARC Field Number: Key Title
        Subfield: Key title
        Subfield: Qualifying information
        Subfield: Linkage
        Subfield: Field lnk and sequence number
MARC Field Number: Uniform Title
        Subfield: Uniform title
        Subfield: Date of treaty signing
        Subfield: Date of work
        Subfield: Miscellaneous information
        Subfield: Medium
        Subfield: Form subheading
        Subfield: Language of a work
        Subfield: Medium of performance for music
        Subfield: Number of part/section of a work
        Subfield: Arranged statement for music
        Subfield: Name of part/section of a work
        Subfield: Key for music
        Subfield: Version
        Subfield: Authority record control number or standard number
        Subfield: Real World Object URI
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Translation of Titlte by Cataloging Agency
        Subfield: Title
        Subfield: Remainder of title
        Subfield: Statement of responsibility
        Subfield: Medium
        Subfield: Number of part/section of a work
        Subfield: Name of part/section of a work
        Subfield: Language of code translated title
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Collection Uniform Title
        Subfield: Uniform title
        Subfield: Date of treaty signing
        Subfield: Date of a work
        Subfield: Miscellaneous information
        Subfield: Medium
        Subfield: Form subheading
        Subfield: Language of a work
        Subfield: Medium of performance music
        Subfield: Number of part/section of a work
        Subfield: Arrange statement for music
        Subfield: Name of part/section of a work
        Subfield: Key for music
        Subfield: Version
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Title Statement
        Subfield: Title
        Subfield: Remainder of title
        Subfield: Statement of responsibility
        Subfield: Inclusive dates
        Subfield: Buk dates
        Subfield: Medium
        Subfield: Form
        Subfield: Number of part/section of a work
        Subfield: Name of part/section of a work
        Subfield: Version
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Varying Form of Title
        Subfield: Title proper/short title
        Subfield: Remainder of title
        Subfield: Date or sequential designation
        Subfield: Miscellaneous information
        Subfield: Medium
        Subfield: Display text
        Subfield: Number of part/section of a work
        Subfield: Name of part/section of a work
        Subfield: Institution to which field applies
        Subfield: Linkage
        Subfield: Field link and sequence number
MARC Field Number: Former Title
```

In order to get the index field name for Uniform Title:

```python
>>> from marcextraction.lookup import MarcFieldLookup
>>> mf = MarcFieldLookup("Main Entry - Uniform Title", "Uniform title")
>>> mf.show_index_field()
130a
```

If on the other hand you are looking to find some particular subset of a bunch of MARC records that you have on-disk, you can do something like the following.

```python
>>> from marcextraction.extractors.interfaces import OnDiskSearcher
>>> searcher = OnDiskSearcher(location='/path/to/a/bunch/of/marc/record/files')
>>> results = searcher.search('banana', 'Title Statement', 'Title')
```

This example will do the following

1. Instantiate an instance of OnDiskSearcher with a list of valid MARC records at /path/to/a/bunch/of/marc/record/files
1. Perform a search on the MARC records for any record with banana in MARC field '245', subfield 'a'.

Still, you might be in an organization using OLE. In which case, you could do something like this.

```python
>>> from marcextraction.extractors.interfaces import VuFindSearcher
>>> searcher = SolrIndexSearcher('http://your.domain/path/to/index', create_ole_index_field, create_ole_query)
>>> results = searcher.search('banana', 'Title Statement', 'Title')
```
This example does the same thing as the earlier example except this time it's searching a SOLR index. 

If you want get the bib numbers for a particular set of results from am OLE index search, you should do the following.

```python
>>> from marcextraction.extractors.interfaces import VuFindSearcher
>>> searcher = SolrIndexSearcher('http://your.domain/path/to/index', create_ole_index_field, create_ole_query)
>>> results = searcher.search('banana', 'Title Statement', 'Title')
>>> results = find_ole_bib_numbers(results)
```

## Internal Project Management

- [Brainstorming document](https://docs.google.com/document/d/18leMBOiPCnQujR2gOBjDCPajI7-t_AzWJxglH34QjFw/edit?usp=sharing)

## Additional Links

- [MARC21 Bibliographic Data]()https://www.loc.gov/marc/bibliographic/) for the field and subfield labels to use when looking up a particular field
## Author

- verbalhanglider (tdanstrom@uchicago.edu)