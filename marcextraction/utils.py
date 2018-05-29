"""utility functions for working with ole index data
"""

def create_ole_index_field(field_name):
    """a method to return the marc field name as entered in the OLE index

    Args:
        field_name (str): a MARC field number with a subfield code as a single string. Ex '245a'
    """
    return "mdf_{}".format(field_name)

def create_ole_query(field_name, query_term, phrase_term=False):
    """a method to return the query string for searching for making a field query in OLE

    Args:
        field_name (str): a MARC field combined with a subfield code with prefix 'mdf_. Ex. 'mdf_245a'.
        query_term (str): a word or phrase 

    Returns:
        str. A full query string to be entered into a Solr index for searching on a particular field. Ex. 'mdf_245a:banana'
    """
    if phrase_term:
        return "{}:\"{}\"".format(field_name, query_term)
    else:
        return "{}:{}".format(field_name, query_term)

def find_ole_bib_numbers(ole_data_list):
    """a method to find bib numbers from a set of OLE results

    Args:
        ole_data_list (list): a list of dictionaries containing output from a Solr search of an OLE index. 

    Returns:
        list. an iterable containing strings that should represent bib numbers. Ex. ['1000435999', '10045334500']
    """
    output = []
    for n_thing in ole_data_list:
        output += n_thing.get("controlfield")
    return output
