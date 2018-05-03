
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
                    if subfield.get("label") == sub_field_name:
                        sf = subfield.get("code")
                        break
        if mf and sf:
            return str(mf)+str(sf)
        else:
            return None

    def show_index_field(self):
        return self.index_field
