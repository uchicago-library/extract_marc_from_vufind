
from abc import ABCMeta, abstractclassmethod, abstractmethod, abstractproperty
from os import scandir
from os.path import exists, isfile, isdir
from pymarc import MARCReader
from pymarc.exceptions import RecordLengthInvalid
from pysolr import Solr
from requests import get
from requests.exceptions import ConnectionError

from ..constants import LOOKUP
from ..lookup import MarcFieldLookup

class Extractor(object, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_dict(self, input_dict):
        raise NotImplementedError

    @abstractmethod
    def search(self):
        raise NotImplementedError

class VuFindExtractor(Extractor):
    def __init__(self, index_url, query_term, query_field=None, query_subfield=None):
        try:
            get(index_url, "head")
            self.solr_index = Solr(index_url)
        except:
            ConnectionError
        if query_field and query_subfield and query_term:
            self.field_term = MarcFieldLookup(query_field, query_subfield).show_index_field()
        self.query_term = query_term

    def search(self):
        query = None
        result = []
        if self.field_term:
            query = "mdf_{}:{}".format(self.field_term, self.query_term)
            result = self.solr_index.search(q=query)
        else:
            query = self.query_term
            result = self.solr_index.search(query)
        if result.hits > 0:
            return [item for sublist in x['controlfield_001'] for x in result for item in sublist]
        else:
            return []

    def from_dict(self, input_dict):
        pass


class OnDiskExtractor(Extractor):
    def __init__(self, location, query_field=None, query_subfield=None, query_term=None):
        if exists(location):
            self.records = self._build_list_of_records(location)
        else:
            raise ValueError("invalid location value")
        if query_field and query_subfield and query_term:
            self.field_term = MarcFieldLookup(query_field, query_subfield).show_index_field()
            self.query_term = query_term
        self.errors = []

    def _check_if_real_marc_record(self, some_path):
        reader = None
        try:
            with open(some_path, 'rb') as opened_file:
                reader = MARCReader(opened_file)
                return (True, [record for record in reader])
        except RecordLengthInvalid:
            msg = "{} is not a valid MARC record".format(some_path)
            self.errors.append(msg)
            return (False, None)

    def _find_marc_files(self, path):
        for n_thing in scandir(path):
            if n_thing.isdir():
                yield from self._find_marc_files(n_thing.path)
            elif n_thing.isfile():
                validity, data_package = self._check_if_real_marc_record(n_thing.path)
                if validity:
                    yield data_package

    def _build_list_of_records(self, path_on_disk):
        records = []
        if isdir(path_on_disk):
            for n_package in self._find_marc_files(path_on_disk):
                records += [x.as_dict() for x in n_package] 
        elif isfile(path_on_disk):
            validity, data_package = self._check_if_real_marc_record(path_on_disk)
            if validity:
                records += [record.as_dict() for record in data_package]
        self.records = records

    def search(self):
        record = None
        for record in self.records:
            for field in record.get("fields"):
                if field == self.field_term[0:3]:
                    subfields = record.get("fields").get(self.field_term[0:3]).get("subfields")
                    for subfield in subfields:
                        if subfield.get(self.field_term[-1]):
                            if subfield.get(self.field_term[-1]) == self.query_term:
                                break
        return record
