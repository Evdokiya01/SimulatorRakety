class Field:
    """
    The Field is a base-class that allows type-checking of each Field subclass via isinstance(). This is
    necessary so the MetaModel can tell the difference between user-defined fields and other model members
    and attributes, such as static variables.

    """

    def key(self, *args):
        """
        Concatenates a list of arguments to provide a (hopefully) unique key to set in the cache.

        :param args: A list of ordered, serializable, values.
        :return: A period-delimited string concatenation of the input arguments in order.
        """
        for key_element in args:
            if not isinstance(key_element, bytes):
                raise TypeError(f'`key` expected bytes, got {type(key_element)}')
        return b".".join([a for a in args])


class ID(Field):
    """
    This field is intended to represent the unique ID on models defined by the user. It has the unique feature that
    neither merging or caching do anything to it. It merely allows an `id` attribute to be defined on our models,
    which is a required parameter.
    """

    def merge(self, a, b):
        assert a == b
        return a

    def cache(self, *args):
        return True


class Sum(Field):
    """
    This field allows either integer or floating point values to be aggregated as a sum. It defines a method to merge
    them locally, as well as in the cache in a way that is totally conflict-free.
    """

    def __init__(self, data_type=int):
        self.data_type = data_type

    def merge(self, a, b):
        return a + b

    def cache(self, client, model, field_name, field_value):
        key = self.key(model.name(), model.id, field_name)
        if self.data_type is int:
            return client.incrby(key, field_value) is not None
        return client.incrbyfloat(key, field_value) is not None


class Diff(Field):
    """
    This field allows either integer or floating point values to be aggregated as a difference. It defines a method to merge
    them locally, as well as in the cache in a way that is totally conflict-free.
    """

    def __init__(self, data_type=int):
        self.data_type = data_type

    def merge(self, a, b):
        return a - b

    def cache(self, client, model, field_name, field_value):
        key = self.key(model.name(), model.id, field_name)
        if self.data_type is int:
            return client.incrby(key, -field_value) is not None
        return client.incrbyfloat(key, -field_value) is not None


class ListAppend(Field):
    """
    This field allows _primitive_ data types to be aggregated as a list. It defines a method to merge
    them locally, as well as in the cache in a way that is totally conflict-free.
    """

    def cache(self, client, model, field_name, field_value):
        key = self.key(model.name(), model.id, field_name)
        return client.rpush(key, *field_value) > 0

    def merge(self, a, b):
        return a + b


class SetAppend(Field):
    """
    This field allows _primitive_ data types to be aggregated as a set. It defines a method to merge
    them locally, as well as in the cache in a way that is totally conflict-free.
    """

    def cache(self, client, model, field_name, field_value):
        key = self.key(model.name(), model.id, field_name)
        return client.sadd(key, *field_value) > 0

    def merge(self, a, b):
        return a.union(b)


class WindowedList(Field):
    """
    This field allows _primitive_ data types to be aggregated as an ordered list. It defines a method to merge
    them locally, as well as in the cache in a way that is totally conflict-free.

    This field is a bit unique in that it imposes a constraint on the value of the list the user provides;
    they must be of the form (timestamp, value). The windowed list is then ranked by time. Hypothetically;
    you could also aggregate a "top ten" list or something of the sort by providing a more general ranking
    instead of a timestamp.
    """

    def __init__(self, window_length=None):
        self.window_length = window_length or 10

    def cache(self, client, model, field_name, field_value):
        key = self.key(model.name(), model.id, field_name)
        pipeline = client.route(key).pipeline()
        pipeline.zadd(key, {value: ts for ts, value in field_value})
        pipeline.zremrangebyrank(key, 0, -self.window_length)
        return pipeline.execute()

    def merge(self, a, b):
        return a + b
