"""
This module contains functions that represent modifications of the functions of the betfairutil library, useful for the parsing
of Betfair price files.

It also contains additional functions useful to extract information from the price files (functions not present in the betfairutil library).
"""

import betfairutil
from betfairlightweight.resources.bettingresources import (MarketBook,
                                                           RunnerBook)


def get_runner_book_from_market_book(
    market_book,
    selection_id=None,
    runner_name=None,
    #handicap=0.0,
    return_type=None,
):
    """
    Extract a runner book from the given market book. The runner can be identified either by ID or name

    :param market_book: A market book either as an object whose class provides the mapping interface (e.g. a dict) or as a betfairlightweight MarketBook object. Alternatively can be None - if so, None will be returned
    :param selection_id: Optionally identify the runner book to extract by the runner's ID
    :param runner_name: Alternatively identify the runner book to extract by the runner's name
    :param handicap: The handicap of the desired runner book
    :param return_type: Optionally specify the return type to be either a dict or RunnerBook. If not given then the return type will reflect the type of market_book; if market_book is a dictionary then the return value is a dictionary. If market_book is a MarketBook object then the return value will be a RunnerBook object
    :returns: If market_book is None then None. Otherwise, the corresponding runner book if it can be found in the market book, otherwise None. The runner might not be found either because the given selection ID/runner name is not present in the market book or because the market book is missing some required fields such as the market definition. The type of the return value will depend on the return_type parameter
    :raises: ValueError if both selection_id and runner_name are given. Only one is required to uniquely identify the runner book
    """
    if market_book is None:
        return None

    if selection_id is not None and runner_name is not None:
        raise ValueError("Both selection_id and runner_name were given")
    if return_type is not None and not (
        return_type is dict or return_type is RunnerBook
    ):
        raise TypeError(
            f"return_type must be either dict or RunnerBook ({return_type} given)"
        )

    if isinstance(market_book, MarketBook):
        market_book = market_book._data
        return_type = return_type or RunnerBook
    else:
        return_type = return_type or dict
    if selection_id is None:
        for runner in market_book.get("marketDefinition", {}).get("runners", []):
            if runner.get("name") == runner_name:
                selection_id = runner.get("id")
                break
        if selection_id is None:
            return

    for runner in market_book.get("runners", []):
        if (
            runner.get("selectionId") == selection_id
            #and runner.get("handicap") == handicap
        ):
            return return_type(**runner)


def get_last_pre_event_market_book_id_from_prices_file(
    path_to_prices_file, filter_suspended = True):
    """
    Search a prices file for the last market book before the market turned in play
    and returns the index of this last pre-event market book.

    :param path_to_prices_file: The prices file to search
    :param filter_suspended: Optionally ignore any pre-event market books where the market status is SUSPENDED
    :return: The last pre-event market book, where the status is not SUSPENDED if filter_suspended has been set to True, provided one such market book exists in the prices file. If not then None will be returned
    """
    g = betfairutil.create_market_book_generator_from_prices_file(path_to_prices_file)
    for idx, market_book in enumerate(g):
        if market_book["inplay"]:
            return idx
        # if not filter_suspended or market_book["status"] != "SUSPENDED":
        #     pre_event_market_book = market_book



def get_last_traded_prices_from_runner(runner_book):
    last_price = runner_book.get('lastPriceTraded', 0)

    if last_price!=None:
        return last_price
    else:
        return 0



def get_name_match(price_file):
    market_books = betfairutil.read_prices_file(price_file)

    return market_books[0]['marketDefinition']['eventName']


def get_event_id(price_file):
    market_books = betfairutil.read_prices_file(price_file)

    return market_books[0]['marketDefinition']['eventId']


def get_event_date(price_file):
    market_books = betfairutil.read_prices_file(price_file)

    return market_books[0]['marketDefinition']['openDate']






if __name__=="__main__":
    path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/matches/nadal_deminaur.bz2"

    pre_event_market_book, idx = get_last_pre_event_market_book_id_from_prices_file(path)
    print(idx)