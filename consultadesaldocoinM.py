import logging
from time import sleep
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
import pandas as pd
import msvcrt


config_logging(logging, logging.DEBUG)
um_futures_client = UMFutures(key='ACAVATUKEY', secret='ACAVATUSECRETKEY')
try:

    balance = um_futures_client.balance(recvWindow=6000)

    df = pd.DataFrame(balance) 
    print(df[["asset" , "balance"]])
    sleep(10)
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )

print("[+] Pulsar cualquier tecla para salir...")
msvcrt.getch()
