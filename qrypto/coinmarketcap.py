# This is a module for download historical data from www.coinmarketcap.com
import time
import pandas as pd
import pickle
import requests
from qrypto.config import URL_BASE
from qrypto.tools import date_to_seconds
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
                            start_time: Optional[str] = None,
                            end_time: Optional[str] = None):
        """
        Function to get historical data for a currency.

        :param currency_id: Currency id
        :param start_time: start time
        :param end_time: end time
        :return: dict

        Example::

            from qrypto import CoinMarketCap

            cmp = CoinMarketCap(cash_id=2781)
            data = cmp.get_historical_data(currency_id=1,             # id = 1 is BTC
                                           start_time='2022-12-01',
                                           end_time='2022-12-03')

            Response:
            ```
                                open          high           low         close        volume     marketCap symbol
            date
            2022-12-01  17168.002138  17197.497253  16888.387888  16967.133667  2.289539e+10  3.261421e+11    BTC
            2022-12-02  16968.683261  17088.660409  16877.881596  17088.660409  1.953971e+10  3.284917e+11    BTC
            2022-12-03  17090.098485  17116.040806  16888.140807  16908.236795  1.621778e+10  3.250372e+11    BTC
            ```

        """

        if not(end_time is None):
            end_time = date_to_seconds(end_time)
        else:
            end_time = int(time.time())

        if not(start_time is None):
            start_time = date_to_seconds(start_time)
        else:
            start_time = end_time - 2 * 24 * 60 * 60

        # Create the url for historical endpoint
        _url = f'{self._url}historical?id={currency_id}&convertId={self._cash_id}'\
               f'&timeStart={start_time}&timeEnd={end_time}'

        return self._dict_to_dataframe(self._get_response(url=_url))

    def _dict_to_dataframe(self, x: dict):
        """Function to parse historical data from json to dataframe."""
        if len(x) > 0:
            _df_ = pd.DataFrame([a['quote'] for a in x['data']['quotes']])
            _df_['timestamp'] = pd.to_datetime(_df_['timestamp'].apply(lambda x: str(x).split('T')[0]))
            _df_['symbol'] = x['data']['symbol']
            return _df_.rename(columns={'timestamp': 'date'}).set_index('date')
        else:
            return None


if __name__ == '__main__':
    from pprint import pprint

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    with open('../symbols.pkl', 'rb') as file:
        symbols = pickle.load(file)

    print(symbols['USD'])  # 2781

    broker = CoinMarketCap(cash_id=symbols['USD'])
    # my_data = broker.get_detail(currency_id=1)
    # pprint(my_data, indent=2)

    df = broker.get_historical_data(currency_id=symbols['BTC'], start_time='2022-12-01',
                                    end_time='2022-12-03')
    print(df)





