
from pymarc import Record, Field
import unittest
from six import BytesIO
from tempfile import TemporaryFile

from marcextraction.lookup import MarcFieldLookup
from marcextraction.factories import ExtractorFactory

class Tests(unittest.TestCase):
    def setUp(self):
        self.ondisk_extractor = ExtractorFactory("file_import").build()
        self.vufind_extractor = ExtractorFactory("vufind").build()

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

        record = Record()
        record.add_field(Field(tag='245', indicators=['0','1'],
                               subfields=[
                                'a','Test book :',
                                'b','a simple test object /',
                                'c','John Doe'])
        )
        flo = BytesIO(record.as_marc())
        extracted_data = self.ondisk_extractor.from_contract({"filo": flo})
        converted_data = extracted_data.to_dict()
        self.assertEqual(self.extractor.count(), 1)
        self.assertEqual(converted_data.get_record_title(), "")

    def testExtractFromVuFind(self):
        extracted_data = self.ondisk_extractor.from_contract(
            {
                "index_url": "http://",
            })
        extracted_data.search('245a', 'bananas')
        self.assertEqual(extracted_data.count(), 1)
        self.asssertEqual(extracted_data.get_record_title, "")
