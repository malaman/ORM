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

if __name__ == '__main__':
    unittest.main()
