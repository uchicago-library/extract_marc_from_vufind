
from .constants import LOOKUP

class MarcFieldLookup:
    def __init__(self, main_field_name, sub_field_name):
        self.index_field = self._find_main_field(main_field_name, sub_field_name)

    def _find_main_field(self, field_name, sub_field_name):
        field = [x for x in LOOKUP if x.get("label") == field_name]
        mf = None
        sf = None
        if field:
            for n in field:
                mf = n.get("field")
                for subfield in n.get("subfields"):
                    print(subfield)
                    if subfield.get("label") == sub_field_name:
                        sf = subfield.get("code")
                        break
        if mf and sf:
            value = str(mf)+str(sf)
            return value

    @staticmethod
    def show_valid_lookups(pretty_print=True):
        if pretty_print:
            for field in LOOKUP:
                if field.get("field", None):
                    print("MARC Field: {}".format(field.get("label")))
                    for subfield in field.get("subfields", []):
                        print("\tSubfield: {}".format(subfield.get("label")))
        else:
            for field in LOOKUP:
                if field.get("field", None):
                     print("MARC Field: {}".format(field.get("label")))
                     for subfield in field.get("subfields", []):
                        print("Subfield: {}".format(subfield.get("label")))
 

    def show_index_field(self):
        return self.index_field
