from psycopg2 import connect, ProgrammingError
from psycopg2.extras import DictCursor


class DatabaseError(Exception):
    pass
class NotFoundError(Exception):
    pass
class AttributeError(Exception):
    pass
class ModifiedButNotSaved(Exception):
    pass
class RuntimeException(Exception):
    pass

class Entity(object):
    db = None

    __delete_query          = 'DELETE FROM "{table}" WHERE {table}_id=%s'
    __insert_query          = 'INSERT INTO "{table}" ({columns}) VALUES ({placeholders}) RETURNING {table}_id'
    __list_query            = 'SELECT * FROM "{table}"'
    __parent_query          = 'SELECT * FROM "{table}" WHERE {parent}_id=%s'
    __select_query          = 'SELECT * FROM "{table}" WHERE {table}_id=%s'
    __select_child_query    = 'SELECT * FROM "{child_table}" WHERE {parent_table}_id=%s'
    __select_all_query      = 'SELECT * FROM "{table}"'
    __sibling_query         = 'SELECT * FROM "{sibling}" NATURAL JOIN "{join_table}" WHERE {table}_id=%s'
    __update_children       = 'UPDATE "{table}" SET {parent}_id=%s WHERE {table}_id IN ({children})'
    __update_query          = 'UPDATE "{table}" SET {columns} WHERE {table}_id=%s'


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
            raise AttributeError
        self.__load()
        if name in self._columns:
            return self._get_column(name)
        if name in self._parents:
            return self._get_parent(name)
        if name in self._children:
            return self._get_children(name)
        raise AttributeError

    def __setattr__(self, name, value):
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    setter with name and value as arguments or use default implementation
        if name in self._columns:
            self._set_column(name, value)
            self.__modified = True
            return
        if name in self._parents:
            self._set_parent(name, value)
            self.__modified = True
            return
        super(Entity, self).__setattr__(name, value)


    def __del__(self):
        self.__cursor.close()

    def __execute_query(self, query, args=None):
        # execute an sql statement and handle exceptions together with transactions
        #to do it is possible to return one row for __execute_query
        try:
            if args is None:
                self.__cursor.execute(query)
            else:
                self.__cursor.execute(query, args)
            try:
                return self.__cursor.fetchall()
            except ProgrammingError:
                return None
        except:
            self.__class__.db.rollback()
            raise DatabaseError

    def __insert(self):
        # generate an insert query string from fields keys and values and execute it
        # use prepared statements
        # save an insert id

        columns = ", ".join('{}'.format(key) for key in self.__fields.keys())
        values = list(self.__fields.values())
        placeholders = ', '.join('%s' for x in values)
        row = self.__execute_query(self.__insert_query.format(table=self.__table, columns=columns,
                                                        placeholders=placeholders), tuple(values))
        self.__id = row[0][0]
        self.db.commit()

    def __load(self):
        # if current instance is not loaded yet — execute select statement and store it's result as an associative array (fields), where column names used as keys
        if not self.__loaded:
            row = self.__execute_query(self.__select_query.format(table=self.__table), (self.__id,))
            self._load_fields(dict(row[0]))

    def _load_fields(self, dictionary):
        """
        load data from dictionary to instance __fields dictionary
        """
        if not self.__id:
            self.__id = dictionary['{}_id'.format(self.__table)]
        del dictionary['{}_id'.format(self.__table)]
        del dictionary['{}_updated'.format(self.__table)]
        del dictionary['{}_created'.format(self.__table)]
        self.__fields = dictionary
        self.__loaded = True

    def __update(self):
        # generate an update query string from fields keys and values and execute it
        # use prepared statements
        columns = ", ".join('{}=%s'.format(key) for key in self.__fields.keys())
        values = list(self.__fields.values())
        values.append(self.__id)
        self.__execute_query(self.__update_query.format(table=self.__table,
                                                        columns=columns), tuple(values))
        self.db.commit()

    def _get_children(self, name):
        # return an array of child entity instances
        # each child instance must have an id and be filled with data
        children_class_name = self._children[name]
        module = __import__('models')
        rows = self.__execute_query(self.__select_child_query.format(child_table=children_class_name.lower(), parent_table=self.__table), (self.__id,))
        instance_list = []
        for row in rows:
            instance = getattr(module, children_class_name)()
            instance._load_fields(dict(row))
            instance_list.append(instance)
        return instance_list

    def _get_column(self, name):
        # return value from fields array by <table>_<name> as a key
        return self.__fields['{}_{}'.format(self.__table, name)]



    def _get_parent(self, name):
        # get parent id from fields with <name>_id as a key
        # return an instance of parent entity class with an appropriate id
        parent_id = self.__fields['{}_id'.format(name)]
        row = self.__execute_query(self.__select_query.format(table=name), (parent_id,))
        module = __import__('models')
        instance = getattr(module, name.capitalize())()
        instance.__id = parent_id
        instance._load_fields(dict(row[0]))
        return instance


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
        if type(value) is int:
            self.__fields['{}_id'.format(name)] = value
        else:
            self.__fields['{}_id'.format(name)] = value.__id

    @classmethod
    def all(cls):
        # get ALL rows with ALL columns from corrensponding table
        # for each row create an instance of appropriate class
        # each instance must be filled with column data, a correct id and MUST NOT query a database for own fields any more
        # return an array of istances
        cls_instance = cls()
        rows = cls_instance.__execute_query(cls_instance.__select_all_query.format(table=cls.__name__.lower()))
        instance_list = []
        for row in rows:
            instance = cls()
            instance._load_fields(dict(row))
            instance_list.append(instance)
        return instance_list

    def delete(self):
        # execute delete query with appropriate id
        if self.__id:
            self.__execute_query(self.__delete_query.format(table=self.__table), (self.__id,))
        else:
            raise RuntimeException

    @property
    def id(self):
        # try to guess yourself
        return self.__id

    @property
    def created(self):
        # try to guess yourself
        return self.__fields['{}_created'.format(self.__table)]

    @property
    def updated(self):
        # try to guess yourself
        return self.__fields['{}_created'.format(self.__table)]

    def save(self):
        # execute either insert or update query, depending on instance id
        if self.__id:
            if self.__modified:
                self.__update()
        else:
            self.__insert()
        self.__modified = False