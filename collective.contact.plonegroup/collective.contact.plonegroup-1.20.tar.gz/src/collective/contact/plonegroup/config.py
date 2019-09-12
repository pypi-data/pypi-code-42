# -*- coding: utf-8 -*-

from copy import deepcopy
from plone import api


# Registry keys
ORGANIZATIONS_REGISTRY = 'collective.contact.plonegroup.browser.settings.IContactPlonegroupConfig.organizations'
FUNCTIONS_REGISTRY = 'collective.contact.plonegroup.browser.settings.IContactPlonegroupConfig.functions'
PLONEGROUP_ORG = 'plonegroup-organization'
DEFAULT_DIRECTORY_ID = 'contacts'


def get_registry_organizations(as_copy=True):
    org_uids = api.portal.get_registry_record(ORGANIZATIONS_REGISTRY)
    if as_copy:
        org_uids = deepcopy(org_uids)
    return org_uids


def get_registry_functions(as_copy=True):
    functions = api.portal.get_registry_record(FUNCTIONS_REGISTRY)
    if as_copy:
        functions = deepcopy(functions)
    return functions


def set_registry_organizations(value):
    api.portal.set_registry_record(ORGANIZATIONS_REGISTRY, value)


def set_registry_functions(value):
    api.portal.set_registry_record(FUNCTIONS_REGISTRY, value)
