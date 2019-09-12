import logging
from unittest.mock import MagicMock

import pytest
import responses

_LOGGER = logging.getLogger(__name__)

VTN_ADDRESS = "https://openadr-staging"
ENDPOINT_BASE = "/OpenADR2/Simple/2.0b/"
ENDPOINT = VTN_ADDRESS + ENDPOINT_BASE
EIEVENT = ENDPOINT + "EiEvent"
EIREPORT = ENDPOINT + "EiReport"
EIREGISTERPARTY = ENDPOINT + "EiRegisterParty"
POLL = ENDPOINT + "OadrPoll"

with open("tests/xml/vtn_distribute_event.xml", "r") as f:
    distribute_event_response_body = f.read()

with open("tests/xml/vtn_empty_poll_response.xml", "r") as f:
    empty_poll_response_body = f.read()

with open("tests/xml/ven_created_event.xml", "r") as f:
    ven_created_event = f.read()

pytestmark = pytest.mark.pony(db_session=False)


class TestEmptyPoll:
    @responses.activate
    def test_returns_no_events(self, agent):
        responses.add(
            responses.POST, POLL, body=empty_poll_response_body, content_type="text/xml"
        )
        agent.send_oadr_poll()
        _LOGGER.warning(responses.calls[:])
        assert responses.calls[0].request.url == POLL
        assert agent.active_or_pending_events == []


class TestPollWithEvent:
    @responses.activate
    def test_adds_events_to_db(self, agent):
        responses.add(
            responses.POST,
            POLL,
            content_type="text/xml",
            body=distribute_event_response_body,
        )
        responses.add(
            responses.POST, POLL, content_type="text/xml", body=empty_poll_response_body
        )
        responses.add(responses.POST, EIEVENT, content_type="text/xml")

        agent.send_oadr_poll()
        assert responses.calls[0].request.url == POLL
        assert responses.calls[1].request.url == EIEVENT
        assert responses.calls[2].request.url == EIEVENT
        assert responses.calls[3].request.url == POLL

        assert len(agent.active_or_pending_events) == 1
        assert len(agent.far_events) == 1
        assert len(agent.near_events) == 0
        assert len(agent.active_events) == 0
        assert len(agent.unresponded_events) == 0


class TestRunMainProcessesWithNoEvents:
    @responses.activate
    def test_calls_send_oadr_poll(self, agent):
        agent.send_oadr_poll = MagicMock()
        agent.tick()
        agent.send_oadr_poll.assert_called()

    @responses.activate
    def test_calls_process_event(self, agent):
        agent.process_event = MagicMock()
        agent.tick()
        agent.process_event.assert_not_called()


class TestRunMainProcessesWithEvents:
    @responses.activate
    def test_calls_send_oadr_poll(self, agent):
        responses.add(
            responses.POST,
            POLL,
            content_type="text/xml",
            body=distribute_event_response_body,
        )
        responses.add(
            responses.POST, POLL, content_type="text/xml", body=empty_poll_response_body
        )
        responses.add(responses.POST, EIEVENT, content_type="text/xml")
        agent.send_oadr_poll = MagicMock()
        agent.tick()
        agent.send_oadr_poll.assert_called()

    @responses.activate
    def test_calls_process_event(self, agent):
        responses.add(
            responses.POST,
            POLL,
            content_type="text/xml",
            body=distribute_event_response_body,
        )
        responses.add(
            responses.POST, POLL, content_type="text/xml", body=empty_poll_response_body
        )
        responses.add(responses.POST, EIEVENT, content_type="text/xml")
        agent.process_event = MagicMock()
        agent.tick()
        agent.process_event.assert_called()
