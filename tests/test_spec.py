
from os import remove, rmdir, getlogin, listdir
from os.path import join
from pymarc import Record, Field
import unittest
from six import BytesIO
from tempfile import TemporaryFile, TemporaryDirectory

from marcextraction.extractors.interfaces import SolrIndexSearcher, OnDiskSearcher
from marcextraction.lookup import MarcFieldLookup
from marcextraction.utils import create_ole_index_field, create_ole_query


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def testLookupMainEntryPersonalNameIndexField(self):
        query = MarcFieldLookup("Main Entry - Personal name", "Personal name")
        self.assertEqual(query.show_index_field(), '100a')

    def testLookupCartographicMathDataCoordinates(self):
        query = MarcFieldLookup(
            "Cartographic Mathematical Data", "Statement of coordinates")
        self.assertEqual(query.show_index_field(), '255c')

    def testExtractFromWriteableObject(self):
        """
        tests whether the following happens
        a.) the extractory builds the right extractor
        b.) the built extractor is able to extract the data from a file like object
        c.) the right available methods gets returned for retrieving the data  
        """

        record = Record()
        record.add_field(Field(tag='245', indicators=['0', '1'],
                               subfields=[
            'a', 'Test book :',
            'b', 'a simple test object /',
            'c', 'John Doe'])
        )
        flo = BytesIO(record.as_marc())
        extracted_data = OnDiskSearcher(writeable_object=flo)
        self.assertEqual(extracted_data.count(), 1)

    def testExtractFromDirectoryLocation(self):
        tempdir = TemporaryDirectory()

        record1 = Record()
        record1.add_field(Field(tag='245', indicators=['0', '1'],
                                subfields=[
                                'a', 'Test book :',
                                'b', 'a simple test object /',
                                'c', 'John Doe'])
                          )

        record2 = Record()

        record2.add_field(Field(tag='245', indicators=['0', '1'],
                                subfields=[
                                'a', 'Another test book :',
                                'b', 'a second test object /',
                                'c', 'Jane Doe'])
                          )
        with open(join(tempdir.name, 'file1.mrc'), 'wb') as write_file:
            write_file.write(record1.as_marc())
            write_file.seek(0)
        with open(join(tempdir.name, 'file2.mrc'), 'wb') as write_file:
            write_file.write(record2.as_marc())
            write_file.seek(0)
        searcher = OnDiskSearcher(location=tempdir.name)
        self.assertEqual(searcher.count(), 2)

    def testCreatingSolrIndexSearcher(self):
        searcher = SolrIndexSearcher(
            "http://olereport02.uchicago.edu:8180/solr/bib/", create_ole_index_field, create_ole_query)
        self.assertEqual(searcher.index_url,
                         'http://olereport02.uchicago.edu:8180/solr/bib/')

    def testSearchingOnDiscRecords(self):
        tempdir = TemporaryDirectory()

        record1 = Record()
        record1.add_field(Field(tag='245', indicators=['0', '1'],
                                subfields=[
                                'a', 'Test book :',
                                'b', 'a simple test object /',
                                'c', 'John Doe'])
                          )

        record2 = Record()

        record2.add_field(Field(tag='245', indicators=['0', '1'],
                                subfields=[
                                'a', 'Another test book :',
                                'b', 'a second test object /',
                                'c', 'Jane Doe'])
                          )
        with open(join(tempdir.name, 'file1.mrc'), 'wb') as write_file:
            write_file.write(record1.as_marc())
            write_file.seek(0)
        with open(join(tempdir.name, 'file2.mrc'), 'wb') as write_file:
            write_file.write(record2.as_marc())
            write_file.seek(0)

        searcher = OnDiskSearcher(location=tempdir.name)
        result = searcher.search(
            'John', 'Title Statement', 'Statement of responsibility, etc.')
        tempdir.cleanup()
        self.assertEqual(len(result), 1)

    def testSearchingVuFind(self):
        searcher = SolrIndexSearcher(
            "http://olereport02.uchicago.edu:8180/solr/bib/", create_ole_index_field, create_ole_query)
        results = searcher.search('Banana', "Title Statement", "Title")
        self.assertEqual(len(results), 10)
