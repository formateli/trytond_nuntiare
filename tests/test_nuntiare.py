# This file is part of nuntiare module.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
#import unittest
#import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class NuntiareTestCase(ModuleTestCase):
    'Test Nuntiare module'
    module = 'nuntiare'

    @with_transaction()
    def test_nuntiare(self):
        pool = Pool()
        Config = pool.get('nuntiare.configuration')

del ModuleTestCase
