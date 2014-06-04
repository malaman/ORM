from entity import *
#todo: do not raise exception when object with number created

class Section(Entity):
    _columns  = ['title']
    _parents  = []
    _children = {'categories': 'Category'}
    _siblings = {}

class Category(Entity):
    _columns  = ['title']
    _parents  = ['section']
    _children = {'posts': 'Post'}
    _siblings = {}

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


if __name__ == "__main__":
    from psycopg2 import connect
    Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')
    section = Section(1)
    print(section.title)
    section.title = "title"
    section.save()
    print(section.title)
    section3 = Section(3)
    section3.title = 'new title for section3'
    section3.save()
    print(section3.title)
    section4 = Section()
    section4.title = "sdfvsdfvsdfvsdf"
    section4.save()
    section4.delete()
    # section.title = "zalupa"
    # section.save()
    #
    # for section in Section.all():
    #     print(section.title)

