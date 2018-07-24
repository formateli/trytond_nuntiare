# This file is part of trytond-nuntiare module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

import os
import sys

# Nuntiare module searching priority:
#  1.- module located in trytond.modules.nuntiare.lib.nuntiare
#  2.- 'NUNTIARE_MODULE' environment variable
#  3.- The installed module.

if 'NUNTIARE_MODULE' in os.environ:
    sys.path.insert(0, os.environ['NUNTIARE_MODULE'])

try:
    from .lib.nuntiare.report import Report as NuntiareReport
    from .lib.nuntiare.render.render import Render
except ImportError:
    try:
        from nuntiare.report import Report as NuntiareReport
        from nuntiare.render.render import Render
    except ImportError as e:
        msg = e.args[0]
        msg += ". Module 'nuntiare' could not be loaded. " \
            "Verify that 'nuntiare' is installed " \
            "(or any dependency, like cairo) " \
            "or module is located under trytond.modules.nuntiare.lib, " \
            "or environment variable 'NUNTIARE_MODULE' is set."
        raise Exception(msg)

from trytond.pool import Pool
from .configuration import *
from .print_parameter import *
from .res_user import *
from .res_group import *

def register():
    Pool.register(
        Configuration,
        PrintParameter,
        PrintParameterDate,
        PrintParameterDates,
        module='nuntiare', type_='model')
    Pool.register(
        PrintResUser,
        PrintResGroup,
        module='nuntiare', type_='wizard')
    Pool.register(
        ResUserReport,
        ResGroupReport,
        module='nuntiare', type_='report')
