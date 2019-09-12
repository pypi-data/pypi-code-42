import pytest
import doctest
from insights.parsers import azure_instance_type
from insights.parsers.azure_instance_type import AzureInstanceType
from insights.tests import context_wrap
from insights.parsers import SkipException, ParseException
from insights.core.plugins import ContentException

AZURE_TYPE_1 = "Standard_L32s"
AZURE_TYPE_2 = "Standard_NV48s_v3"
AZURE_TYPE_DOC = "Standard_L64s_v2"
AZURE_TYPE_AB_1 = """
curl: (7) Failed to connect to 169.254.169.254 port 80: Connection timed out
""".strip()
AZURE_TYPE_AB_2 = """
curl: (7) couldn't connect to host
""".strip()
AZURE_TYPE_AB_3 = """
curl: (28) connect() timed out!
""".strip()
AZURE_TYPE_AB_4 = """
.micro
""".strip()
AZURE_TYPE_AB_5 = """
No module named insights.tools
""".strip()


def test_azure_instance_type_ab_other():
    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_1))

    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_2))

    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_3))

    with pytest.raises(ParseException) as pe:
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_4))
        assert 'Unrecognized type' in str(pe)

    with pytest.raises(ContentException) as pe:
        AzureInstanceType(context_wrap(AZURE_TYPE_AB_5))


def test_azure_instance_type_ab_empty():
    with pytest.raises(SkipException):
        AzureInstanceType(context_wrap(''))


def test_azure_instance_type():
    azure = AzureInstanceType(context_wrap(AZURE_TYPE_1))
    assert azure.type == "Standard"
    assert azure.size == "L32s"
    assert azure.version is None
    assert azure.raw == "Standard_L32s"

    azure = AzureInstanceType(context_wrap(AZURE_TYPE_2))
    assert azure.type == "Standard"
    assert azure.size == "NV48s"
    assert azure.version == "v3"
    assert azure.raw == "Standard_NV48s_v3"
    assert "NV48s" in str(azure)


def test_doc_examples():
    env = {
            'azure_inst': AzureInstanceType(context_wrap(AZURE_TYPE_DOC))
          }
    failed, total = doctest.testmod(azure_instance_type, globs=env)
    assert failed == 0
