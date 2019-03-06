import csv

import geocoder


def filter_not_assigned_postcodes(canada_post_codes):
    """
    This function filters out not assigned postcodes.
    :param canada_post_codes: pd.DataFrame object with garbage postcodes
    :return: pd.DataFrame object without garbage
    """
    assigned_postcodes = canada_post_codes['Borough'] != 'Not assigned'
    return canada_post_codes[assigned_postcodes].reset_index(drop=True)


def name_not_assigned_neighborhoods(canada_post_codes):
    """
    In the DataFrame there can be boroughs with not
    assigned neighborhoods. In this case, we should set the name of
    the neighborhood same as one in the corresponding borough
    """
    not_assigned_neighborhoods = canada_post_codes['Neighbourhood'] == 'Not assigned'
    canada_post_codes.loc[not_assigned_neighborhoods, 'Neighbourhood'] = \
        canada_post_codes.loc[not_assigned_neighborhoods, 'Borough']

    return canada_post_codes


def combine_rows_with_same_postcode(canada_post_codes):
    """
    There might be several rows with the same postal code.
    This function groups this rows into one row and uses string join
    to combine neighborhoods.
    """
    grouped_post_codes = canada_post_codes.groupby(['Postcode', 'Borough'])
    return grouped_post_codes['Neighbourhood'].apply(', '.join).reset_index()

def get_latitude_longitude(postcode):
    """
    The function uses geocoder library to obtain latitude and
    longitude of the area from it's postal code.
    :param postcode: string with postal code of the area
    :return: tuple with latitude and longitude
    """
    latitude_longitude = None
    secure_counter = 10 # To avoid infinite loop
    while latitude_longitude is None and secure_counter:
        provider_response = geocoder.google('{}, Toronto, Ontario'.format(postcode))
        latitude_longitude = provider_response.latlng
        secure_counter -= 1
    if latitude_longitude is None: latitude_longitude = (0, 0)
    return latitude_longitude


def get_latitude_longitude_from_csv(postcode):
    """
    The function uses the proposed csv file with the coordinates to
    obtain latitude and longitude of the area from its postal code.
    :param postcode: string with postal code of the area
    :return: tuple with latitude and longitude
    """
    with open('Geospatial_Coordinates.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        pc_col, lat_col, lon_col = reader.fieldnames

        result = (0, 0)

        for row in reader:
            if row[pc_col] == postcode:
                result = (row[lat_col], row[lon_col])
                break

        return result


def get_nearby_venues(neighborhood, lat, lon)
    pass
