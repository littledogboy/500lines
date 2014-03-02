MISSING = object()

class Base(object):
    """ The base class that all of the object model classes inherit from. """

    def __init__(self, cls):
        """ Every object has a class. """
        self.cls = cls

    def read_field(self, fieldname):
        """ read field 'fieldname' out of the object """
        return self._read_dict(fieldname)

    def write_field(self, fieldname, value):
        """ write field 'fieldname' into the object """
        self._write_dict(fieldname, value)

    def isinstance(self, cls):
        """ return True if the object is an instance of class cls """
        return self.cls.issubclass(cls)

    def send(self, methname, *args):
        """ send message 'methname' with arguments `args` to object """
        meth = self.cls._read_from_class(methname)
        return meth(self, *args)

    def _read_dict(self, fieldname):
        return MISSING

    def _write_dict(self, fieldname, value):
        raise AttributeError


class Instance(Base):
    """Instance of a user-defined class. """

    def __init__(self, cls):
        assert cls is None or isinstance(cls, Class)
        self.cls = cls
        self._dct = {}

    def _read_dict(self, fieldname):
        return self._dct.get(fieldname, MISSING)

    def _write_dict(self, fieldname, value):
        self._dct[fieldname] = value


class Class(Base):
    """ A User-defined class. """

    def __init__(self, name, base_class, dct, metaclass):
        Base.__init__(self, metaclass)
        self._dct = dct
        self.name = name
        self.base_class = base_class

    def _read_dict(self, fieldname):
        return self._dct.get(fieldname, MISSING)

    def _write_dict(self, fieldname, value):
        self._dct[fieldname] = value

    def mro(self):
        """ compute the mro (method resolution order) of the class """
        if self.base_class is None:
            return [self]
        else:
            return [self] + self.base_class.mro()

    def issubclass(self, cls):
        """ is self a subclass of cls? """
        return cls in self.mro()

    def _read_from_class(self, methname):
        for cls in self.mro():
            if methname in cls._dct:
                return cls._dct[methname]
        return MISSING

# set up the base hierarchy like in Python (the ObjVLisp model)
# the ultimate base class is OBJECT
OBJECT = Class("object", None, {}, None)
# TYPE is a subclass of OBJECT
TYPE = Class("type", OBJECT, {}, None)
# TYPE is an instance of itself
TYPE.cls = TYPE
# OBJECT is an instance of TYPE
OBJECT.cls = TYPE
