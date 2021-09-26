import csv
from HashMap import HashMap

location_names = HashMap()
""" An instance of class :class:`HashMap` """
with open('CSV/WGUPSDistances.csv') as distances_file:

    distance_data = csv.reader(distances_file, delimiter=',')
    """ 
    The file :download:`WGUPSDistances.csv <../../../src/CSV/WGUPSDistances.csv>` information is read into the 
    variable, then the csv data read in, is organized as a 2D :func:`list`. 
    
    .. note::
        The time-complexity of :func:`list` is O(N)
    """
    distance_data = list(distance_data)


def first_7_letters_to_ascii_value(text):
    """
    This converts the first 7 characters, including spaces if they exist, to a large integer comprised of all the ascii
    codes concatenated producing a unique dictionary key.

    .. note::
        The time-complexity of this method is O(1)

    :param string text: The string you would like to convert
    :return: ascii numbers concatenated
    """
    ascii_letters_to_encode = text[:7]
    return ''.join(str(ord(char)) for char in ascii_letters_to_encode)


with open('CSV/WGUPSPlacesOfDelivery.csv') as deliv_locations_file:
    locations = csv.reader(deliv_locations_file, delimiter=',')
    """ 
    The file :download:`WGUPSPlacesOfDelivery.csv <../../../src/CSV/WGUPSPlacesOfDelivery.csv>` information is read into the 
    variable, then the csv data read in is organized into :mod:`DataImporter.location_names`.
    
    .. note::
        Utilizing a HashMap of the locations was my attempt to minimize time complexity for lookup. The time complexity is O(N)
        
    """
    for location in locations:
        location_names.set(int(first_7_letters_to_ascii_value(location[2])), location)
