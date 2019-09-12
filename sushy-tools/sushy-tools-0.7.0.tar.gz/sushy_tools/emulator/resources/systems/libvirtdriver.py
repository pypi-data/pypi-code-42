# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
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

from collections import defaultdict
from collections import namedtuple
import logging
import os
import uuid
import xml.etree.ElementTree as ET

from sushy_tools.emulator import constants
from sushy_tools.emulator import memoize
from sushy_tools.emulator.resources.systems.base import AbstractSystemsDriver
from sushy_tools import error

try:
    import libvirt

except ImportError:
    libvirt = None


is_loaded = bool(libvirt)


logger = logging.getLogger(__name__)


BiosProcessResult = namedtuple('BiosProcessResult',
                               ['tree',
                                'attributes_written',
                                'bios_attributes'])


class libvirt_open(object):

    def __init__(self, uri, readonly=False):
        self._uri = uri
        self._readonly = readonly

    def __enter__(self):
        try:
            self._conn = (libvirt.openReadOnly(self._uri)
                          if self._readonly else
                          libvirt.open(self._uri))

            return self._conn

        except libvirt.libvirtError as e:
            msg = ('Error when connecting to the libvirt URI "%(uri)s": '
                   '%(error)s' % {'uri': self._uri, 'error': e})
            raise error.FishyError(msg)

    def __exit__(self, type, value, traceback):
        self._conn.close()


class LibvirtDriver(AbstractSystemsDriver):
    """Libvirt driver"""

    # XML schema: https://libvirt.org/formatdomain.html#elementsOSBIOS

    BOOT_DEVICE_MAP = {
        constants.DEVICE_TYPE_PXE: 'network',
        constants.DEVICE_TYPE_HDD: 'hd',
        constants.DEVICE_TYPE_CD: 'cdrom',
        constants.DEVICE_TYPE_FLOPPY: 'floppy'
    }

    BOOT_DEVICE_MAP_REV = {v: k for k, v in BOOT_DEVICE_MAP.items()}

    LIBVIRT_URI = 'qemu:///system'

    BOOT_MODE_MAP = {
        'Legacy': 'rom',
        'Uefi': 'pflash'
    }

    BOOT_MODE_MAP_REV = {v: k for k, v in BOOT_MODE_MAP.items()}

    BOOT_LOADER_MAP = {
        'Uefi': {
            'x86_64': '/usr/share/OVMF/OVMF_CODE.fd',
            'aarch64': '/usr/share/AAVMF/AAVMF_CODE.fd'
        },
        'Legacy': {
            'x86_64': None,
            'aarch64': None
        }

    }

    DEVICE_TYPE_MAP = {
        constants.DEVICE_TYPE_CD: 'cdrom',
        constants.DEVICE_TYPE_FLOPPY: 'floppy',
    }

    DEVICE_TYPE_MAP_REV = {v: k for k, v in DEVICE_TYPE_MAP.items()}

    # target device, controller ID, controller unit number
    DEVICE_TARGET_MAP = {
        constants.DEVICE_TYPE_FLOPPY: ('fda', 'fdc', '0'),
        constants.DEVICE_TYPE_CD: ('hdc', 'ide', '1')
    }

    DEFAULT_BIOS_ATTRIBUTES = {"BootMode": "Uefi",
                               "EmbeddedSata": "Raid",
                               "NicBoot1": "NetworkBoot",
                               "ProcTurboMode": "Enabled"}

    STORAGE_POOL = 'default'

    STORAGE_VOLUME_XML = """
<volume type='file'>
  <name>%(name)s</name>
  <key>%(path)s</key>
  <capacity unit='bytes'>%(size)i</capacity>
  <physical unit='bytes'>%(size)i</physical>
  <target>
    <path>%(path)s</path>
    <format type='raw'/>
  </target>
</volume>
"""

    @classmethod
    def initialize(cls, config, uri=None):
        cls._config = config
        cls._uri = uri or cls.LIBVIRT_URI
        cls.BOOT_LOADER_MAP = cls._config.get(
            'SUSHY_EMULATOR_BOOT_LOADER_MAP', cls.BOOT_LOADER_MAP)
        cls.KNOWN_BOOT_LOADERS = set(y for x in cls.BOOT_LOADER_MAP.values()
                                     for y in x.values())
        return cls

    @memoize.memoize()
    def _get_domain(self, identity, readonly=False):
        with libvirt_open(self._uri, readonly=readonly) as conn:
            try:
                uu_identity = uuid.UUID(identity)

                return conn.lookupByUUID(uu_identity.bytes)

            except (ValueError, libvirt.libvirtError):
                try:
                    domain = conn.lookupByName(identity)

                except libvirt.libvirtError as ex:
                    msg = ('Error finding domain by name/UUID "%(identity)s" '
                           'at libvirt URI %(uri)s": %(err)s' %
                           {'identity': identity,
                            'uri': self._uri, 'err': ex})

                    logger.debug(msg)

                    raise error.FishyError(msg)

            raise error.AliasAccessError(domain.UUIDString())

    @property
    def driver(self):
        """Return human-friendly driver information

        :returns: driver information as string
        """
        return '<libvirt>'

    @property
    def systems(self):
        """Return available computer systems

        :returns: list of UUIDs representing the systems
        """
        with libvirt_open(self._uri, readonly=True) as conn:
            return [domain.UUIDString() for domain in conn.listAllDomains()]

    def uuid(self, identity):
        """Get computer system UUID

        The universal unique identifier (UUID) for this system. Can be used
        in place of system name if there are duplicates.

        :param identity: libvirt domain name or UUID

        :returns: computer system UUID
        """
        domain = self._get_domain(identity, readonly=True)
        return domain.UUIDString()

    def name(self, identity):
        """Get computer system name by name

        :param identity: libvirt domain name or UUID

        :returns: computer system name
        """
        domain = self._get_domain(identity, readonly=True)
        return domain.name()

    def get_power_state(self, identity):
        """Get computer system power state

        :param identity: libvirt domain name or ID

        :returns: current power state as *On* or *Off* `str` or `None`
            if power state can't be determined
        """
        domain = self._get_domain(identity, readonly=True)
        return 'On' if domain.isActive() else 'Off'

    def set_power_state(self, identity, state):
        """Set computer system power state

        :param identity: libvirt domain name or ID
        :param state: string literal requesting power state transition.
            If not specified, current system power state is returned.
            Valid values  are: *On*, *ForceOn*, *ForceOff*, *GracefulShutdown*,
            *GracefulRestart*, *ForceRestart*, *Nmi*.

        :raises: `error.FishyError` if power state can't be set
        """
        domain = self._get_domain(identity)

        try:
            if state in ('On', 'ForceOn'):
                if not domain.isActive():
                    domain.create()
            elif state == 'ForceOff':
                if domain.isActive():
                    domain.destroy()
            elif state == 'GracefulShutdown':
                if domain.isActive():
                    domain.shutdown()
            elif state == 'GracefulRestart':
                if domain.isActive():
                    domain.reboot()
            elif state == 'ForceRestart':
                if domain.isActive():
                    domain.reset()
            elif state == 'Nmi':
                if domain.isActive():
                    domain.injectNMI()

        except libvirt.libvirtError as e:
            msg = ('Error changing power state at libvirt URI "%(uri)s": '
                   '%(error)s' % {'uri': self._uri, 'error': e})

            raise error.FishyError(msg)

    def get_boot_device(self, identity):
        """Get computer system boot device name

        :param identity: libvirt domain name or ID

        :returns: boot device name as `str` or `None` if device name
            can't be determined
        """
        domain = self._get_domain(identity, readonly=True)

        tree = ET.fromstring(domain.XMLDesc())

        boot_element = tree.find('.//boot')
        if boot_element is not None:
            boot_source_target = (
                self.BOOT_DEVICE_MAP_REV.get(boot_element.get('dev'))
            )

            return boot_source_target

    def set_boot_device(self, identity, boot_source):
        """Get/Set computer system boot device name

        :param identity: libvirt domain name or ID
        :param boot_source: optional string literal requesting boot device
            change on the system. If not specified, current boot device is
            returned. Valid values are: *Pxe*, *Hdd*, *Cd*.

        :raises: `error.FishyError` if boot device can't be set
        """
        domain = self._get_domain(identity)

        # XML schema: https://libvirt.org/formatdomain.html#elementsOSBIOS
        tree = ET.fromstring(domain.XMLDesc())

        try:
            target = self.BOOT_DEVICE_MAP[boot_source]

        except KeyError:
            msg = ('Unknown power state requested: '
                   '%(boot_source)s' % {'boot_source': boot_source})

            raise error.FishyError(msg)

        for os_element in tree.findall('os'):
            # Remove all "boot" elements
            for boot_element in os_element.findall('boot'):
                os_element.remove(boot_element)

            # Add a new boot element with the request boot device
            boot_element = ET.SubElement(os_element, 'boot')
            boot_element.set('dev', target)

        try:
            with libvirt_open(self._uri) as conn:
                conn.defineXML(ET.tostring(tree).decode('utf-8'))

        except libvirt.libvirtError as e:
            msg = ('Error changing boot device at libvirt URI "%(uri)s": '
                   '%(error)s' % {'uri': self._uri, 'error': e})

            raise error.FishyError(msg)

    def get_boot_mode(self, identity):
        """Get computer system boot mode.

        :returns: either *Uefi* or *Legacy* as `str` or `None` if
            current boot mode can't be determined
        """
        domain = self._get_domain(identity, readonly=True)

        # XML schema: https://libvirt.org/formatdomain.html#elementsOSBIOS
        tree = ET.fromstring(domain.XMLDesc())

        loader_element = tree.find('.//loader')

        if loader_element is not None:
            boot_mode = (
                self.BOOT_MODE_MAP_REV.get(loader_element.get('type'))
            )

            return boot_mode

    def set_boot_mode(self, identity, boot_mode):
        """Set computer system boot mode.

        :param boot_mode: optional string literal requesting boot mode
            change on the system. If not specified, current boot mode is
            returned. Valid values are: *Uefi*, *Legacy*.

        :raises: `error.FishyError` if boot mode can't be set
        """
        domain = self._get_domain(identity, readonly=True)

        # XML schema: https://libvirt.org/formatdomain.html#elementsOSBIOS
        tree = ET.fromstring(domain.XMLDesc())

        try:
            loader_type = self.BOOT_MODE_MAP[boot_mode]

        except KeyError:
            msg = ('Unknown boot mode requested: '
                   '%(boot_mode)s' % {'boot_mode': boot_mode})

            raise error.FishyError(msg)

        os_elements = tree.findall('os')
        if len(os_elements) != 1:
            msg = ('Can\'t set boot mode because "os" element must be present '
                   'exactly once in domain "%(identity)s" '
                   'configuration' % {'identity': identity})
            raise error.FishyError(msg)

        os_element = os_elements[0]

        type_element = os_element.find('type')
        if type_element is None:
            os_arch = None

        else:
            os_arch = type_element.get('arch')

        try:
            loader_path = self.BOOT_LOADER_MAP[boot_mode][os_arch]

        except KeyError:
            logger.warning('Boot loader binary is not configured for '
                           'boot mode %s and OS architecture %s. '
                           'Assuming default boot loader for the domain.',
                           boot_mode, os_arch)
            loader_path = None

        loader_elements = os_element.findall('loader')
        if len(loader_elements) > 1:
            msg = ('Can\'t set boot mode because "loader" element must be '
                   'present exactly once in domain "%(identity)s" '
                   'configuration' % {'identity': identity})
            raise error.FishyError(msg)

        if loader_elements:
            loader_element = loader_elements[0]

            if loader_element.text not in self.KNOWN_BOOT_LOADERS:
                msg = ('Unknown boot loader path "%(path)s" in domain '
                       '"%(identity)s" configuration encountered while '
                       'setting boot mode "%(mode)s", system architecture '
                       '"%(arch)s". Consider adding this loader path to '
                       'emulator config.' % {'identity': identity,
                                             'mode': boot_mode,
                                             'arch': os_arch,
                                             'path': loader_element.text})
                raise error.FishyError(msg)

            if loader_path:
                loader_element.set('type', loader_type)
                loader_element.set('readonly', 'yes')
                loader_element.text = loader_path

            else:
                # NOTE(etingof): path must be present or element must be absent
                os_element.remove(loader_element)

        elif loader_path:
            loader_element = ET.SubElement(os_element, 'loader')
            loader_element.set('type', loader_type)
            loader_element.set('readonly', 'yes')
            loader_element.text = loader_path

        with libvirt_open(self._uri) as conn:

            try:
                conn.defineXML(ET.tostring(tree).decode('utf-8'))

            except libvirt.libvirtError as e:
                msg = ('Error changing boot mode at libvirt URI '
                       '"%(uri)s": %(error)s' % {'uri': self._uri,
                                                 'error': e})

                raise error.FishyError(msg)

    def get_total_memory(self, identity):
        """Get computer system total memory

        :param identity: libvirt domain name or ID

        :returns: available RAM in GiB as `int` or `None` if total memory
            count can't be determined
        """
        domain = self._get_domain(identity, readonly=True)
        return int(domain.maxMemory() / 1024 / 1024)

    def get_total_cpus(self, identity):
        """Get computer system total count of available CPUs

        :param identity: libvirt domain name or ID

        :returns: available CPU count as `int` or `None` if CPU count
            can't be determined
        """
        domain = self._get_domain(identity, readonly=True)

        tree = ET.fromstring(domain.XMLDesc())

        total_cpus = 0

        if domain.isActive():
            total_cpus = domain.maxVcpus()

        # If we can't get it from maxVcpus() try to find it by
        # inspecting the domain XML
        if total_cpus <= 0:
            vcpu_element = tree.find('.//vcpu')
            if vcpu_element is not None:
                total_cpus = int(vcpu_element.text)

        return total_cpus or None

    def _process_bios_attributes(self,
                                 domain_xml,
                                 bios_attributes=DEFAULT_BIOS_ATTRIBUTES,
                                 update_existing_attributes=False):
        """Process Libvirt domain XML for BIOS attributes

        This method supports adding default BIOS attributes,
        retrieving existing BIOS attributes and
        updating existing BIOS attributes.

        This method is introduced to make XML testable otherwise have to
        compare XML strings to test if XML saved to libvirt is as expected.

        Sample of custom XML:
        <domain type="kvm">
        [...]
          <metadata xmlns:sushy="http://openstack.org/xmlns/libvirt/sushy">
            <sushy:bios>
              <sushy:attributes>
                <sushy:attribute name="ProcTurboMode" value="Enabled"/>
                <sushy:attribute name="BootMode" value="Uefi"/>
                <sushy:attribute name="NicBoot1" value="NetworkBoot"/>
                <sushy:attribute name="EmbeddedSata" value="Raid"/>
              </sushy:attributes>
            </sushy:bios>
          </metadata>
        [...]

        :param domain_xml: Libvirt domain XML to process
        :param bios_attributes: BIOS attributes for updates or default
            values if not specified
        :param update_existing_attributes: Update existing BIOS attributes

        :returns: namedtuple of tree: processed XML element tree,
            attributes_written: if changes were made to XML,
            bios_attributes: dict of BIOS attributes
        """
        namespace = 'http://openstack.org/xmlns/libvirt/sushy'
        ET.register_namespace('sushy', namespace)
        ns = {'sushy': namespace}

        tree = ET.fromstring(domain_xml)
        metadata = tree.find('metadata')

        if metadata is None:
            metadata = ET.SubElement(tree, 'metadata')
        bios = metadata.find('sushy:bios', ns)

        attributes_written = False
        if bios is not None and update_existing_attributes:
            metadata.remove(bios)
            bios = None
        if bios is None:
            bios = ET.SubElement(metadata, '{%s}bios' % (namespace))
            attributes = ET.SubElement(bios, '{%s}attributes' % (namespace))
            for key, value in sorted(bios_attributes.items()):
                ET.SubElement(attributes,
                              '{%s}attribute' % (namespace),
                              name=key,
                              value=value)
            attributes_written = True

        bios_attributes = {atr.attrib['name']: atr.attrib['value']
                           for atr in tree.find('.//sushy:attributes', ns)}

        return BiosProcessResult(tree, attributes_written, bios_attributes)

    def _process_bios(self, identity,
                      bios_attributes=DEFAULT_BIOS_ATTRIBUTES,
                      update_existing_attributes=False):
        """Process Libvirt domain XML for BIOS attributes and update it if necessary

        :param identity: libvirt domain name or ID
        :param bios_attributes: Full list of BIOS attributes to use if
            they are missing or update necessary
        :param update_existing_attributes: Update existing BIOS attributes

        :returns: New or existing dict of BIOS attributes

        :raises: `error.FishyError` if BIOS attributes cannot be saved
        """
        domain = self._get_domain(identity)

        result = self._process_bios_attributes(domain.XMLDesc(),
                                               bios_attributes,
                                               update_existing_attributes)

        if result.attributes_written:

            try:
                with libvirt_open(self._uri) as conn:
                    conn.defineXML(ET.tostring(result.tree).decode('utf-8'))

            except libvirt.libvirtError as e:
                msg = ('Error updating BIOS attributes'
                       ' at libvirt URI "%(uri)s": '
                       '%(error)s' % {'uri': self._uri, 'error': e})
                raise error.FishyError(msg)

        return result.bios_attributes

    def get_bios(self, identity):
        """Get BIOS section

        If there are no BIOS attributes, domain is updated with default values.

        :param identity: libvirt domain name or ID
        :returns: dict of BIOS attributes
        """
        return self._process_bios(identity)

    def set_bios(self, identity, attributes):
        """Update BIOS attributes

        These values do not have any effect on VM. This is a workaround
        because there is no libvirt API to manage BIOS settings.
        By storing fake BIOS attributes they are attached to VM and are
        persisted through VM lifecycle.

        Updates to attributes are immediate unlike in real BIOS that
        would require system reboot.

        :param identity: libvirt domain name or ID
        :param attributes: dict of BIOS attributes to update. Can pass only
            attributes that need update, not all
        """
        bios_attributes = self.get_bios(identity)

        bios_attributes.update(attributes)

        self._process_bios(identity, bios_attributes,
                           update_existing_attributes=True)

    def reset_bios(self, identity):
        """Reset BIOS attributes to default

        :param identity: libvirt domain name or ID
        """
        self._process_bios(identity, self.DEFAULT_BIOS_ATTRIBUTES,
                           update_existing_attributes=True)

    def get_nics(self, identity):
        """Get list of network interfaces and their MAC addresses

        Use MAC address as network interface's id

        :param identity: libvirt domain name or ID

        :returns: list of network interfaces dict with their attributes
        """
        domain = self._get_domain(identity, readonly=True)
        tree = ET.fromstring(domain.XMLDesc())
        return [{'id': iface.get('address'), 'mac': iface.get('address')}
                for iface in tree.findall(
                ".//devices/interface[@type='network']/mac")]

    def get_boot_image(self, identity, device):
        """Get backend VM boot image info

        :param identity: node name or ID
        :param device: device type (from
            `sushy_tools.emulator.constants`)
        :returns: a `tuple` of (boot_image, write_protected, inserted)
        :raises: `error.FishyError` if boot device can't be accessed
        """
        domain = self._get_domain(identity, readonly=True)

        tree = ET.fromstring(domain.XMLDesc())

        device_element = tree.find('devices')
        if device_element is None:
            msg = ('Missing "devices" tag in the libvirt domain '
                   '"%(identity)s" configuration' % {'identity': identity})
            raise error.FishyError(msg)

        for disk_element in device_element.findall('disk'):
            dev_type = disk_element.attrib.get('device')
            if (dev_type not in self.DEVICE_TYPE_MAP_REV or
                    dev_type != self.DEVICE_TYPE_MAP.get(device)):
                continue

            source_element = disk_element.find('source')
            if source_element is None:
                continue

            boot_image = source_element.attrib.get('file')
            if boot_image is None:
                continue

            read_only = disk_element.find('readonly') or False

            inserted = (self.get_boot_device(identity) ==
                        constants.DEVICE_TYPE_CD)
            if inserted:
                inserted = self.get_boot_mode(identity) == 'Uefi'

            return boot_image, read_only, inserted

        return '', False, False

    def _upload_image(self, domain, conn, boot_image):
        pool = conn.storagePoolLookupByName(self.STORAGE_POOL)

        pool_tree = ET.fromstring(pool.XMLDesc())

        # Find out path to images
        pool_path_element = pool_tree.find('target/path')
        if pool_path_element is None:
            msg = ('Missing "target/path" tag in the libvirt '
                   'storage pool "%(pool)s"'
                   '' % {'pool': self.STORAGE_POOL})
            raise error.FishyError(msg)

        image_name = '%s-%s.img' % (
            os.path.basename(boot_image).replace('.', '-'),
            domain.UUIDString())

        image_path = os.path.join(
            pool_path_element.text, image_name)

        image_size = os.stat(boot_image).st_size

        # Remove already existing volume

        volumes_names = [v.name() for v in pool.listAllVolumes()]
        if image_name in volumes_names:
            volume = pool.storageVolLookupByName(image_name)
            volume.delete()

        # Create new volume

        volume = pool.createXML(
            self.STORAGE_VOLUME_XML % {
                'name': image_name, 'path': image_path,
                'size': image_size})

        # Upload image to hypervisor

        stream = conn.newStream()
        volume.upload(stream, 0, image_size)

        def read_file(stream, nbytes, fl):
            return fl.read(nbytes)

        stream.sendAll(read_file, open(boot_image, 'rb'))

        stream.finish()

        return image_path

    def _add_boot_image(self, domain, domain_tree, device,
                        boot_image, write_protected):

        identity = domain.UUIDString()

        device_element = domain_tree.find('devices')
        if device_element is None:
            msg = ('Missing "devices" tag in the libvirt domain '
                   '"%(identity)s" configuration' % {'identity': identity})
            raise error.FishyError(msg)

        with libvirt_open(self._uri) as conn:

            image_path = self._upload_image(domain, conn, boot_image)

            try:
                lv_device = self.BOOT_DEVICE_MAP[device]

            except KeyError:
                raise error.FishyError(
                    'Unknown device %s at %s' % (device, identity))

            # Add disk element pointing to the boot image

            disk_element = ET.SubElement(device_element, 'disk')
            disk_element.set('type', 'file')
            disk_element.set('device', lv_device)

            tgt_dev, tgt_bus, tgt_unit = self.DEVICE_TARGET_MAP[device]

            target_element = ET.SubElement(disk_element, 'target')
            target_element.set('dev', tgt_dev)
            target_element.set('bus', tgt_bus)

            driver_element = ET.SubElement(disk_element, 'driver')
            driver_element.set('name', 'qemu')
            driver_element.set('type', 'raw')

            address_element = ET.SubElement(disk_element, 'address')
            address_element.set('type', 'drive')
            address_element.set('controller', '0')
            address_element.set('bus', '0')
            address_element.set('target', '0')
            address_element.set('unit', tgt_unit)

            source_element = ET.SubElement(disk_element, 'source')
            source_element.set('file', image_path)

            if write_protected:
                ET.SubElement(disk_element, 'readonly')

    def _remove_boot_images(self, domain, domain_tree, device):

        identity = domain.UUIDString()

        device_element = domain_tree.find('devices')
        if device_element is None:
            msg = ('Missing "devices" tag in the libvirt domain '
                   '"%(identity)s" configuration' % {'identity': identity})
            raise error.FishyError(msg)

        try:
            lv_device = self.BOOT_DEVICE_MAP[device]

        except KeyError:
            raise error.FishyError(
                'Unknown device %s at %s' % (device, identity))

        device_element = domain_tree.find('devices')
        if device_element is None:
            msg = ('Missing "devices" tag in the libvirt domain '
                   '"%(identity)s" configuration' % {'identity': identity})
            raise error.FishyError(msg)

        # First, remove all existing devices
        disk_elements = device_element.findall('disk')

        for disk_element in disk_elements:
            dev_type = disk_element.attrib.get('device')
            if dev_type == lv_device:
                device_element.remove(disk_element)

    def set_boot_image(self, identity, device, boot_image=None,
                       write_protected=True):
        """Set backend VM boot image

        :param identity: node name or ID
        :param device: device type (from
            `sushy_tools.emulator.constants`)
        :param boot_image: path to the image file or `None` to remove
            configured image entirely
        :param write_protected: expose media as read-only or writable

        :raises: `error.FishyError` if boot device can't be set
        """
        domain = self._get_domain(identity)

        domain_tree = ET.fromstring(domain.XMLDesc())

        self._remove_boot_images(domain, domain_tree, device)

        if boot_image:

            try:
                self._add_boot_image(domain, domain_tree, device,
                                     boot_image, write_protected)

            except libvirt.libvirtError as e:
                msg = ('Error changing boot image at libvirt URI "%(uri)s": '
                       '%(error)s' % {'uri': self._uri, 'error': e})

                raise error.FishyError(msg)

        with libvirt_open(self._uri) as conn:
            conn.defineXML(ET.tostring(domain_tree).decode('utf-8'))

    def _find_device_by_path(self, vol_path):
        """Get device attributes using path

        :param vol_path: path for the libvirt volume
        :returns: a dict (or None) of the corresponding device attributes
        """
        with libvirt_open(self._uri, readonly=True) as conn:
            try:
                vol = conn.storageVolLookupByPath(vol_path)
            except libvirt.libvirtError as e:
                msg = ('Could not find storage volume by path '
                       '"%(path)s" at libvirt URI "%(uri)s": '
                       '%(err)s' %
                       {'path': vol_path, 'uri': self._uri,
                        'err': e})
                logger.debug(msg)
                return
            disk_device = {
                'Name': vol.name(),
                'CapacityBytes': vol.info()[1]
            }
            return disk_device

    def _find_device_from_pool(self, pool_name, vol_name):
        """Get device attributes from pool

        :param pool_name: libvirt pool name
        :param vol_name: libvirt volume name
        :returns: a dict (or None) of the corresponding device attributes
        """
        with libvirt_open(self._uri, readonly=True) as conn:
            try:
                pool = conn.storagePoolLookupByName(pool_name)
            except libvirt.libvirtError as e:
                msg = ('Error finding Storage Pool by name "%(name)s" at'
                       'libvirt URI "%(uri)s": %(err)s' %
                       {'name': pool_name, 'uri': self._uri, 'err': e})
                logger.debug(msg)
                return

            try:
                vol = pool.storageVolLookupByName(vol_name)
            except libvirt.libvirtError as e:
                msg = ('Error finding Storage Volume by name "%(name)s" '
                       'in Pool '"%(pName)s"' at libvirt URI "%(uri)s"'
                       ': %(err)s' %
                       {'name': vol_name, 'pName': pool_name,
                        'uri': self._uri, 'err': e})
                logger.debug(msg)
                return
            disk_device = {
                'Name': vol.name(),
                'CapacityBytes': vol.info()[1]
            }
            return disk_device

    def get_simple_storage_collection(self, identity):
        """Get a dict of simple storage controllers and their devices

        Only those storage devices that are configured as a libvirt volume
        via a pool and attached to the domain will reflect as a device.
        Others are skipped.

        :param identity: libvirt domain or ID
        :returns: dict of simple storage controller dict with their attributes
        """
        domain = self._get_domain(identity, readonly=True)
        tree = ET.fromstring(domain.XMLDesc())
        simple_storage = defaultdict(lambda: defaultdict(DeviceList=list()))

        for disk_element in tree.findall(".//disk/target[@bus]/.."):
            source_element = disk_element.find('source')
            if source_element is not None:
                disk_type = disk_element.attrib['type']
                ctl_type = disk_element.find('target').attrib['bus']
                disk_device = None
                if disk_type in ('file', 'block'):
                    if disk_type == 'file':
                        vol_path = source_element.attrib['file']
                    else:
                        vol_path = source_element.attrib['dev']
                    disk_device = self._find_device_by_path(vol_path)
                elif disk_type == 'volume':
                    pool_name = source_element.attrib['pool']
                    vol_name = source_element.attrib['volume']
                    disk_device = self._find_device_from_pool(pool_name,
                                                              vol_name)
                if disk_device is not None:
                    simple_storage[ctl_type]['Id'] = ctl_type
                    simple_storage[ctl_type]['Name'] = ctl_type
                    simple_storage[ctl_type]['DeviceList'].append(disk_device)
        return simple_storage

    def find_or_create_storage_volume(self, data):
        """Find/create volume based on existence in the virtualization backend

        :param data: data about the volume in dict form with values for `Id`,
                     `Name`, `CapacityBytes`, `VolumeType`, `libvirtPoolName`
                     and `libvirtVolName`

        :returns: Id of the volume if successfully found/created else None
        """
        with libvirt_open(self._uri) as conn:
            try:
                poolName = data['libvirtPoolName']
            except KeyError:
                poolName = self.STORAGE_POOL
            try:
                pool = conn.storagePoolLookupByName(poolName)
            except libvirt.libvirtError as ex:
                msg = ('Error finding Storage Pool by name "%(name)s" at '
                       'libvirt URI "%(uri)s": %(err)s' %
                       {'name': poolName, 'uri': self._uri, 'err': ex})
                logger.debug(msg)
                return
            try:
                vol = pool.storageVolLookupByName(data['libvirtVolName'])
            except libvirt.libvirtError as ex:

                msg = ('Creating storage volume with name: "%s"',
                       data['libvirtVolName'])
                logger.debug(msg)

                pool_tree = ET.fromstring(pool.XMLDesc())

                # Find out path to the volume
                pool_path_element = pool_tree.find('target/path')
                if pool_path_element is None:
                    msg = ('Missing "target/path" tag in the libvirt '
                           'storage pool "%(pool)s"'
                           '' % {'pool': poolName})
                    logger.debug(msg)
                    return

                vol_path = os.path.join(
                    pool_path_element.text, data['libvirtVolName'])

                # Create a new volume
                vol = pool.createXML(
                    self.STORAGE_VOLUME_XML % {
                        'name': data['libvirtVolName'], 'path': vol_path,
                        'size': data['CapacityBytes']})

                if not vol:
                    msg = ('Error creating "%s" storage volume in "%s" pool',
                           data['libvirtVolName'], poolName)
                    logger.debug(msg)
                    return
            return data['Id']
