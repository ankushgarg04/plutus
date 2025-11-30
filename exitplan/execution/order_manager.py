import time
from config import TRADING_PARAMS
from utils.logger import setup_logger

logger = setup_logger("order_manager")

class OrderManager:
    def __init__(self, api):
        self.api = api
        self.exchange = TRADING_PARAMS['exchange']
        self.product_type = TRADING_PARAMS['product_type']
        self.order_type = TRADING_PARAMS['order_type']
        self.max_qty = TRADING_PARAMS['max_quantity']
        self.current_qty = 0 # Track current position (simplified)

    def place_buy_order(self, symbol, quantity, price=0):
        """
        Place a BUY order with safety checks.
        """
        if quantity <= 0:
            logger.error(f"Invalid quantity: {quantity}")
            return None

        if self.current_qty + quantity > self.max_qty:
            logger.warning(f"Order rejected: Max quantity limit reached ({self.max_qty})")
            return None

        logger.info(f"Placing BUY order for {quantity} {symbol} at {price if price > 0 else 'MKT'}")
        
        try:
            # Note: In a real scenario, you'd map order_type to API constants
            # Assuming 'MKT' maps to 'MKT' string expected by API
            ret = self.api.place_order(
                buy_or_sell='B', 
                product_type=self.product_type,
                exchange=self.exchange, 
                tradingsymbol=symbol, 
                quantity=quantity, 
                discloseqty=0,
                price_type=self.order_type, 
                price=price,
                trigger_price=None,
                retention='DAY', 
                remarks='AlgoTrade'
            )
            
            if ret and ret.get('stat') == 'Ok':
                order_id = ret.get('norenordno')
                logger.info(f"BUY Order placed successfully. Order ID: {order_id}")
                self.current_qty += quantity
                return order_id
            else:
                logger.error(f"BUY Order failed: {ret.get('emsg')}")
                return None
                
        except Exception as e:
            logger.error(f"Exception placing BUY order: {e}")
            return None

    def place_sell_order(self, symbol, quantity, price=0):
        """
        Place a SELL order with safety checks.
        """
        if quantity <= 0:
            logger.error(f"Invalid quantity: {quantity}")
            return None

        # For simplicity, allowing short selling (negative qty)
        # But warning if selling more than held (if long only strategy)
        
        logger.info(f"Placing SELL order for {quantity} {symbol} at {price if price > 0 else 'MKT'}")
        
        try:
            ret = self.api.place_order(
                buy_or_sell='S', 
                product_type=self.product_type,
                exchange=self.exchange, 
                tradingsymbol=symbol, 
                quantity=quantity, 
                discloseqty=0,
                price_type=self.order_type, 
                price=price,
                trigger_price=None,
                retention='DAY', 
                remarks='AlgoTrade'
            )
            
            if ret and ret.get('stat') == 'Ok':
                order_id = ret.get('norenordno')
                logger.info(f"SELL Order placed successfully. Order ID: {order_id}")
                self.current_qty -= quantity
                return order_id
            else:
                logger.error(f"SELL Order failed: {ret.get('emsg')}")
                return None
                
        except Exception as e:
            logger.error(f"Exception placing SELL order: {e}")
            return None
