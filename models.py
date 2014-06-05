from entity import *

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

class Article(Entity):
    _columns = ['title', 'text', 'description', 'tag']


if __name__ == "__main__":
    from psycopg2 import connect
    Entity.db = connect(host='localhost', dbname='news2', user='dbuser', password='dbuser', port='5432')
    section = Section()
    section.title = 'something'
    section.save()
    section2 = Section(436)
    print(section2.title)
    section2.title = 'new title'
    section2.save()
    section3 = Section(437)
    section3.title = 'sdfvsdfv'
    section3.save()
    # section.title = 'new test title'
    # section.delete()
    # section.title = "title"
    # print(section.title)
    # section.save()
    # section.title = "title1234"
    # print(section.title)
    # section3 = Section(3)
    # section3.title = 'new title for section3'
    # section3.save()
    # print(section3.title)
    # section4 = Section()
    # section4.title = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    # section4.save()
    # section5 = Section()
    # section5.title = 'test title for section5'
    # section5.save()
    # section6 = Section()
    # section6.title = "this is really important title"
    # section6.save()
    # section = Section()
    # section.title = 'sdfvsdfv'
    # section.title = 'sdfvsdfvdsfvdsfv'
    # section.save()
    # print(section6.id)
    # lst = Section.all()
    # for obj in lst:
    #     obj.title = 'same title for all objects'
    #     obj.save()
    #
    # section = Section()
    # section.title = "zalupa"
    # section.save()

    # for section in Section.all():
    #      section.delete()

    Entity.db.close()

