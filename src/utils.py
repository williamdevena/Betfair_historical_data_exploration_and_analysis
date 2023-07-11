import betfairutil


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
    pre_event_market_book = None
    for idx, market_book in enumerate(g):
        if market_book["inplay"]:
            return pre_event_market_book, idx
        if not filter_suspended or market_book["status"] != "SUSPENDED":
            pre_event_market_book = market_book


if __name__=="__main__":
    path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/matches/nadal_deminaur.bz2"

    pre_event_market_book, idx = get_last_pre_event_market_book_id_from_prices_file(path)
    print(idx)