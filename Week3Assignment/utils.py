def filter_not_assigned_postcodes(canada_post_codes):
    """
    This function filters out not assigned postcodes.
    :param canada_post_codes: pd.DataFrame object with garbage postcodes
    :return: pd.DataFrame object without garbage
    """
    assigned_postcodes = canada_post_codes['Borough'] != 'Not assigned'
    return canada_post_codes[assigned_postcodes]

