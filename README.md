# qrypto

Package to download data from CoinMarketCap.

## Getting started 

Install the package with the following code.
````
pip install git+https://github.com/pereradrian/qrypto.git
````

**Example of code**

The following code set cash as 'USD' with the `cash_id` = 2781, 
and then download three days of historical data for Bitcoin (BTC).
The `currency_id` = 1 is for Bitcoin.

````python
from qrypto import CoinMarketCap

cmp = CoinMarketCap(cash_id=2781)
df = cmp.get_historical_data(currency_id=1,
                             start_time='2022-12-01',
                             end_time='2022-12-03')
````

Result:

````
                    open          high           low         close        volume     marketCap symbol
date                                                                                                 
2022-12-01  17168.002138  17197.497253  16888.387888  16967.133667  2.289539e+10  3.261421e+11    BTC
2022-12-02  16968.683261  17088.660409  16877.881596  17088.660409  1.953971e+10  3.284917e+11    BTC
2022-12-03  17090.098485  17116.040806  16888.140807  16908.236795  1.621778e+10  3.250372e+11    BTC
````