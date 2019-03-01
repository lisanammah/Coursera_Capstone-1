import unittest

import requests
from bs4 import BeautifulSoup

from Week3Assignment.wiki_table_extractor import WikiTableExtractor


class TestWikiTableExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        The method make url request to download wiki page with table
        (any page with single table) and creates BeautifulSoup instance
        using the page content.
        Since url request is pretty slow, let's do it only once
        per tests set.
        """
        super().setUpClass()

        page_link = ('https://en.wikipedia.org/wiki/'
                     'List_of_countries_by_beer_consumption_per_capita')
        page_response = requests.get(page_link, timeout=5)

        cls.page_content = BeautifulSoup(page_response.content, 'html.parser')

        # test data:
        cls.actual_titles = ['Global rank[1]', 'Country', 'Consumption per capita [1](litres)',
                             '2015–2016change(litres)', 'Total national consumption(106 L)[A]',
                             'Year']
        cls.actual_row_0 = ['1', 'Czech Republic', '143.3', '0.9', '1959', '2016']
        cls.actual_row_4 = ['5', 'Poland', '100.8', '1.8', '3892', '2016']
        cls.actual_row_last = ['', 'Indonesia[4]', '0.7', '', '', '2015']

    def setUp(self):
        self.extractor = WikiTableExtractor()
        self.extractor.parse_table_from_page(self.page_content)
        self.table = self.extractor.table

    def test_titles(self):
        self.assertEqual(self.table.titles, self.actual_titles)

    def test_rows(self):
        self.assertEqual(self.table.rows[0], self.actual_row_0)
        self.assertEqual(self.table.rows[4], self.actual_row_4)
        self.assertEqual(self.table.rows[-1], self.actual_row_last)

    def test_dict_list(self):
        actual_row_dict_0 = dict(zip(self.actual_titles, self.actual_row_0))
        actual_row_dict_4 = dict(zip(self.actual_titles, self.actual_row_4))
        actual_row_dict_last = dict(zip(self.actual_titles, self.actual_row_last))

        parsed_dict = self.table.as_dict_list()

        self.assertEqual(parsed_dict[0], actual_row_dict_0)
        self.assertEqual(parsed_dict[4], actual_row_dict_4)
        self.assertEqual(parsed_dict[-1], actual_row_dict_last)
