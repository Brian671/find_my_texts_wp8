__author__ = 'owner'

import sqlite3
from types import *
current_db = None
current_tb = None
generic_tb_index = 0
#generic_db_index = 0
"""
def open_db(path):
    try:
        db = sqlite3.connect(path);
        cursor = db.cursor();
        cursor.execute(
            ""
                CREATE TABLE IF NOT EXISTS

            ""
        )
"""


# cross join / cartesian product (*)
# inner join INNER JOIN
"""
INNER JOIN
-------------
**IMPLICIT**
SELECT *
FROM employee
INNER JOIN department ON employee.DepartmentID = department.DepartmentID;

-------------
**EXPLICIT**
SELECT *
FROM employee, department
WHERE employee.DepartmentID = department.DepartmentID;
"""



"""
EQUI-JOIN
retain if
-------------
**IMPLICIT**
SELECT *
FROM employee, department
WHERE employee.DepartmentID = department.DepartmentID;

-------------
**EXPLICIT**
SELECT *
FROM employee
INNER JOIN department
USING (DepartmentID);
"""


""" NATURAL JOIN
retain if entire record is equal
-------------
**IMPLICIT**
[use nested equi-joins]

-------------
**EXPLICIT**
SELECT *
FROM employee
NATURAL JOIN department;

"""

"""
LEFT OUTER JOIN
-------------
**IMPLICIT**
SELECT *
FROM employee, department
WHERE employee.DepartmentID = department.DepartmentID(+);
-or-
SELECT *
FROM employee, department
WHERE employee.DepartmentID *= department.DepartmentID;
-or-
SELECT *
FROM employee, OUTER department
WHERE employee.DepartmentID = department.DepartmentID

-------------
**EXPLICIT**
SELECT *
FROM employee
LEFT OUTER JOIN department ON employee.DepartmentID = department.DepartmentID;
"""
class View(object):














    __slots__ = 0
    __dict__ = {}
    __metaclass__ = None

    def COUNT(self, column_name='*', distinct=False):
        pass
    # & SELECT * as row FROM [self] as self, [other] as other WHERE other
    def __and__(self, other):
        pass
    # ^
    def __xor__(self, other):
        pass

    # len() COUNT(*)
    def __len__(self):
        return COUNT(self)


    def SELECT(self):
        pass
    def __getslice__(self, i, j):
        pass


    def __new__(cls):
        pass
    def __init__(self):
        pass
    def __del__(self):
        pass
    def __repr__(self):
        pass
    def __str__(self):
        pass
    def __lt__(self, other):
        pass
    def __le__(self, other):
        pass
    def __eq__(self, other):
        pass
    def __ne__(self, other):
        pass
    def __gt__(self, other):
        pass
    def __ge__(self, other):
        pass
    def __cmp__(self, other):
        pass
    def __nonzero__(self):
        pass
    def __unicode__(self):
        pass
    def __getitem__(self, key):
        pass
    def __missing__(self, key):
        pass
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __iter__(self):
        pass
    def __contains__(self, item):
        pass
    def __setslice__(self, i, j, sequence):
        pass
    def __delslice__(self, i, j):
        pass
    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __floordiv__(self, other):
        pass
    def __mod__(self, other):
        pass
    def __divmod__(self, other):
        pass
    def __pow__(self, other, modulo=None): #ternary?
        pass
    def __lshift__(self, other):
        pass
    def __rshift__(self, other):
        pass

    def __or__(self, other):
        pass
    def __div__(self, other):
        pass
    def __truediv__(self, other):
        pass
    def __iadd__(self, other):
        pass
    def __isub__(self, other):
        pass
    def __imul__(self, other):
        pass
    def __ifloordiv__(self, other):
        pass
    def __imod__(self, other):
        pass
    def __idivmod__(self, other):
        pass
    def __ipow__(self, other, modulo=None): #ternary?
        pass
    def __ilshift__(self, other):
        pass
    def __irshift__(self, other):
        pass
    def __iand__(self, other):
        pass
    def __ixor__(self, other):
        pass
    def __ior__(self, other):
        pass
    def __idiv__(self, other):
        pass
    def __itruediv__(self, other):
        pass
    def __neg__(self):
        pass
    def __pos__(self):
        pass
    def __abs__(self):
        pass
    #
    def __invert__(self):
        pass

    # int() ?
    def __int__(self):
        pass

class Table(View):
    pass

"""


def open_table(db=None, tb=None):
    try:
        if tb is None:
            tb
    except Exception e:
        pass

# http://pythoncentral.io/introduction-to-sqlite-in-python/
def open_db(db=None):
    global current_db
    try:
        if db is None:
            if current_db is None:
                db = sqlite3.connect(":memory:")
            else:
                db = current_db
        elif db is StringType:
            cursor = db.cursor()
            db = sqlite3.connect(db)
    except Exception as e:
        db.rollback()
    current_db = db
    return db




"""