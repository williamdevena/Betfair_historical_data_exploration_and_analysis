import betfairutil

from src import betfairutil_copy, utils

FUNS_FOR_PRICE_FILE = {
    'Total volume traded': betfairutil.get_total_volume_traded_from_prices_file,
    'Pre-event volume': betfairutil.get_pre_event_volume_traded_from_prices_file
}

FUNS_FOR_MB = {
    'Total matched': betfairutil.calculate_total_matched,
    'Available volume back': betfairutil.calculate_available_volume,
    'Available volume lay': betfairutil.calculate_available_volume,
    'Publish time': lambda mb: betfairutil.publish_time_to_datetime(mb['publishTime'])
}

FUNS_FOR_RUNNERS = {
    #'Spread': betfairutil.get_spread,
    'Spread': betfairutil_copy.get_spread,
    'Mid price': betfairutil.get_mid_price,
    'OB imbalance': betfairutil.calculate_order_book_imbalance,
    'Last traded price': utils.get_last_traded_prices_from_runner
}

PARAMETERS_FOR_FUNCTIONS = {
    'Available volume back': [betfairutil.Side.BACK, 1000],
    'Available volume lay': [betfairutil.Side.LAY, 1000],
}