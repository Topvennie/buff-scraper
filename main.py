import threading
from datetime import timedelta
from time import sleep, time
from typing import Any

import mysql.connector.errors

import config
from buffParser import *
from database import Database


def validate(validation: bool, error_text: str) -> bool:
    if not validation:
        print(error_text)
    return validation


def check_positive_int(number: Any) -> bool:
    return type(number) == int and number >= 0


def start_class(start, end):
    BuffAPIParser(start, end).start_parsing()


if __name__ == '__main__':
    start_time = time()

    # Check if connection to database works
    try:
        with Database(config.DATABASE_USER, config.DATABASE_PASSWORD, config.DATABASE_HOST, config.DATABASE) as db:
            connection_succes = True
    except mysql.connector.errors.InterfaceError:
        connection_succes = False
        print('Unable to connect to the database!')
        print('Make sure the config file is right')
        print('Aborting script...')
        sleep(5)

    # Basic config validation
    if config.USE_URL_METHOD:
        config_succes = validate(
            check_positive_int(config.START_PAGE),
            'START_PAGE has to be a positive integer!'
        )
    else:
        config_succes = validate(
            check_positive_int(config.START_CODE),
            'START_CODE has to be a positive integer!'
        )
        # Only check config.END_CODE > config.START_CODE if both values or integers
        config_succes = config_succes and validate(
            check_positive_int(config.END_CODE) and config.END_CODE > config.START_CODE,
            'END_CODE has to be a positive integer and larger than START_CODE!'
        )
        if config.ENABLE_THREADS:
            config_succes = config_succes and validate(
                check_positive_int(config.AMOUNT_OF_THREADS),
                'AMOUNT_OF_THREADS has to be a positive integer!'
            )

    if connection_succes and config_succes:
        if config.USE_URL_METHOD:
            print('Using the URL method')
            BuffURLParser().start()
        else:
            print('Using the code method')
            if config.ENABLE_THREADS:
                threads = []
                amount_of_threads = config.AMOUNT_OF_THREADS

                print('THREADS ENABLED')
                print(f'Using {amount_of_threads} thread{"s" if config.AMOUNT_OF_THREADS > 1 else ""}')

                for i in range(0, amount_of_threads):
                    # Split the code range up in equal parts
                    start_code = ((config.END_CODE - config.START_CODE) // amount_of_threads) * i + config.START_CODE
                    end_code = ((config.END_CODE - config.START_CODE) // amount_of_threads) * (i + 1) + config.START_CODE
                    if i == amount_of_threads - 1:
                        end_code = config.END_CODE
                    threads.append(threading.Thread(target=start_class, args=(start_code, end_code)))

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()
            else:
                print('THREADS DISABLED')
                BuffAPIParser(config.START_CODE, config.END_CODE).start_parsing()

        end_time = time()
        running_time = str(timedelta(seconds=end_time - start_time))
        print(f'Total execution time: {running_time}')
