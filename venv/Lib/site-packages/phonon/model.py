import phonon.fields
import phonon.exceptions
import phonon.connections
import phonon.reference
import phonon.registry


class MetaModel(type):
    """
    The MetaModel is a meta-class for the Model; which allows fields to be set on the model as kwargs to it's
    initializer, loosely validated against the user-defined fields.

    Validation here is extremely minimal. The Fields here are only used to provide a merge/cache interface, and to
    parse kwargs passed to the Model initializer (to be set as model members).
    """
    def __new__(cls, name, parents, dct):
        cls._fields = {}
        for key, val in list(dct.items()):
            if isinstance(val, phonon.fields.Field):
                cls._fields[key] = val

        return super(MetaModel, cls).__new__(cls, name, parents, dct)


class Model(metaclass=MetaModel):
    """
    The Model class should be the base for any user-defined models. It provides an interface to configure your
    datatypes in such a way that aggregation is simple and transparent, with global awareness. For example; if you
    define a Session model as

    ```python
    class Session(phonon.models.Model):
        id = phonon.fields.ID()
        last_10_pages_viewed = phonon.fields.WindowedList()
    ```

    You can instantiate the session on two entirely different hosts such as on host A:

    ```python
    session_one = Session(id=1, last_10_pages_viewed=[(timestamp, viewed_page)])
    ```

    And on host B:
    ```python
    session_one = Session(id=1, last_10_pages_viewed=[(timestamp, viewed_page)])
    ```
    Now each machine is aware that the global reference count for this session is _2_. This allows decisions to be made
    such as at what time to write that session data to the database; and how to sort the last ten pages viewed when in
    fact the user has viewed 20.
    """

    TTL = 30  # Seconds

    def __init__(self, *args, **kwargs):
        try:
            self.id = kwargs['id']
            if not isinstance(self.id, bytes):
                raise TypeError(f'Model expected its `id` to be of type bytes, got {type(self.id)}')
            self.__resource_key = f"{self.__class__.__name__}.{self.id}".encode('utf8')
            self.__client = phonon.connections.connection.client.using_key(self.__resource_key)
            self.reference = phonon.reference.Reference(self.__resource_key)
        except KeyError as e:
            raise phonon.exceptions.ArgumentError("id is a required field")

        for key, field in list(self.__class__._fields.items()):
            setattr(self, key, kwargs[key])

    def name(self):
        return self.__class__.__name__.encode('utf8')

    def registry_key(self):
        return self.name() + b'.' + self.id

    def merge(self, other):
        for key, field in list(self.__class__._fields.items()):
            setattr(self, key, field.merge(getattr(self, key),
                                           getattr(other, key)))

    def cache(self):
        for field_name, field in list(self.__class__._fields.items()):
            field_value = getattr(self, field_name)
            if not field.cache(self.__client, self, field_name.encode('utf8'), field_value):
                raise phonon.exceptions.CacheError("Failed to cache {}".format(field_name))

    def on_complete(self):
        raise phonon.exceptions.NotImplemented("on_complete should be implemented.")
