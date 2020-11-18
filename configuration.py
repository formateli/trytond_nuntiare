# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import (
    ModelSingleton, ModelView, ModelSQL, fields)

__all__ = ['Configuration']

OUTPUT_LIST = [
        ('pdf', 'PDF'),
        ('xlsx', 'XLSX'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
        ('xml', 'XML'),
    ]


class Configuration(
        ModelSingleton, ModelSQL, ModelView):
    'Nuntiare Configuration'
    __name__ = 'nuntiare.configuration'

    default_output = fields.Selection(OUTPUT_LIST,
        'Default Output', required=True)
