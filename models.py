from entity import *
#todo when made update it is nessesry to build update statement with .__fields disctionary
#todo __getattr_ отрабатывает только тогда, когда в __dict__ нету правильного аттрибута.
#todo getattribut отрабатывает всегда

class Section(Entity):
    _columns  = ['title']
    _parents  = []
    _children = {'categories': 'Category'}
    _siblings = {}

# class Category(Entity):
#     _columns  = ['title']
#     _parents  = ['section']
#     _children = {'posts': 'Post'}
#     _siblings = {}

class Post(Entity):
    _columns  = ['content', 'title']
    _parents  = ['category']
    _children = {'comments': 'Comment'}
    _siblings = {'tags': 'Tag'}

class Comment(Entity):
    _columns  = ['text']
    _parents  = ['post', 'user']
    _children = {}
    _siblings = {}

class Tag(Entity):
    _columns  = ['name']
    _parents  = []
    _children = {}
    _siblings = {'posts': 'Post'}

class User(Entity):
    _columns  = ['name', 'email', 'age']
    _parents  = []
    _children = {'comments': 'Comment'}
    _siblings = {}

class Category(Entity):
    _columns = ['title', 'enabled']
    _parents = []
    _children = {'items': 'Item'}

class Item(Entity):
    _columns = ['name', 'description', 'price', 'popular']
    _parents = ['category']
    _children = {}

if __name__ == "__main__":
    from psycopg2 import connect
    Entity.db = connect(host='localhost', dbname='news3', user='dbuser', password='dbuser', port='5432')
    category = Category(1)
    print(category.title)
    item = Item(1)
    print(item.name)
    print(item.category.title)
    category = Category(2)

    category = Category()
    category.title = 'new category'
    category.save()

    category = Category(1)

    for item in category.items:
        print(item.name)


    # for category in Category.all():
    #     print(category.title)
    #
    # instance = item._get_parent('category')
    # print(instance.title)



    Entity.db.close()

