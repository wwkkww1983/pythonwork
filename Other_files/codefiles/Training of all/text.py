#-*- coding:utf-8 -*-
'''s1=72
s2=85
r=(s2-s1)/s1*100
print('小明成绩上升%.1f%%' %r)'''

print(u'''静夜诗
床前明月光，
疑是地上霜，
举头望明月，
低头思故乡。''')

Python 3.5.0 (v3.5.0:374f501f4567, Sep 13 2015, 02:16:59) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> classmates = ['Micheal','Bob','Tracy']
>>> classmates
['Micheal', 'Bob', 'Tracy']
>>> len(classmates)
3
>>> classmates[0]
'Micheal'
>>> cm=classmates
>>> cm
['Micheal', 'Bob', 'Tracy']
>>> cm[0]
'Micheal'
>>> cm[2]
'Tracy'
>>> cm[3]
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    cm[3]
IndexError: list index out of range
>>> cm[len(cm)-1]
'Tracy'
>>> cm[2]
'Tracy'
>>> cm[-1]
'Tracy'
>>> help(list)
Help on class list in module builtins:

class list(object)
 |  list() -> new empty list
 |  list(iterable) -> new list initialized from iterable's items
 |  
 |  Methods defined here:
 |  
 |  __add__(self, value, /)
 |      Return self+value.
 |  
 |  __contains__(self, key, /)
 |      Return key in self.
 |  
 |  __delitem__(self, key, /)
 |      Delete self[key].
 |  
 |  __eq__(self, value, /)
 |      Return self==value.
 |  
 |  __ge__(self, value, /)
 |      Return self>=value.
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __getitem__(...)
 |      x.__getitem__(y) <==> x[y]
 |  
 |  __gt__(self, value, /)
 |      Return self>value.
 |  
 |  __iadd__(self, value, /)
 |      Implement self+=value.
 |  
 |  __imul__(self, value, /)
 |      Implement self*=value.
 |  
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __iter__(self, /)
 |      Implement iter(self).
 |  
 |  __le__(self, value, /)
 |      Return self<=value.
 |  
 |  __len__(self, /)
 |      Return len(self).
 |  
 |  __lt__(self, value, /)
 |      Return self<value.
 |  
 |  __mul__(self, value, /)
 |      Return self*value.n
 |  
 |  __ne__(self, value, /)
 |      Return self!=value.
 |  
 |  __new__(*args, **kwargs) from builtins.type
 |      Create and return a new object.  See help(type) for accurate signature.
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  
 |  __reversed__(...)
 |      L.__reversed__() -- return a reverse iterator over the list
 |  
 |  __rmul__(self, value, /)
 |      Return self*value.
 |  
 |  __setitem__(self, key, value, /)
 |      Set self[key] to value.
 |  
 |  __sizeof__(...)
 |      L.__sizeof__() -- size of L in memory, in bytes
 |  
 |  append(...)
 |      L.append(object) -> None -- append object to end
 |  
 |  clear(...)
 |      L.clear() -> None -- remove all items from L
 |  
 |  copy(...)
 |      L.copy() -> list -- a shallow copy of L
 |  
 |  count(...)
 |      L.count(value) -> integer -- return number of occurrences of value
 |  
 |  extend(...)
 |      L.extend(iterable) -> None -- extend list by appending elements from the iterable
 |  
 |  index(...)
 |      L.index(value, [start, [stop]]) -> integer -- return first index of value.
 |      Raises ValueError if the value is not present.
 |  
 |  insert(...)
 |      L.insert(index, object) -- insert object before index
 |  
 |  pop(...)
 |      L.pop([index]) -> item -- remove and return item at index (default last).
 |      Raises IndexError if list is empty or index is out of range.
 |  
 |  remove(...)
 |      L.remove(value) -> None -- remove first occurrence of value.
 |      Raises ValueError if the value is not present.
 |  
 |  reverse(...)
 |      L.reverse() -- reverse *IN PLACE*
 |  
 |  sort(...)
 |      L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  __hash__ = None

>>> help(list.append)
Help on method_descriptor:

append(...)
    L.append(object) -> None -- append object to end

>>> cm
['Micheal', 'Bob', 'Tracy']
>>> cm.append('Adam')
>>> cm
['Micheal', 'Bob', 'Tracy', 'Adam']
>>> cm.insert(1,'Jack')
>>> cm
['Micheal', 'Jack', 'Bob', 'Tracy', 'Adam']
>>> help(list.insert)
Help on method_descriptor:

insert(...)
    L.insert(index, object) -- insert object before index

>>> help(list.pop)
Help on method_descriptor:

pop(...)
    L.pop([index]) -> item -- remove and return item at index (default last).
    Raises IndexError if list is empty or index is out of range.

>>> cm.pop()
'Adam'
>>> cm
['Micheal', 'Jack', 'Bob', 'Tracy']
>>> cm.pop(2)
'Bob'
>>> cm
['Micheal', 'Jack', 'Tracy']
>>> cm[1] = 'Sarah'
>>> cm
['Micheal', 'Sarah', 'Tracy']
>>> type(cm)
<class 'list'>
>>> id(cm)
32690944
>>> help(type)
Help on class type in module builtins:

class type(object)
 |  type(object_or_name, bases, dict)
 |  type(object) -> the object's type
 |  type(name, bases, dict) -> a new type
 |  
 |  Methods defined here:
 |  
 |  __call__(self, /, *args, **kwargs)
 |      Call self as a function.
 |  
 |  __delattr__(self, name, /)
 |      Implement delattr(self, name).
 |  
 |  __dir__(...)
 |      __dir__() -> list
 |      specialized __dir__ implementation for types
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __instancecheck__(...)
 |      __instancecheck__() -> bool
 |      check if an object is an instance
 |  
 |  __new__(*args, **kwargs)
 |      Create and return a new object.  See help(type) for accurate signature.
 |  
 |  __prepare__(...)
 |      __prepare__() -> dict
 |      used to create the namespace for the class statement
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  
 |  __setattr__(self, name, value, /)
 |      Implement setattr(self, name, value).
 |  
 |  __sizeof__(...)
 |      __sizeof__() -> int
 |      return memory consumption of the type object
 |  
 |  __subclasscheck__(...)
 |      __subclasscheck__() -> bool
 |      check if a class is a subclass
 |  
 |  __subclasses__(...)
 |      __subclasses__() -> list of immediate subclasses
 |  
 |  mro(...)
 |      mro() -> list
 |      return a type's method resolution order
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __abstractmethods__
 |  
 |  __dict__
 |  
 |  __text_signature__
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  __base__ = <class 'object'>
 |      The most base type
 |  
 |  __bases__ = (<class 'object'>,)
 |  
 |  __basicsize__ = 432
 |  
 |  __dictoffset__ = 132
 |  
 |  __flags__ = -2146675712
 |  
 |  __itemsize__ = 20
 |  
 |  __mro__ = (<class 'type'>, <class 'object'>)
 |  
 |  __weakrefoffset__ = 184

>>> help(id)
Help on built-in function id in module builtins:

id(obj, /)
    Return the identity of an object.
    
    This is guaranteed to be unique among simultaneously existing objects.
    (CPython uses the object's memory address.)

>>> L = ['Apple',100,True,3.2565,cm]
>>> L
['Apple', 100, True, 3.2565, ['Micheal', 'Sarah', 'Tracy']]
>>> len(L)
5
>>> L[4][2]
'Tracy'
>>> l=[]
>>> l
[]
>>> len(l)
0
>>> L1=['Apple', 100, True, 3.2565, ['Micheal', 'Sarah', 'Tracy',[1,2,3,4]]]
>>> L1
['Apple', 100, True, 3.2565, ['Micheal', 'Sarah', 'Tracy', [1, 2, 3, 4]]]
>>> L[4][2][1]
'r'
>>> L1[4][2][1]
'r'
>>> L1[4][1][1]
'a'
>>> L1[4][3][1]
2
>>> cmt = ('Micheal', 'Sarah', 'Tracy')
>>> cmt1 =('Bob')
>>> type(cmt1)
<class 'str'>
>>> type(cmt)
<class 'tuple'>
>>> cmt1 = ('Bob',)
>>> type(cmt1)
<class 'tuple'>
>>> score = (98)
>>> type(score)
<class 'int'>
>>> score = (98,)
>>> type(score)
<class 'tuple'>
>>> cmt
('Micheal', 'Sarah', 'Tracy')
>>> t = ()
>>> type(t)
<class 'tuple'>
>>> t1 = (,)
SyntaxError: invalid syntax
>>> cmt
('Micheal', 'Sarah', 'Tracy')
>>> t = ('Apple', 100, True, 3.2565, ['Micheal', 'Sarah', 'Tracy'])
>>> t
('Apple', 100, True, 3.2565, ['Micheal', 'Sarah', 'Tracy'])
>>> t[4][1] = 'Bob'
>>> t
('Apple', 100, True, 3.2565, ['Micheal', 'Bob', 'Tracy'])
>>> t[0][0] = 'a'
Traceback (most recent call last):
  File "<pyshell#63>", line 1, in <module>
    t[0][0] = 'a'
TypeError: 'str' object does not support item assignment
>>> t[0] = 'Banana'
Traceback (most recent call last):
  File "<pyshell#64>", line 1, in <module>
    t[0] = 'Banana'
TypeError: 'tuple' object does not support item assignment
>>> cm
['Micheal', 'Sarah', 'Tracy']
>>> t= ('Apple', 100, True, 3.2565, cm)
>>> t
('Apple', 100, True, 3.2565, ['Micheal', 'Sarah', 'Tracy'])
>>> cm[1] = 'Bob'
>>> cm
['Micheal', 'Bob', 'Tracy']
>>> t
('Apple', 100, True, 3.2565, ['Micheal', 'Bob', 'Tracy'])
>>> help(tuple)
Help on class tuple in module builtins:

class tuple(object)
 |  tuple() -> empty tuple
 |  tuple(iterable) -> tuple initialized from iterable's items
 |  
 |  If the argument is a tuple, the return value is the same object.
 |  
 |  Methods defined here:
 |  
 |  __add__(self, value, /)
 |      Return self+value.
 |  
 |  __contains__(self, key, /)
 |      Return key in self.
 |  
 |  __eq__(self, value, /)
 |      Return self==value.
 |  
 |  __ge__(self, value, /)
 |      Return self>=value.
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __getitem__(self, key, /)
 |      Return self[key].
 |  
 |  __getnewargs__(...)
 |  
 |  __gt__(self, value, /)
 |      Return self>value.
 |  
 |  __hash__(self, /)
 |      Return hash(self).
 |  
 |  __iter__(self, /)
 |      Implement iter(self).
 |  
 |  __le__(self, value, /)
 |      Return self<=value.
 |  
 |  __len__(self, /)
 |      Return len(self).
 |  
 |  __lt__(self, value, /)
 |      Return self<value.
 |  
 |  __mul__(self, value, /)
 |      Return self*value.n
 |  
 |  __ne__(self, value, /)
 |      Return self!=value.
 |  
 |  __new__(*args, **kwargs) from builtins.type
 |      Create and return a new object.  See help(type) for accurate signature.
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  
 |  __rmul__(self, value, /)
 |      Return self*value.
 |  
 |  count(...)
 |      T.count(value) -> integer -- return number of occurrences of value
 |  
 |  index(...)
 |      T.index(value, [start, [stop]]) -> integer -- return first index of value.
 |      Raises ValueError if the value is not present.

>>> len(t)
5
>>> t
('Apple', 100, True, 3.2565, ['Micheal', 'Bob', 'Tracy'])
>>> t = ('Apple', 100, True, 3.2565, ['Micheal', 'Bob', 'Tracy'],100,False,False,False)
>>> t
('Apple', 100, True, 3.2565, ['Micheal', 'Bob', 'Tracy'], 100, False, False, False)
>>> t.count(100)
2
>>> t.count(Flase)
Traceback (most recent call last):
  File "<pyshell#77>", line 1, in <module>
    t.count(Flase)
NameError: name 'Flase' is not defined
>>> t.count(False)
3

>>> t.count('Bob')
0
>>> t.index(100)
1
>>> t.index(True)
2
>>> T.index(False)
Traceback (most recent call last):
  File "<pyshell#82>", line 1, in <module>
    T.index(False)
NameError: name 'T' is not defined
>>> t.index(False)
6
>>> 