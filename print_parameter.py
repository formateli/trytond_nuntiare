# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from trytond.model import ModelView, fields
from .configuration import OUTPUT_LIST

__all__ = [
        'PrintParameter',
        'PrintParameterDate',
        'PrintParameterDates',
    ]

_OUTPUT_TYPE = fields.Selection(
    OUTPUT_LIST, 'Output Type', required=True)


class PrintParameter(ModelView):
    'Print Parameters'
    __name__ = 'nuntiare.print.parameter'

    output_type = _OUTPUT_TYPE

    @staticmethod
    def default_output_type():
        return get_default_output_type()


class PrintParameterDate(ModelView):
    'Print Parameter Date'
    __name__ = 'nuntiare.print.parameter.date'

    date = fields.Date('Date', required=True)
    output_type = _OUTPUT_TYPE

    @staticmethod
    def default_output_type():
        return get_default_output_type()


class PrintParameterDates(ModelView):
    'Print Parameter Dates'
    __name__ = 'nuntiare.print.parameter.dates'

    date_start = fields.Date('From', required=True)
    date_end = fields.Date('To', required=True)
    output_type = _OUTPUT_TYPE

    @staticmethod
    def default_output_type():
        return get_default_output_type()


def get_default_output_type():
    pool = Pool()
    Config = pool.get('nuntiare.configuration')
    config = Config(1)
    return config.default_output
