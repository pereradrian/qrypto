# This is a module for download historical data from www.coinmarketcap.com
import time
import numpy as np
import pickle
import requests
from qrypto.config import URL_BASE
from typing import Optional


class CoinMarketCap:
    """Class for coinmarketcap api v3"""

    def __init__(self, cash_id: int = 2781):
        """
        Function for setting the `cash_id`.

        :param int cash_id: Cash id. e.g. id=2781 is USD and id = 2790 is EUR. Default is 2781.

        """
        self._url = URL_BASE
        self._cash_id = cash_id

    def _get_response(self, url: str) -> dict:
        """
        Internal function to handle the url's.

        :param url: The url of the current API endpoint.
        :return: The response dict.

        """
        try:
            _response = requests.get(url)
            if _response.status_code != 200:
                print(_response)
                raise
        except Exception as err_msg:
            print(err_msg)
            return {}
        else:
            return _response.json()

    def get_detail(self, currency_id: int):
        """
        Function to get details for a input currency id.

        :param currency_id:
        :return: dict

        Example::

                from qrypto import CoinMarketCap

                cmp = CoinMarketCap(cash_id=2781)
                data = cmp.get_detail(currency_id=1)

                Response:
                ```
                { 'data': { 'alertLink': '',
                            'analysisFlag': True,
                            'category': 'coin',
                            'cexVolume': 15347635273.188282,
                            'dateAdded': '2013-04-28T00:00:00.000Z',
                            'description': '## What Is Bitcoin (BTC)?\n',
                            'holdersFlag': True,
                            'id': 1,
                            'isAudited': False,
                            'latestUpdateTime': '2022-12-03T18:46:00.000Z',
                            'launchPrice': 135.3,
                            'name': 'Bitcoin',
                            'notice': '',
                            'ratingsFlag': True,
                            'slug': 'bitcoin',
                            'socialsFlag': True,
                            'statistics': { 'circulatingSupply': 19223487.0,
                                            'closeYesterday': 17088.660409402313,
                                            'fullyDilutedMarketCap': 356639126748.48,
                                            'fullyDilutedMarketCapChangePercentage24h': 0.13,
                                            'high24h': 17116.04080553255,
                                            'high30d': 21446.886096690843,
                                            'high52w': 53904.67951179671,
                                            'high7d': 17197.49725344472,
                                            'high90d': 22673.819766285604,
                                            'highAllTime': 68789.62593892214,
                                            'highAllTimeChangePercentage': -75.31,
                                            'highAllTimeTimestamp': '2021-11-10T14:17:02.000Z',
                                            'highYesterday': 17088.660409402313,
                                            'low24h': 16939.136500144697,
                                            'low30d': 15599.047175382899,
                                            'low52w': 15599.047175382899,
                                            'low7d': 16054.53021534078,
                                            'low90d': 15599.047175382899,
                                            'lowAllTime': 65.5260009765625,
                                            'lowAllTimeChangePercentage': 25817.67,
                                            'lowAllTimeTimestamp': '2013-07-05T18:56:01.000Z',
                                            'lowYesterday': 16877.88159587772,
                                            'marketCap': 326468934130.51,
                                            'marketCapChangePercentage24h': 0.1315,
                                            'marketCapDominance': 38.1796,
                                            'maxSupply': 21000000.0,
                                            'openYesterday': 16968.683261479262,
                                            'price': 16982.815559451374,
                                            'priceChangePercentage1h': 0.02347074,
                                            'priceChangePercentage24h': 0.12714502,
                                            'priceChangePercentage30d': -16.09250846,
                                            'priceChangePercentage60d': -15.32211267,
                                            'priceChangePercentage7d': 2.89214829,
                                            'priceChangePercentage90d': -14.38778882,
                                            'priceChangePercentageYesterday': 0.71,
                                            'rank': 1,
                                            'roi': 12451.97011046,
                                            'totalSupply': 19223487.0,
                                            'turnover': 0.04701198,
                                            'volumeYesterday': 19539705127.46,
                                            'ytdPriceChangePercentage': -64.3868},
                            'status': 'active',
                            'symbol': 'BTC',
                            ...

                ```

        """
        _url = f'{self._url}detail?id={currency_id}'
        return self._get_response(url=_url)

    def get_historical_data(self,
                            currency_id: int,
                            start_time: Optional[int] = None,
                            end_time: Optional[int] = None):
        """
        Function to get historical data for a currency.

        :param currency_id: Currency id
        :param start_time: start time
        :param end_time: end time
        :return: dict

        Example::

            from qrypto import CoinMarketCap

            cmp = CoinMarketCap(cash_id=2781)
            data = cmp.get_historical_data(currency_id=1)  # id = 1 is BTC

            Response:
            ```
            { 'data': { 'id': 1,
                        'name': 'Bitcoin',
                        'quotes': [ { 'quote': { 'close': 17088.6604094023,
                                                 'high': 17088.6604094023,
                                                 'low': 16877.8815958777,
                                                 'marketCap': 328491679165.28,
                                                 'open': 16968.6832614793,
                                                 'timestamp': '2022-12-02T23:59:59.999Z',
                                                 'volume': 19539705127.46},
                                      'timeClose': '2022-12-02T23:59:59.999Z',
                                      'timeHigh': '2022-12-02T23:59:00.000Z',
                                      'timeLow': '2022-12-02T14:09:00.000Z',
                                      'timeOpen': '2022-12-02T00:00:00.000Z'}],
                        'symbol': 'BTC'},
              'status': { 'credit_count': 0,
                          'elapsed': '4',
                          'error_code': '0',
                          'error_message': 'SUCCESS',
                          'timestamp': '2022-12-03T11:01:23.064Z'}}
            ```

        """
        if end_time is None:
            end_time = int(time.time())
        if start_time is None:
            start_time = end_time - 2*24*60*60

        # Create the url for historical endpoint
        _url = f'{self._url}historical?id={currency_id}&convertId={self._cash_id}'\
               f'&timeStart={start_time}&timeEnd={end_time}'

        return self._get_response(url=_url)


if __name__ == '__main__':
    from pprint import pprint

    with open('../symbols.pkl', 'rb') as file:
        symbols = pickle.load(file)

    print(symbols['USD'])  # 2781

    broker = CoinMarketCap(cash_id=symbols['USD'])
    my_data = broker.get_detail(currency_id=1)
    # my_data = broker.get_historical_data(currency_id=symbols['BTC'])
    pprint(my_data, indent=2)









