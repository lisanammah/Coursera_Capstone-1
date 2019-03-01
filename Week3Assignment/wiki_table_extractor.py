class WikiTableExtractor:
    """
    Class to extract the table from a wiki page

    This class thoroughly relies on python duck-typing. page_content is assumed to
    be an instance of the BeautifulSoup class.

    Other assumptions:
    1. There is only one table on the page
    2. There is only one titles row in the table or no titles at all
    3. The titles row (if there is one) is the first in the table
    4. All rows of the table have the same length

    How to use it:
    1. Use requests(or similar) and BeautifulSoup library to download and
       parse the page
    2. Create an instance, using the constructor
    3. Call the method: instance.parse_table_from_page(YourBeautifulSoupInstance)
    4. Use instance.table attribute to work with extracted table

    """
    def __init__(self):
        self.table = Table()

    def parse_table_from_page(self, page_content):
        """
        Call this method to fill the table instance of the class.

        Use preliminary instantiated BeautifulSoup object as an argument.
        """
        table_content = page_content.find('table', {'class': 'wikitable sortable'})
        self.table.titles = self._get_titles(table_content)
        self.table.rows = self._get_rows(table_content)
        self.table._check_table()

    @staticmethod
    def _get_titles(table_content):
        # 'th' is html tag that defines Table Header (column name)
        title_elements = table_content.find_all('th')

        if title_elements:
            titles_dumped = [title_element.get_text() for title_element in title_elements]
            titles = [title_dumped.rstrip('\n\r').strip()
                      for title_dumped in titles_dumped]
        else:
            titles = []

        return titles

    @staticmethod
    def _get_rows(table_content):
        rows = []
        # 'tr' is an html tag that defines a Table Row
        row_elements = table_content.find_all('tr')
        # throw away the row with column names
        row_elements.pop(0)
        for row_element in row_elements:
            # 'td' is html tag that defines a column with the Table Data
            cells = row_element.find_all('td')
            row = [cell.get_text().rstrip('\n\r').strip() for cell in cells]
            rows.append(row)
        return rows


class Table:
    """
    The Class that provides a convenient interface to an extracted table.

    It should not be instantiated explicitly by the user,
    but implicitly through WikiTableExtractor constructor.
    The class' instance after proper initialization procedure contains
    all table's titles and rows.

    How to use it:
    1. Create an instance, using the constructor
    2. Set titles (optional), using instance.titles = [title list]
    3. Set rows (all at once), using instance.rows = [[row0], [row1], ..., [rowN]]
    4. Call instance._check_table() to test the attributes
    5. Use the method instance.as_dict_list() to convert the table to pandas DataFrame
    """
    def __init__(self):
        self._titles = []
        self._rows = []

    @property
    def titles(self):
        return self._titles

    @titles.setter
    def titles(self, titles):
        if not self._titles:
            self._titles.extend(titles)
        else:
            raise TitlesNotEmptyError()

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        if not self._rows:
            self._rows.extend(rows)
        else:
            raise RowsNotEmptyError()

    def as_dict_list(self):
        result = []
        for row in self._rows:
            result.append(dict(zip(self.titles, row)))

        return result

    def _check_table(self):
        assert self._rows

        common_len = len(self._rows[0])
        for row in self._rows:
            assert len(row) == common_len

        if not self._titles:
            self.titles = list(range(common_len))


class TitlesNotEmptyError(Exception): pass


class RowsNotEmptyError(Exception): pass
