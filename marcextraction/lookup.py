
"""classes for performing MARC Field creation from label lookups
"""

from .constants import LOOKUP


class MarcFieldLookup:
    """a class meant to be used to transform lookups by label into MARC fields and subfields
    """

    def __init__(self, field=None, field_label=None, subfield=None, subfield_label=None):
        """initializes an instance of the class MarcFieldLookup 

        KWArgs:
            field_label (str): a field name label for a major MARC field
            subfield_label (str): a sub field label for a sub field of the major MARC field defined main_field_name
            field (str): a field name label for a major MARC field
            subfield (str): a sub field label for a sub field of the major MARC field defined main_field_name
        """
        if field_label and subfield_label:
            self.index_field = self._find_main_field_by_label(field_label, subfield_label)
        elif field and subfield:
            self.index_field = self._find_main_field_by_code(field, subfield)
        elif field:
            self.index_field = self._find_all_subfields_by_field(field)
        elif field_label:
            self.index_field = self._find_all_subfields_by_field_label(field_label)
        else:
            self.index_field = self._find_all_fields()

    def _find_all_fields(self):
        output = []
        for a_dict in LOOKUP:
            field = a_dict.get("field")
            if a_dict.get("subfields"):
                for subfield in a_dict.get("subfields"):
                    a_param = "{}{}".format(field, subfield.get("code"))
                    output.append(a_param)
        return output

    def _find_a_field(self, label=None, number=None):
        if label:
            field = [x for x in LOOKUP if x.get("label") == label]
            err_msg = "no field found for {}".format(field)
        elif number:
            field = [x for x in LOOKUP if x.get("field") == number]
            err_msg = "no field found for {}".format(label)
        if field: 
            subfields = field[0].get("subfields")
            if not subfields:
                err_msg = "no subfields defined for field {}".format(field.get("field"))
                raise ValueError(err_msg)
            else:
                return (field[0].get("field") , field[0].get("subfields"))
        else:
            raise ValueError(err_msg)

    def _find_a_subfield(self, subfield_list, label=None, code=None):
        if label:
            subfield = [x for x in subfield_list if x.get("label") == label]
            err_msg = "no subfield field found for {}".format(label)
        elif code:
            subfield = [x for x in subfield_list if x.get("code") == label]
            err_msg = "no subfield field found for {}".format(code)
        if subfield:
            return subfield[0].get("code")
        else:
            raise ValueError(err_msg)
        

    def _find_all_subfields_by_field_label(self, field_label):
        output = []
        field, subfields = self._find_a_field(label=field_label)
        for n_subfield in subfields:
            sf_code = n_subfield.get("code")
            a_param = "{}{}".format(field, sf_code)
            output.append(a_param)
        return output

    def _find_all_subfields_by_field(self, field):
        output = []
        field, subfields = self._find_a_field(number=field)
        for n_subfield in subfields:
            sf_code = n_subfield.get("code")
            a_param = "{}{}".format(field, sf_code)
            output.append(a_param)
        return output

    def _find_main_field_by_code(self, field, subfield):
       field, subfields = self._find_a_field(number=field)
       subfield = self._find_a_subfield(subfields, code=subfield)
       return ["{}{}".format(field, subfield)]

    def _find_main_field_by_label(self, field_name, sub_field_name):
        """a private method to convert label lookups into field number and subfield code

        Args:
            field_name (str): a label for a MARC21 major field
            sub_field_name (str): a label for a MARC21 sub field associated with the field_name

        Returns:
            str. The proper MARC21 field code and subfield as a single string

            -- ("Main Entry Uniform Title, "Uniform Title") -> 130a
            -- ("Index Term-Genre/Form", "Non-focus term") -> 655b
        """ 
        field, subfields = self._find_a_field(label=field_name)
        subfield = self._find_a_subfield(subfields, label=sub_field_name)
        return ["{}{}".format(field, subfield)]

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

    def show_index_fields(self):
        """method to show the generated index field from lookup

        .. code-block:: python
            MarcFieldLookup("Uniform Title", "Title").show_index_field()

        Returns:
            str. The proper MARC21 field code and subfield as a single string

            -- ("Main Entry Uniform Title, "Uniform Title") -> 130a
            -- ("Index Term-Genre/Form", "Non-focus term") -> 655b
        """
        return self.index_field
