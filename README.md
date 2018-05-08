
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

## Internal Project Management

- [Brainstorming document](https://docs.google.com/document/d/18leMBOiPCnQujR2gOBjDCPajI7-t_AzWJxglH34QjFw/edit?usp=sharing)

## Author

- verbalhanglider (tdanstrom@uchicago.edu)