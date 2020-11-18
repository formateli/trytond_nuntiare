# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.modules.nuntiare.nuntiare_report import Nuntiare

__all__ = ['PrintResGroup', 'ResGroupReport']


class PrintResGroup(Wizard):
    'Print Groups'
    __name__ = 'nuntiare.print_res_group'

    start = StateView('nuntiare.print.parameter',
        'nuntiare.print_parameter_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Print', 'print_', 'tryton-print', default=True),
            ])
    print_ = StateAction('nuntiare.report_res_group')

    def do_print_(self, action):
        data = {
            'output_type': self.start.output_type,
            }
        return action, data

    def transition_print_(self):
        return 'end'


class ResGroupReport(Nuntiare):
    __name__ = 'nuntiare.res_group'

    @classmethod
    def execute(cls, ids, data):
        data['str_where'] = 'id<>-1'
        if ids:
            data['str_where'] = ''
            for i in ids:
                if data['str_where'] == '':
                    data['str_where'] = ' id=' + str(i)
                else:
                    data['str_where'] = data['str_where'] + ' OR id=' + str(i)

        return super(ResGroupReport, cls).execute(ids, data)
