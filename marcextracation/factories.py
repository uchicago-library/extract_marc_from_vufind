
from .extractors import VuFindExtractor, OnDiskExtractor

class ExtractorFactory:
    def __init__(self, choice):
        self.request = choice

    def build_extractor(self):
        if self.request == 'vufind':
            return VuFindExtractor()
        elif self.request == 'file_import':
            return OnDiskExtractor()
        else:
            raise TypeError("factory can only build extractors for vufind or file_import")
    