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
