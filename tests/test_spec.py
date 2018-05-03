
import unittest
from six import BytesIO
from tempfile import TemporaryFile

from marcextraction.lookup import MarcFieldLookup
from marcextraction.factories import ExtractorFactory

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def testLookupMainEntryPersonalNameIndexField(self):
        query = MarcFieldLookup("Main Entry - Personal name", "Personal name")
        self.assertEqual(query.show_index_field(), '100a')

    def testLookupCartographicMathDataCoordinates(self):
        query = MarcFieldLookup("Cartographic Mathemtical Data", "Statement of coordinates")
        self.assertEqual(query.show_index_field(), '255c')

    def testExtractFromDisk(self):
        """
        tests whether the following happens
        a.) the extractory builds the right extractor
        b.) the built extractor is able to extract the data from a file like object
        c.) the right available methods gets returned for retrieving the data  
        """
        extractor = ExtractorFactory('file_import').build()
        
        extracted_data = extractor.from_external_source(file_like_object)
        converted_data = extracted_data.to_dict()
        self.assertEqual(extractor.count(), 1)
        self.assertEqual(extractor.get_record_title(), "")
