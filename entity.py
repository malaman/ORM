from psycopg2 import connect
from psycopg2.extras import DictCursor


class DatabaseError(Exception):
    pass
class NotFoundError(Exception):
    pass
class AttributeError(Exception):
    pass
class ModifiedButNotSaved(Exception):
    pass

class Entity(object):
    db = None

    __delete_query    = 'DELETE FROM "{table}" WHERE {table}_id=%s'
    __insert_query    = 'INSERT INTO "{table}" ({columns}) VALUES ({placeholders})'
    __list_query      = 'SELECT * FROM "{table}"'
    __parent_query    = 'SELECT * FROM "{table}" WHERE {parent}_id=%s'
    __select_query    = 'SELECT * FROM "{table}" WHERE {table}_id=%s'
    __sibling_query   = 'SELECT * FROM "{sibling}" NATURAL JOIN "{join_table}" WHERE {table}_id=%s'
    __update_children = 'UPDATE "{table}" SET {parent}_id=%s WHERE {table}_id IN ({children})'
    __update_query    = 'UPDATE "{table}" SET {columns} WHERE {table}_id=%s'

    def __init__(self, id=None):
        if self.__class__.db is None:
            raise DatabaseError()

        self.__cursor   = self.__class__.db.cursor(cursor_factory=DictCursor)
        self.__fields   = {}
        self.__id       = id
        self.__loaded   = False
        self.__modified = False
        self.__table    = self.__class__.__name__.lower()

    def __getattr__(self, name):
        # check, if instance is modified and throw an exception
        # get corresponding data from database if needed
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    getter with name as an argument
        # throw an exception, if attribute is unrecognized
        if self.__modified:
            raise ModifiedButNotSaved
        else:
            if name in self._columns:
                if not self.__loaded:
                    self.__load()
                return self._get_column(name)
            else:
                raise AttributeError
        return super(Entity, self).__getattr__(name)


    def __setattr__(self, name, value):
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    setter with name and value as arguments or use default implementation
        if name in self._columns:
            exist_value = None
            try:
                exist_value=self.__getattr__(name)
            except KeyError:
                pass
            if exist_value != value:
                self._set_column(name, value)
                self.__modified = True
                return
        else:
            super(Entity, self).__setattr__(name, value)


    def __execute_query(self, query, args=None):
        # execute an sql statement and handle exceptions together with transactions
        try:
            if args is None:
                self.__cursor.execute(query)
            else:
                self.__cursor.execute(query % args)
            self.__class__.db.commit()
        except:
            self.__class__.db.rollback()
            raise DatabaseError

    def __insert(self):
        # generate an insert query string from fields keys and values and execute it
        # use prepared statements
        # save an insert id
        if self.__id:
            self.__fields['{}_id'.format(self.__table)] = self.__id
        columns = ", ".join('{}'.format(key) for key in self.__fields.keys())
        placeholders = ", ".join("'{}'".format(value) for value in self.__fields.values())
        if not columns  or not placeholders:
            raise AttributeError
        self.__execute_query(self.__insert_query.format(table=self.__table, columns=columns,
                                                        placeholders=placeholders))
        self.__modified = False

    def __load(self):
        # if current instance is not loaded yet — execute select statement and store it's result as an associative array (fields), where column names used as keys
        if self.__id:
            self.__execute_query(self.__select_query.format(table=self.__table), self.__id)
            result = self.__cursor.fetchone()
            if result:
                keys = ['{}_{}'.format(self.__table, elem) for elem in self._columns]
                values = []
                for key in keys:
                    values.append(result[key])
                self.__fields = dict(zip(keys, values))
                self.__loaded = True

    def __update(self):
        # generate an update query string from fields keys and values and execute it
        # use prepared statements
        columns = ", ".join(["{}='{}'".format(k, v) for (k, v) in self.__fields.items()])
        self.__execute_query(self.__update_query.format(table=self.__table, columns=columns), self.__id)
        self.__modified = False

    def _get_children(self, name):
        # return an array of child entity instances
        # each child instance must have an id and be filled with data
        pass

    def _get_column(self, name):
        # return value from fields array by <table>_<name> as a key
        return self.__fields['{}_{}'.format(self.__table, name)]

    def _get_parent(self, name):
        # get parent id from fields with <name>_id as a key
        # return an instance of parent entity class with an appropriate id
        pass

    def _get_siblings(self, name):
        # get parent id from fields with <name>_id as a key
        # return an array of sibling entity instances
        # each sibling instance must have an id and be filled with data
        pass

    def _set_column(self, name, value):
        # put new value into fields array with <table>_<name> as a key
        self.__fields['{}_{}'.format(self.__table, name)] = value

    def _set_parent(self, name, value):
        # put new value into fields array with <name>_id as a key
        # value can be a number or an instance of Entity subclass
        pass

    @classmethod
    def all(cls):
        # get ALL rows with ALL columns from corrensponding table
        # for each row create an instance of appropriate class
        # each instance must be filled with column data, a correct id and MUST NOT query a database for own fields any more
        # return an array of istances
        pass

    def delete(self):
        # execute delete query with appropriate id
        if self.__id:
            self.__execute_query(self.__delete_query.format(self.__table), self.__id)

    @property
    def id(self):
        # try to guess yourself
        return self.__id

    @property
    def created(self):
        # try to guess yourself
        pass

    @property
    def updated(self):
        # try to guess yourself
        return self.__modified

    def save(self):
        # execute either insert or update query, depending on instance id
        if self.__loaded:
            self.__update()
        else:
            self.__insert()


