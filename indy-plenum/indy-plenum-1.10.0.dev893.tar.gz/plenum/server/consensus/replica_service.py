from typing import List

from plenum.server.consensus.message_request.message_req_3pc_service import MessageReq3pcService
from plenum.server.consensus.ordering_service_msg_validator import OrderingServiceMsgValidator
from plenum.server.replica_freshness_checker import FreshnessChecker

from crypto.bls.bls_bft_replica import BlsBftReplica
from plenum.common.config_util import getConfig
from plenum.common.event_bus import InternalBus, ExternalBus
from plenum.common.messages.node_messages import Checkpoint
from plenum.common.stashing_router import StashingRouter
from plenum.common.timer import TimerService
from plenum.server.consensus.checkpoint_service import CheckpointService
from plenum.server.consensus.consensus_shared_data import ConsensusSharedData
from plenum.server.consensus.ordering_service import OrderingService
from plenum.server.consensus.view_change_service import ViewChangeService
from plenum.server.request_managers.write_request_manager import WriteRequestManager


class ReplicaService:
    """
    This is a wrapper consensus-related services. Now it is intended mostly for
    simulation tests, however in future it can replace actual Replica in plenum.
    """

    def __init__(self, name: str, validators: List[str], primary_name: str,
                 timer: TimerService, bus: InternalBus, network: ExternalBus,
                 write_manager: WriteRequestManager,
                 bls_bft_replica: BlsBftReplica=None):
        self._data = ConsensusSharedData(name, validators, 0)
        self._data.primary_name = primary_name
        config = getConfig()
        stasher = StashingRouter(config.REPLICA_STASH_LIMIT, buses=[bus, network])
        self._orderer = OrderingService(data=self._data,
                                        timer=timer,
                                        bus=bus,
                                        network=network,
                                        write_manager=write_manager,
                                        bls_bft_replica=bls_bft_replica,
                                        freshness_checker=FreshnessChecker(
                                            freshness_timeout=config.STATE_FRESHNESS_UPDATE_INTERVAL),
                                        stasher=stasher)
        self._orderer._validator = OrderingServiceMsgValidator(self._orderer._data)
        self._checkpointer = CheckpointService(self._data, bus, network, stasher,
                                               write_manager.database_manager)
        self._view_changer = ViewChangeService(self._data, timer, bus, network, stasher)
        self._message_requestor = MessageReq3pcService(self._data, bus, network)

        # TODO: This is just for testing purposes only
        self._data.checkpoints.append(
            Checkpoint(instId=0, viewNo=0, seqNoStart=0, seqNoEnd=0,
                       digest='4F7BsTMVPKFshM1MwLf6y23cid6fL3xMpazVoF9krzUw'))
