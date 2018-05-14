"""the interface classes to allow for building a list of records and/or searching for relevant records
"""

from abc import ABCMeta, abstractclassmethod, abstractmethod, abstractproperty
from io import BytesIO
from os import scandir, stat
from os.path import exists, isfile, isdir
from pymarc import MARCReader
from pymarc.exceptions import RecordLengthInvalid
from pysolr import Solr
from requests import get
from requests.exceptions import ConnectionError

from .constants import LOOKUP
from .lookup import MarcFieldLookup
from .utils import create_ole_index_field, create_ole_query

class SolrIndexSearcher:
    """a class to be used to search a Solr index for a query
    """
    def __init__(self, index_url, index_type):
        """initializes an instance of the class SolrIndexSearcher 

        Args:
            index_url (str): the URL to the SOLR index that will be queried.
            index_type (str): a flag indicating which type of index is being used. 
                Needed for being able to generate the correct index field name
 
        """
        try: # have to check if index_url inputted is a resolveable URL
            get(index_url, "head")
            self.solr_index = Solr(index_url)
            self.index_url = self.solr_index.url
            self.field_creator = self._build_field_definer(index_type)
            self.query_creator = self._set_query_creator(index_type)
        except ConnectionError:
            pass # not sure what to do if ConnectionError does happen. 
                 # it's a deal breaker. should be logged somehow.

    def _build_field_definer(self, flag):
        """a private method to build the field definition

         Args
            flag (str): an indicate of what the field is in the index
        """
        if flag == 'ole':
            return create_ole_index_field
        else:
            raise ValueError("invalid index_type {}".format(flag))

    def _set_query_creator(self, flag):
        """a private method to set the query_creator function of the instance

        Args
            flag (str): an indicato of what kind of query construction needs to be done
        """
        if flag == 'ole':
            return create_ole_query
        else:
            raise ValueError("invalid index type '{}' for query creation".format(flag))

    def search(self, query_term, query_field, query_subfield):
        """a method to run a search on the index for a particular value in a particular field

        Args:
            query_term (str): the string to be searched. This string will be stemmed in Solr searches.
            query_field: the label for the MARC21 field that you want to search in.
            query_subfield: the label for the relevant subfield of the MARC21 field that you want to search.

        Returns:
            list. An iterable containing dictionaries for each matching record in the Solr index 
                for the query_term, query_field, and query_subfield.
        """
        query = None
        result = []
        field_name = MarcFieldLookup(
            query_field, query_subfield).show_index_field()
        if field_name:
            query = self.query_creator(
                self.field_creator(field_name), query_term)
            result = self.solr_index.search(q=query)
        else:
            query = query_term
            result = self.solr_index.search(query)
        if result.hits > 0:
            self.total = result.hits
            print(self.total)
            self.records = [x for x in result]
            return self.records
        else:
            return []


class OnDiskSearcher:
    """a class to use for building up a list of exported MARC files at a particular location on-disk

    Useage:
        searcher  = OnDiskSeacher(location='/path/to/marc/records')
        searcher.search('Cartographic Mathematical Data', 'Spatial coordinates')


    """
    def __init__(self, writeable_object=None, location=None):
        if location and exists(location):
            self.records = self._build_list_of_records(location)
            self.total = len(self.records)
        elif writeable_object:
            validity, records = self._check_if_real_marc_record(
                writeable_object.read())
            self.records = records if validity else []
            self.total = len(records) if validity else 0
        self.errors = []

    def _check_if_real_marc_record(self, some_bytes):
        """a method to check of a chunk of bytes is in fact a MARC record

        Returns a tuple, first element is True|False evaluating whether it was a MARC record and
        second element is either None or a list of MARC records as dictionaries if first element is True

        :param some_bytes: a chunk of binary data

        :rtype tuple
        """
        try:
            with BytesIO(some_bytes) as read_file:
                reader = MARCReader(read_file)
                return (True, [record for record in reader])
        except RecordLengthInvalid:
            msg = "not a valid MARC record"
            self.errors.append(msg)
            return (False, None)

    def count(self):
        """a method to return the total number of records extracted

        Returns:
            int. total records found on-disk
        """
        return self.total

    def _find_marc_files(self, path):
        """a generator function to return a list of valid MARC records found from a particular location on-disk

        Args:
            path (str): a location on disk to a file or a directory

        Returns:
            generator. an interable containing MARC record objects 
        """
        for n_thing in scandir(path):
            if n_thing.is_dir():
                yield from self._find_marc_files(n_thing.path)
            elif n_thing.is_file():
                bytes_file = open(n_thing.path, 'rb')
                bytes_data = bytes_file.read()
                bytes_file.close()
                validity, data_package = self._check_if_real_marc_record(
                    bytes_data)
                if validity:
                    yield data_package

    def _build_list_of_records(self, path_on_disk):
        """a  method to get a list of MARC records transformed to dictionaries to allow for searching

        Args:
            path_on_disk (str): a particular location on-disk

        Returns:
            list. an iterable containing dictionaries representing MARC records
        """
        records = []
        if isdir(path_on_disk):
            for n_package in self._find_marc_files(path_on_disk):
                records += [x.as_dict() for x in n_package]
        elif isfile(path_on_disk):
            bytes_file = open(path_on_disk, 'rb')
            bytes_data = bytes_file.close()
            bytes_file.close()
            validity, data_package = self._check_if_real_marc_record(
                bytes_data)
            if validity:
                records += [record.as_dict() for record in data_package]
        return records

    def search(self, query_term, query_field, query_subfield):
        """a method to search for records matching query term and field lookup

        Args:
            query term (str): a word or phrase that should be present in relevant MARC records
            query_field (str): a valid MARC field label
            query_subfield (str): a valid MARC subfield label for a subfield associated with the MARC field entered

        Returns:
            list. an iterable contianing dicitonaries

        :rtype list
        """
        output = []
        field_name = MarcFieldLookup(
            query_field, query_subfield).show_index_field()
        if field_name:
            counter = 0
            for record in self.records:
                counter += 1
                for field in record.get("fields"):
                    if field.get(field_name[0:3]):
                        subfields = field.get(field_name[0:3]).get("subfields")
                        for subfield in subfields:
                            if subfield.get(field_name[-1]):
                                if query_term in subfield.get(field_name[-1]):
                                    output.append(record)
        return output

    @classmethod
    def from_flo(cls, flo):
        """a method to instantiate an instance of OnDiskExtractor from a file-like object

        Args:
            flo (File Object): a file-like object with read, write methods 

        Returns:
            OnDiskSearcher
        """
        return cls(writeable_object=flo)
