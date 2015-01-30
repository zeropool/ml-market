
class MarketMaker(object):
    """Specifies the actions each market maker should implement. """

    def order_placed(self, ord):
        """Handles placing of an order by the user. """
        raise NotImplementedError()
    
    def can_quote(self):
        raise NotImplementedError()

    def price_quote(self, ord):
        """Gets a price quote for the given order. """
        raise NotImplementedError()

    def end_challenge(self):
        raise NotImplementedError()
