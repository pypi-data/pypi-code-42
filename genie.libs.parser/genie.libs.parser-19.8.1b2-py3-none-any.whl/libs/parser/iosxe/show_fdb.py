"""show_fdb.py
   supported commands:
     *  show mac address-table
     *  show mac address-table aging-time
     *  show mac address-table learning
"""
# Python
import re

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, \
                                         Any, \
                                         Optional, \
                                         Or, \
                                         And, \
                                         Default, \
                                         Use

# import parser utils
from genie.libs.parser.utils.common import Common


class ShowMacAddressTableSchema(MetaParser):
    """Schema for show mac address-table"""
    schema = {
        'mac_table': {
            'vlans': {
                Any(): {
                    'vlan': Or(int, str),
                    'mac_addresses': {
                        Any(): {
                            'mac_address': str,
                            Optional('drop'): {
                                'drop': bool,
                                'entry_type': str
                            },
                            Optional('interfaces'): {
                                Any(): {
                                    'interface': str,
                                    'entry_type': str,
                                    Optional('entry'): str,
                                    Optional('learn'): str,
                                    Optional('age'): int
                                }
                            }
                        }
                    }
                }
            }
        },
        Optional('total_mac_addresses'): int,
    }

class ShowMacAddressTable(ShowMacAddressTableSchema):
    """Parser for show mac address-table"""

    cli_command = 'show mac address-table'

    def cli(self,output=None):
        if output is None:
            # get output from device
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        ret_dict = mac_dict = {}
        entry_type = entry = learn = age = ''
        
        # initial regexp pattern
        p1 = re.compile(r'^Total +Mac +Addresses +for +this +criterion: +(?P<val>\d+)$')
        p2 = re.compile(r'^(?P<entry>[\w\*] )?\s*(?P<vlan>All|[\d\-]+) +(?P<mac>[\w.]+)'
            ' +(?P<entry_type>\w+) +(?P<intfs>\S+|[^\s]+\s[^\s]+)$')
        p3 = re.compile(r'^(?P<intfs>(vPC Peer-Link)?[\w\/\,\(\)]+)$')
        p4 = re.compile(r'^(?P<entry>[\w\*] )?\s*(?P<vlan>All|[\d\-]+) +(?P<mac>[\w.]+)'
            ' +(?P<entry_type>\w+) +(?P<learn>\w+) +(?P<age>[\d\-\~]+) '
            '+(?P<intfs>(vPC )?[\w\/\,\-\(\)]+)$')
        p5 = re.compile(r'^(?P<entry>[\w\*] )?\s*(?P<vlan>All|[\d\-]+) +(?P<mac>[\w.]+)'
            ' +(?P<entry_type>\w+) +(?P<age>[\d\-\~]+) +(?P<secure>\w+) '
            '+(?P<ntfy>\w+) +(?P<intfs>(vPC )?[\w\/\,\-\(\)]+)$')
        
        for line in out.splitlines():
            line = line.strip()

            # Total Mac Addresses for this criterion: 93
            m = p1.match(line)
            if m:
                ret_dict.update({'total_mac_addresses': int(m.groupdict()['val'])})
                continue

            # 10    aaaa.bbbb.cccc    STATIC      Gi1/0/8 Gi1/0/9
            # 20    aaaa.bbbb.cccc    STATIC      Drop
            # All    0100.0ccc.cccd    STATIC      CPU
            m = p2.match(line)
            if m:
                group = m.groupdict()
                mac = group['mac']
                vlan = int(group['vlan']) if re.search('\d+', group['vlan']) \
                                          else group['vlan'].lower()
                intfs = group['intfs'].strip()
                vlan_dict = ret_dict.setdefault('mac_table', {}) \
                .setdefault('vlans', {}).setdefault(str(vlan), {})
                vlan_dict['vlan'] = vlan
                mac_dict = vlan_dict.setdefault('mac_addresses', {}) \
                                    .setdefault(mac, {})
                mac_dict.update({'mac_address': mac})

                if 'drop' in intfs.lower():
                    drop_dict = mac_dict.setdefault('drop', {})
                    drop_dict.update({'drop': True})
                    drop_dict.update({'entry_type': group['entry_type'].lower()})
                    continue

                for intf in intfs.replace(' ',',').split(','):
                    intf = Common.convert_intf_name(intf)
                    intf_dict = mac_dict.setdefault('interfaces', {}) \
                                        .setdefault(intf, {})
                    intf_dict.update({'interface': intf})
                    entry_type = group['entry_type'].lower()
                    intf_dict.update({'entry_type': entry_type})
                    if group['entry']:
                        entry = group['entry'].strip()
                        intf_dict.update({'entry': entry})
                continue

            # Gi1/9,Gi1/10,Gi1/11,Gi1/12
            #               Router,Switch
            m = p3.match(line)
            if m:
                group = m.groupdict()
                intfs = group['intfs'].strip()

                if 'drop' in intfs.lower():
                    drop_dict = mac_dict.setdefault('drop', {})
                    drop_dict.update({'drop': True})
                    drop_dict.update({'entry_type': entry_type})
                    continue

                for intf in intfs.split(','):
                    intf = Common.convert_intf_name(intf)
                    intf_dict = mac_dict.setdefault('interfaces', {}) \
                                        .setdefault(intf, {})
                    intf_dict.update({'interface': intf})
                    intf_dict.update({'entry_type': entry_type})
                    if entry:
                        intf_dict.update({'entry': entry})
                    if learn:
                        intf_dict.update({'learn': learn})
                    if age:
                        intf_dict.update({'age': age})
                continue

            # *  101  44dd.ee55.ff66   dynamic  Yes         10   Gi1/40
            # *  102  aa11.bb22.cc33    static  Yes          -   Gi1/2,Gi1/4,Gi1/5,Gi1/6
            # *  400  0000.0000.0000    static  No           -   vPC Peer-Link
            # *  ---  0000.0000.0000    static  No           -   Router
            m = p4.match(line)
            if m:
                group = m.groupdict()
                mac = group['mac']
                vlan = int(group['vlan']) if re.search('\d+', group['vlan']) \
                                          else group['vlan'].lower()
                intfs = group['intfs'].strip()
                vlan_dict = ret_dict.setdefault('mac_table', {}) \
                .setdefault('vlans', {}).setdefault(str(vlan), {})
                vlan_dict['vlan'] = vlan
                mac_dict = vlan_dict.setdefault('mac_addresses', {}) \
                                    .setdefault(mac, {})
                mac_dict.update({'mac_address': mac})

                if 'drop' in intfs.lower():
                    drop_dict = mac_dict.setdefault('drop', {})
                    drop_dict.update({'drop': True})
                    drop_dict.update({'entry_type': group['entry_type'].lower()})
                    continue

                for intf in intfs.split(','):
                    intf = Common.convert_intf_name(intf)
                    intf_dict = mac_dict.setdefault('interfaces', {}) \
                                        .setdefault(intf, {})
                    intf_dict.update({'interface': intf})
                    entry_type = group['entry_type'].lower()
                    intf_dict.update({'entry_type': entry_type})
                    if group['entry']:
                        entry = group['entry'].strip()
                        intf_dict.update({'entry': entry})
                    if group['learn']:
                        learn = group['learn']
                        intf_dict.update({'learn': learn})
                    if group['age']:
                        if group['age'].isdigit():
                            age = int(group['age'])
                            intf_dict.update({'age': age})
                        else:
                            age = None
                continue

        return ret_dict


class ShowMacAddressTableAgingTimeSchema(MetaParser):
    """Schema for show mac address-table aging-time"""
    schema = {
        'mac_aging_time': int,
        Optional('vlans'): {
            Any(): {
                'mac_aging_time': int,
                'vlan': Or(int, str)
            }
        }
    }

class ShowMacAddressTableAgingTime(ShowMacAddressTableAgingTimeSchema):
    """Parser for show mac address-table aging-time"""

    cli_command = 'show mac address-table aging-time'

    def cli(self,output=None):
        if output is None:
            # get output from device
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        ret_dict = {}

        # initial regexp pattern
        p1 = re.compile(r'^Global +Aging +Time: +(?P<time>\d+)$')
        p2 = re.compile(r'^(?P<vlan>\w+) +(?P<time>\d+)$')

        for line in out.splitlines():
            line = line.strip()

            # Global Aging Time:    0
            m = p1.match(line)
            if m:
                ret_dict.update({'mac_aging_time': int(m.groupdict()['time'])})
                continue

            # Vlan    Aging Time
            # ----    ----------
            #   10      10
            m = p2.match(line)
            if m:
                group = m.groupdict()
                vlan = int(group['vlan']) if re.search('\d+', group['vlan']) \
                else group['vlan'].lower()

                vlan_dict = ret_dict.setdefault('vlans', {}) \
                .setdefault(str(vlan), {})
                vlan_dict.update({'vlan': vlan})
                vlan_dict.update({'mac_aging_time': int(m.groupdict()['time'])})
                continue

        return ret_dict


class ShowMacAddressTableLearningSchema(MetaParser):
    """Schema for show mac address-table learning"""
    schema = {
        'vlans': {
            Any(): {
                'mac_learning': bool,
                'vlan': Or(int, str)
            }
        }
    }

class ShowMacAddressTableLearning(ShowMacAddressTableLearningSchema):
    """Parser for show mac address-table learning"""

    cli_command = 'show mac address-table learning'

    def cli(self,output=None):
        if output is None:
            # get output from device
            out = self.device.execute(self.cli_command)
        else:
            out = output
        # initial return dictionary
        ret_dict = {}

        # initial regexp pattern
        p1 = re.compile(r'^Learning +disabled +on +vlans: +(?P<vlans>[\w\,\-\s]+)$')

        for line in out.splitlines():
            line = line.strip()

            # Learning disabled on vlans: 10,101-103,105
            m = p1.match(line)
            if m:
                vlans = m.groupdict()['vlans']
                # generate the list of the vlans
                vlans = vlans.split(',')
                vlan_list = []
                for vlan in vlans:
                    vlan_list.append(vlan) if '-' not in vlan else \
                        vlan_list.extend(list(range(int(vlan.split('-')[0]), \
                            int(vlan.split('-')[1]) + 1)))
                for vlan in vlan_list:
                    try:
                        vlan = int(vlan)
                    except Exception:
                        vlan = vlan.lower()
                    ret_dict.setdefault('vlans', {}).setdefault(str(vlan), {}) \
                                                    .setdefault('mac_learning', False)
                    ret_dict.setdefault('vlans', {}).setdefault(str(vlan), {}) \
                                                    .setdefault('vlan', vlan)
                continue

        return ret_dict
