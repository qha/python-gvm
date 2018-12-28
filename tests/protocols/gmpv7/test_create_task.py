# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import warnings

from gvm.errors import RequiredArgument, InvalidArgument
from gvm.protocols.gmpv7 import Gmp

from .. import MockConnection


class GMPCreateTaskCommandTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_create_task(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '</create_task>'
        )

    def test_create_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name=None,
                config_id='c1',
                target_id='t1',
                scanner_id='s1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='',
                config_id='c1',
                target_id='t1',
                scanner_id='s1',
            )

    def test_create_task_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='foo',
                config_id=None,
                target_id='t1',
                scanner_id='s1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='foo',
                config_id='',
                target_id='t1',
                scanner_id='s1',
            )

    def test_create_task_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id=None,
                scanner_id='s1',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id='',
                scanner_id='s1',
            )

    def test_create_task_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id='t1',
                scanner_id=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id='t1',
                scanner_id='',
            )

    def test_create_task_with_comment(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            comment='bar',
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<comment>bar</comment>'
            '</create_task>'
        )

    def test_create_task_single_alert(self):

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id='t1',
                scanner_id='s1',
                alert_ids='a1', # will be removed in future
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            '</create_task>'
        )

        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            alert_ids=['a1'],
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            '</create_task>'
        )

    def test_create_task_multiple_alerts(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            alert_ids=['a1', 'a2', 'a3'],
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            '<alert id="a2"/>'
            '<alert id="a3"/>'
            '</create_task>'
        )

    def test_create_task_with_alterable(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            alterable=True,
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alterable>1</alterable>'
            '</create_task>'
        )

        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            alterable=False,
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alterable>0</alterable>'
            '</create_task>'
        )

    def test_create_task_with_hosts_ordering(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            hosts_ordering='foo',
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<hosts_ordering>foo</hosts_ordering>'
            '</create_task>'
        )

    def test_create_task_with_schedule(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            schedule_id='s1',
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<schedule id="s1"/>'
            '</create_task>'
        )

    def test_create_task_with_schedule_and_schedule_periods(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            schedule_id='s1',
            schedule_periods=0,
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<schedule id="s1"/>'
            '<schedule_periods>0</schedule_periods>'
            '</create_task>'
        )

        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            schedule_id='s1',
            schedule_periods=5,
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<schedule id="s1"/>'
            '<schedule_periods>5</schedule_periods>'
            '</create_task>'
        )

    def test_create_task_with_schedule_and_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id='t1',
                scanner_id='s1',
                schedule_id='s1',
                schedule_periods='foo',
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_task(
                name='foo',
                config_id='c1',
                target_id='t1',
                scanner_id='s1',
                schedule_id='s1',
                schedule_periods=-1,
            )

    def test_create_task_with_observers(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            observers=['u1', 'u2'],
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<observers>u1,u2</observers>'
            '</create_task>'
        )


if __name__ == '__main__':
    unittest.main()
