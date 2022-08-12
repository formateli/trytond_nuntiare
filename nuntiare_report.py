# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os
import tempfile
from trytond.pool import Pool
from trytond.report import Report
from trytond.config import config
from trytond.transaction import Transaction
from . import NuntiareReport, Render


class Nuntiare(Report):
    @classmethod
    def execute(cls, ids, data):
        pool = Pool()
        ActionReport = pool.get('ir.action.report')
        cls.check_access()

        action_id = data.get('action_id')
        if action_id is None:
            action_reports = ActionReport.search([
                    ('report_name', '=', cls.__name__)
                    ])
            assert action_reports, '%s not found' % cls
            action_report = action_reports[0]
        else:
            action_report = ActionReport(action_id)

        report_context = cls.get_context(None, None, data)
        oext = cls.get_extension(action_report, data)
        content = cls.render(
            action_report,
            report_context,
            oext=oext)

        return (oext, content, action_report.direct_print, action_report.name)

    @classmethod
    def render(cls, report, report_context, oext='pdf'):
        fd, path = cls._prepare_template_file(report)
        os.close(fd)

        rpt = NuntiareReport(path)
        rpt.run(
            cls.get_parameters(report_context['data']))

        render = Render.get_render(oext)
        render.render(rpt, overwrite=False)

        result_path = path.replace('.xml', '.' + oext)
        with open(result_path, 'rb') as message:
            data = message.read()

        os.remove(result_path)
        os.remove(path)

        return data

    @classmethod
    def _prepare_template_file(cls, report):
        # Convert to str as value from DB is not supported by StringIO
        report_content = (bytes(report.report_content) if report.report_content
            else None)
        if not report_content:
            raise Exception('Error', 'Missing report file!')

        fd, path = tempfile.mkstemp(
            suffix=(os.extsep + report.template_extension),
            prefix='trytond_')
        with open(path, 'wb') as f:
            f.write(report_content)
        return fd, path

    @classmethod
    def get_parameters(cls, data):
        result = {}
        result['conn_string'] = cls.get_conn_string()
        cls.add_company_info(result)
        for key in data:
            if key == "output_type":
                continue
            result[key] = data[key]
        return result

    @classmethod
    def add_company_info(cls, parameters):
        pool = Pool()
        res = {'company_id':None, 'company_name': None}

        company_id = Transaction().context.get('company')
        if company_id:
            Company = pool.get('company.company')
            company = Company(company_id)
            parameters['company_id'] = company.id
            parameters['company_name'] = company.party.name

    @classmethod
    def get_conn_string(cls):
        uri = config.get('database', 'uri')
        uri = uri.replace('postgresql://', '')
        uri = uri.replace('sqlite://', '')
        arroba = uri.find('@')
        user = uri[:arroba]
        host = uri[arroba + 1:]
        user, password = user.split(':')
        host, port = host.split(':')
        port = port.replace('/', '')

        conn = 'dbname=' + Transaction().database.name
        conn += ' host=' + host
        conn += ' port=' + port
        conn += ' user=' + user
        conn += ' password=' + password
        conn += ' client_encoding=UNICODE connect_timeout=0'

        return conn

    @classmethod
    def get_extension(cls, report_action, data):
        output_format = data.get('output_type', None)
        if not output_format:
            output_format = report_action.extension
        return output_format
