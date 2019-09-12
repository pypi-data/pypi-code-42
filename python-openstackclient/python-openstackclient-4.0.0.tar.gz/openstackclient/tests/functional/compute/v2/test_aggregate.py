#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import time
import uuid

from openstackclient.tests.functional import base


class AggregateTests(base.TestCase):
    """Functional tests for aggregate"""

    def wait_for_status(self, check_type, check_name, desired_status,
                        wait=120, interval=5, failures=None):
        current_status = "notset"
        if failures is None:
            failures = ['error']
        total_sleep = 0
        while total_sleep < wait:
            output = json.loads(self.openstack(
                check_type + ' show -f json ' + check_name))
            current_status = output['name']
            if (current_status == desired_status):
                print('{} {} now has status {}'
                      .format(check_type, check_name, current_status))
                return
            print('Checking {} {} Waiting for {} current status: {}'
                  .format(check_type, check_name,
                          desired_status, current_status))
            if current_status in failures:
                raise Exception(
                    'Current status {} of {} {} is one of failures {}'
                    .format(current_status, check_type, check_name, failures))
            time.sleep(interval)
            total_sleep += interval
        self.assertOutput(desired_status, current_status)

    def test_aggregate_crud(self):
        """Test create, delete multiple"""
        name1 = uuid.uuid4().hex
        cmd_output = json.loads(self.openstack(
            'aggregate create -f json ' +
            '--zone nova ' +
            '--property a=b ' +
            name1
        ))
        self.assertEqual(
            name1,
            cmd_output['name']
        )
        self.assertEqual(
            'nova',
            cmd_output['availability_zone']
        )
        self.assertIn(
            'a',
            cmd_output['properties']
        )
        self.wait_for_status('aggregate', name1, name1)
        self.addCleanup(
            self.openstack,
            'aggregate delete ' + name1,
            fail_ok=True,
        )

        name2 = uuid.uuid4().hex
        cmd_output = json.loads(self.openstack(
            'aggregate create -f json ' +
            '--zone external ' +
            name2
        ))
        self.assertEqual(
            name2,
            cmd_output['name']
        )
        self.assertEqual(
            'external',
            cmd_output['availability_zone']
        )
        self.wait_for_status('aggregate', name2, name2)
        self.addCleanup(
            self.openstack,
            'aggregate delete ' + name2,
            fail_ok=True,
        )

        # Test aggregate set
        name3 = uuid.uuid4().hex
        raw_output = self.openstack(
            'aggregate set ' +
            '--name ' + name3 + ' ' +
            '--zone internal ' +
            '--no-property ' +
            '--property c=d ' +
            name1
        )
        self.assertOutput('', raw_output)
        self.addCleanup(
            self.openstack,
            'aggregate delete ' + name3,
            fail_ok=True,
        )

        cmd_output = json.loads(self.openstack(
            'aggregate show -f json ' +
            name3
        ))
        self.assertEqual(
            name3,
            cmd_output['name']
        )
        self.assertEqual(
            'internal',
            cmd_output['availability_zone']
        )
        self.assertIn(
            'c',
            cmd_output['properties']
        )
        self.assertNotIn(
            'a',
            cmd_output['properties']
        )

        # Test aggregate list
        cmd_output = json.loads(self.openstack(
            'aggregate list -f json'
        ))
        names = [x['Name'] for x in cmd_output]
        self.assertIn(name3, names)
        self.assertIn(name2, names)
        zones = [x['Availability Zone'] for x in cmd_output]
        self.assertIn('external', zones)
        self.assertIn('internal', zones)

        # Test aggregate list --long
        cmd_output = json.loads(self.openstack(
            'aggregate list --long -f json'
        ))
        names = [x['Name'] for x in cmd_output]
        self.assertIn(name3, names)
        self.assertIn(name2, names)
        zones = [x['Availability Zone'] for x in cmd_output]
        self.assertIn('external', zones)
        self.assertIn('internal', zones)
        properties = [x['Properties'] for x in cmd_output]
        self.assertNotIn({'a': 'b'}, properties)
        self.assertIn({'c': 'd'}, properties)

        # Test unset
        raw_output = self.openstack(
            'aggregate unset ' +
            '--property c ' +
            name3
        )
        self.assertOutput('', raw_output)

        cmd_output = json.loads(self.openstack(
            'aggregate show -f json ' +
            name3
        ))
        self.assertNotIn(
            "c='d'",
            cmd_output['properties']
        )

        # test aggregate delete
        del_output = self.openstack(
            'aggregate delete ' +
            name3 + ' ' +
            name2
        )
        self.assertOutput('', del_output)

    def test_aggregate_add_and_remove_host(self):
        """Test aggregate add and remove host"""
        # Get a host
        cmd_output = json.loads(self.openstack(
            'host list -f json'
        ))
        host_name = cmd_output[0]['Host Name']

        # NOTE(dtroyer): Cells v1 is not operable with aggregates.  Hostnames
        #                are returned as rrr@host or ccc!rrr@host.
        if '@' in host_name:
            self.skipTest("Skip aggregates in a Nova cells v1 configuration")

        name = uuid.uuid4().hex
        self.openstack(
            'aggregate create ' +
            name
        )
        self.addCleanup(self.openstack, 'aggregate delete ' + name)

        # Test add host
        cmd_output = json.loads(self.openstack(
            'aggregate add host -f json ' +
            name + ' ' +
            host_name
        ))
        self.assertIn(
            host_name,
            cmd_output['hosts']
        )

        # Test remove host
        cmd_output = json.loads(self.openstack(
            'aggregate remove host -f json ' +
            name + ' ' +
            host_name
        ))
        self.assertNotIn(
            host_name,
            cmd_output['hosts']
        )
