# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.


class Data(object):
    class Record(object):
        def __init__(self, fields):
            for field in fields:
                self.add_value(field, None)

        def add_value(self, field_name, value):
            setattr(self, field_name, value)

    def __init__(self):
        self._fields = []
        self._result = []
        self._cur_record = None

    def new_record(self):
        self._cur_record = Data.Record(self._fields)
        self._result.append(self._cur_record)

    def add_values(self, values):
        for name, value in values.items():
            self.add_value(name, value)

    def add_value(self, field_name, value):
        if field_name not in self._fields:
            raise Exception(
                "Field '{0}' is not defined.".format(field_name))
        self._cur_record.add_value(field_name, value)

    def add_fields(self, list_name):
        for name in list_name:
            self.add_field(name)

    def add_field(self, name):
        if name in self._fields:
            raise Exception(
                "Field '{0}' already in fields collection.".format(
                    name))
        self._fields.append(name)

    def get_records(self):
        return self._result
