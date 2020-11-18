# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.modules.nuntiare.nuntiare_report import Nuntiare
from trytond.modules.nuntiare.data import Data


__all__ = ['PrintResUser', 'ResUserReport']


class PrintResUser(Wizard):
    'Print Users'
    __name__ = 'nuntiare.print_res_user'

    start = StateView('nuntiare.print.parameter',
        'nuntiare.print_parameter_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Print', 'print_', 'tryton-print', default=True),
            ])
    print_ = StateAction('nuntiare.report_res_user')

    def do_print_(self, action):
        data = {
            'output_type': self.start.output_type,
            }
        return action, data

    def transition_print_(self):
        return 'end'


class ResUserReport(Nuntiare):
    __name__ = 'nuntiare.res_user'

    @classmethod
    def execute(cls, ids, data):
        User = Pool().get('res.user')

        records = Data()
        records.add_fields(['id', 'name'])

        domain = []
        if ids:
            domain = [('id', 'in', ids)]

        users = User.search(domain)
        for user in users:
            records.new_record()
            records.add_values({
                    'id': user.id,
                    'name': user.name,
                })

        data['records'] = records.get_records()

        return super(ResUserReport, cls).execute(ids, data)
