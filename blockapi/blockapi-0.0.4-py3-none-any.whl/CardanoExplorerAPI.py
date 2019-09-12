import pytz
from datetime import datetime
from .services import BlockchainAPI,set_default_args_values,APIError,AddressNotExist,BadGateway,GatewayTimeOut

class CardanoExplorerAPI(BlockchainAPI):
    """
    Cardano
    API docs: https://cardanodocs.com/technical/explorer/api/
    Explorer: https://cardanoexplorer.com
    """

    currency_id = 'cardano'
    base_url = 'https://cardanoexplorer.com/api'
    rate_limit = 0
    coef = 1e-6

    supported_requests = {
        'get_summary': '/addresses/summary/{address}'
    }

    def get_balance(self):
        summary = self._get_summary()
        return int(summary['Right']['caBalance']['getCoin']) * self.coef

    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        summary = self._get_summary()
        txs = summary['Right']['caTxList']
        return [self.parse_tx(t) for t in txs]

    def parse_tx(self, tx):
        my_input = next((i for i in tx['ctbInputs']
            if i[0].lower() == self.address.lower()), None)

        my_output = next((i for i in tx['ctbOutputs']
            if i[0].lower() == self.address.lower()), None)

        fee = None

        if my_input:
            fee = (int(tx['ctbInputSum']['getCoin'])
                - int(tx['ctbOutputSum']['getCoin']))

            to_address = (tx['ctbInputs'][0][0]
                if len(tx['ctbInputs']) else None)
            from_address = self.address
            amount = int(my_input[1]['getCoin']) * self.coef

        elif my_output:
            from_address = (tx['ctbOutputs'][0][0]
                if len(tx['ctbOutputs']) else None)
            to_address = self.address
            amount = int(my_output[1]['getCoin']) * self.coef

        return {
            'date': datetime.fromtimestamp(tx['ctbTimeIssued'], pytz.utc),
            'from_address': from_address,
            'to_address': to_address,
            'amount': amount,
            'fee': fee,
            'gas': {},
            'hash': tx['ctbId'],
            'confirmed': None,
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': 'outgoing' if my_input else 'incoming',
            'raw': tx
        }

    def _get_summary(self):
        summary = self.request('get_summary', address=self.address)
        if summary.get('Left'):
            self._process_error(summary['Left'])
            return None

        return summary

    def _process_error(self, msg):
        if msg == 'Invalid Cardano address!':
            raise AddressNotExist()
        else:
            raise APIError(msg)
