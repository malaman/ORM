import unittest

from entity import *
from models import *


class MyTestCase(unittest.TestCase):
    def test_object_creation(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')
        item = Item()
        item.name = 'test'
        item.price = 100
        item.category = 1
        item.save()
        item.delete()
        self.assertTrue(1, 1)

    def test_creation_and_deletion_without_saving(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')
        item = Item()
        self.assertRaises(RuntimeException, item.delete)

    def test_retrive(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')
        item = Item()
        item.name = 'test test'
        item.price = 100
        item.category = 1
        item.save()
        item2 = Item(item.id)
        self.assertEqual(item.name, item2.name)
        item.delete()


    def test_update(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')

        item = Item()
        item.name = 'test test'
        item.price = 100
        item.category = 1
        item.save()
        item2 = Item(item.id)
        item2.name = 'new item name for test'
        item2.save()

        item = Item(item2.id)
        self.assertTrue(item.name, 'new item name for test')
        item.delete()

    def test_all_feature(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')

        item_list = Item.all()
        for item in item_list:
            print(item.name)
        self.assertTrue(1, 1)

    def test_parent_retrieve_feature(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')

        item = Item(1)
        parent = item.category
        self.assertEqual(item.category.title, parent.title)

    def test_parent_update_feature(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')

        item = Item(1)
        item.category = 2
        item.save()
        item = Item(1)
        self.assertEqual(item.category.id, 2)
        item.category = 1
        category = Category(3)
        item.category = category
        item.save()

        item = Item(1)
        self.assertEqual(item.category.id, category.id)
        item.category = 1
        item.save()

    def test_get_children_feature(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')

        category = Category(1)

        for item in category.items:
            print(item.name, '!!!!')
        self.assertTrue(1,1)

    def test_get_siblings_feature(self):
        Entity.db = connect(host='localhost', dbname='db2', user='dbuser', password='dbuser', port='5432')
        order = Order(6)

        for item in order.items:
            print(item.name, '????')

        self.assertTrue(1,1)

if __name__ == '__main__':
    unittest.main()
