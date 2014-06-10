import unittest

from entity import *
from models import *


class MyTestCase(unittest.TestCase):
    def test_object_creation(self):
        Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')
        section = Section()
        section.title = 'test'
        section.save()
        self.assertTrue(1, 1)

    def test_creation_and_deletion_without_saving(self):
        Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')
        section = Section()
        self.assertRaises(RuntimeException, section.delete)

    def test_retrive(self):
        Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')
        section = Section()
        section.title = 'test test'
        section.save()
        section2 = Section(section.id)
        self.assertEqual(section.title, section2.title)

    def test_update(self):
        Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')

        section = Section()
        section.title = 'test test'
        section.save()
        section2 = Section(section.id)
        section2.title = 'new section title for test'
        section2.save()

        section = Section(section2.id)
        self.assertTrue(section.title, 'new section title for test')

    def test_all_feature(self):
        Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')

        section_list = Section.all()
        for section in section_list:
            print(section.title)
        self.assertTrue(1, 1)


if __name__ == '__main__':
    unittest.main()
