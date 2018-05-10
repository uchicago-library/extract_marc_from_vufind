"""utility functions for working with ole index data
"""

def create_ole_index_field(field_name):
    """a method to return the marc field name as entered in the OLE index
    """
    return "mdf_{}".format(field_name)

def create_ole_query(field_name, query_term):
    """a method to return the query string for searching for making a field query in OLE
    """
    return "{}:{}".format(field_name, query_term)

def find_ole_bib_numbers(ole_data_list):
    """a method to find bib numbers from a set of OLE results
    """
    output = []
    for n_thing in ole_data_list:
        output += n_thing.get("controlfield")
    return output
