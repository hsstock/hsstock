from hsstock.common.constant import *

class FREQ:
    UNLOCK_TRADE = "unlock_trade"
    PLACE_ORDER = "place_order"
    MODIFY_ORDER = "modify_order"
    CHANGE_ORDER = "change_order"
    HISTORY_ORDER_LIST_QUERY = "history_order_list_query"
    HISTORY_DEAL_LIST_QUERY = "history_deal_list_query"
    GET_MARKET_SNAPSHOT = "get_market_snapshot"
    GET_PLATE_LIST = "get_plate_list"
    GET_PLATE_STOCK = "get_plate_stock"
    TOTAL_SECONDS = "total_seconds"


FREQLIMIT={
    FREQ.UNLOCK_TRADE:10,
    FREQ.PLACE_ORDER:30,
    FREQ.MODIFY_ORDER:30,
    FREQ.CHANGE_ORDER:30,
    FREQ.HISTORY_DEAL_LIST_QUERY:10,
    FREQ.HISTORY_ORDER_LIST_QUERY:10,
    FREQ.GET_MARKET_SNAPSHOT:10,
    FREQ.GET_PLATE_LIST:10,
    FREQ.GET_PLATE_STOCK:10,
    FREQ.TOTAL_SECONDS:30
}
