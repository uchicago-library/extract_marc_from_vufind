
"""classes for performing MARC Field creation from label lookups
"""

from .constants import LOOKUP


class MarcFieldLookup:
    """a class meant to be used to transform lookups by label into MARC fields and subfields
    """

    def __init__(self, main_field_name, sub_field_name):
        """initializes an instance of the class MarcFieldLookup 

        Args:
            main_field_name (str): a field name label for a major MARC field
            sub_field_name (str): a sub field label for a sub field of the major MARC field defined main_field_name
        """
        self.index_field = self._find_main_field(
            main_field_name, sub_field_name)

    def _find_main_field(self, field_name, sub_field_name):
        """a private method to convert label lookups into field number and subfield code

        Args:
            field_name (str): a label for a MARC21 major field
            sub_field_name (str): a label for a MARC21 sub field associated with the field_name

        Returns:
            str. The proper MARC21 field code and subfield as a single string

            -- ("Main Entry Uniform Title, "Uniform Title") -> 130a
            -- ("Index Term-Genre/Form", "Non-focus term") -> 655b
        """ 
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
            value = str(mf)+str(sf)
            return value
        return "*"

    @staticmethod
    def show_valid_lookups(pretty_print=False):
        """a static method to allow programmers to view the labels to use for looking up fields and subfields

        .. code-block:: python
            mf = MarcFieldLookup
            lookups = mf.show_valid_lookups

        Kwargs:
            pretty_print (bool: Whether to prettify output with indents for subfields. Defaults to False.

        Returns:
            str. All the fields and subfields with labels for lookup
        """
        output = ""
        if pretty_print:
            for field in LOOKUP:
                if field.get("field", None):
                    output += "MARC Field: {} {}\n".format(field.get("field"), field.get("label"))
                    for subfield in field.get("subfields", []):
                        output += "\tSubfield: {} {}\n".format(
                            subfield.get("code"),
                            subfield.get("label"))
        else:
            for field in LOOKUP:
                if field.get("field", None):
                    output += "MARC Field: {} {}\n".format(field.get("field"), field.get("label"))
                    for subfield in field.get("subfields", []):
                        output += "Subfield: {} {}\n".format(
                            subfield.get("code"),
                            subfield.get("label"))
        return output

    def show_index_field(self):
        """method to show the generated index field from lookup

        .. code-block:: python
            MarcFieldLookup("Uniform Title", "Title").show_index_field()

        Returns:
            str. The proper MARC21 field code and subfield as a single string

            -- ("Main Entry Uniform Title, "Uniform Title") -> 130a
            -- ("Index Term-Genre/Form", "Non-focus term") -> 655b
        """
        return self.index_field
