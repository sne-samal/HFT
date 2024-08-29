from order_book import OrderBook
import string
import numpy as np
from exchange import convert_to_hex
SHAPE_PARAMETER = 0.005 
# Bytes:      Bits:       reg:                                Bitreglength    Message:
#     1       0-7:        reg0[7:0]                           8               "A" for add order 
#     2       8-23:       reg0[23:8]                          16              Locate code identifying the security - a random number associated with a specific stock, new every day
#     2       24-39:      reg0[31:24] reg1[7:0]               16              Internal tracking number
#     6       40-87:      reg1[31:8] reg2[23:0]               48              Timestamp - nanoseconds since midnight - we will just do seconds since start of trading day

#     8       88-151:     reg2[31:24] reg3[31:0] reg4[23:0]   64              Order ID
#     1       152-159:    reg4[31:24]                         8               Buy or sell indicator - 0 or 1
#     4       160-191:    reg5[31:0]                          32              Number of shares / order quantity
#     8       192-255:    reg6[31:0] reg7[31:0]               64              Stock ID
#     4       255-287:    reg8[31:0]                          32              Price


def parse(ITCH_data):
        # return a list of the parsed data
        reg_0 = ITCH_data[8]
        reg_1 = ITCH_data[7]
        reg_2 = ITCH_data[6]
        reg_3 = ITCH_data[5]
        reg_4 = ITCH_data[4]
        reg_5 = ITCH_data[3]
        reg_6 = ITCH_data[2]
        reg_7 = ITCH_data[1]
        reg_8 = ITCH_data[0]

        order_book_inputs = []

        order_type = reg_0 & 0xff

        locate_code = (reg_0 >> 8) & 0xFFFF

        internal_tracking_number_half_1 = (reg_0 >> 24) & 0xFF
        internal_tracking_number_half_2 = reg_1 & 0xFF
        internal_tracking_number = (internal_tracking_number_half_1 << 8) | internal_tracking_number_half_2

        timestamp_1 = (reg_1 >> 8) & 0xFFFFFF
        timestamp_2 = (reg_2) & 0xFFFFFF
        final_time = (timestamp_1 << 25 ) | timestamp_2
        
        order_id_1 = (reg_2 >> 24) & 0xFF
        order_id_2 = reg_3
        order_id_3 = (reg_4) & 0xFFF
        order_id = (order_id_1 << 56) | (order_id_2 << 32) | order_id_3

        buy_or_sell = (reg_4 >> 24) & 0xFF

        shares = reg_5
        stock_id = (reg_6 << 32) | reg_7
        price = reg_8

        order_book_inputs.append(stock_id)
        order_book_inputs.append(order_id)
        order_book_inputs.append(buy_or_sell)
        order_book_inputs.append(shares)
        order_book_inputs.append(price)
        order_book_inputs.append(order_type)
        order_book_inputs.append(final_time)
        
        # print(order_book_inputs)

        ### TESTING    
        # # Print extracted values
        # print(f"reg_0: {bin(reg_0)}")
        # print(f"Add Order: {bin(add_order)}")
        # print(f"Locate Code: {bin(locate_code)}")
        # print("\n")

        # print(f"reg_0: {bin(reg_0)}")
        # print(f"reg_1: {bin(reg_1)}")
        # print(f"Tracking Number: {bin(internal_tracking_number_half_1)}")
        # print(f"Tracking Number: {bin(internal_tracking_number_half_2)}")
        # print(f"Final Tracking Number: {bin(internal_tracking_number)}")
        # print("\n")

        # print(f"reg_1: {bin(reg_1)}")
        # print(f"reg_2 {bin(reg_2)}")
        # print(f"Timestamp 1: {bin(timestamp_1)}")
        # print(f"Timestamp 2: {bin(timestamp_2)}")
        # print(f"Final timestamp: {bin(final_time)}")
        # print("\n")

        # print(f"reg_2 {bin(reg_2)}")
        # print(f"reg_3 {bin(reg_3)}")
        # print(f"reg_4 {bin(reg_4)}")
        # print(f"order_id_1: {bin(order_id_1)}")
        # print(f"order_id_2: {bin(order_id_2)}")
        # print(f"order_id_3: {bin(order_id_3)}")
        # print(f"order_id: {bin(order_id)}")
        # print("\n")

        # print(f"reg_4 {bin(reg_4)}")
        # print(f"Buy/Sell Indicator: {bin(buy_or_sell)}")

        # print(f"shares: {bin(reg_5)}")
        # print(f"stock_id: {bin(reg_6)} and {bin(reg_7)}")
        # print(f"shares: {bin(reg_8)}")
    
        # 0b 0000 0001 0000 0000 0000 0000 0000 0000
        
        # print(f"Timestamp: {bin(timestamp)}")
        # print(f"Order ID: {bin(order_id)}")
        # print(f"Buy/Sell Indicator: {bin(buy_sell_indicator)}")
        # print(f"Order Quantity: {bin(order_quantity)}")

class Model:

    def __init__(self):
        self.ob = OrderBook()
        self.inventory = [0, 0, 0, 0]

    
    def quote_orders(self, ITCH_data):
        # parse the order
        order_book_inputs = parse(ITCH_data)
        # TODO: not complete
        stock_id = order_book_inputs[0]
        order_id = order_book_inputs[1]
        trade_type = order_book_inputs[2]
        quantity = order_book_inputs[3]
        price = order_book_inputs[4]
        order_type = order_book_inputs[5]
        timestamp = order_book_inputs[6]    

        # load it into the order book
        if order_type.upper() == "ADD":
            self.ob.add_order(stock_id, order_id, trade_type, quantity, price)
        elif order_type.upper() == "CANCEL":
            self.order_book.cancel_order(stock_id, trade_type, order_id)
        elif order_type.upper() == "EXECUTE":
            self.order_book.execute_order(stock_id, quantity, order_id)

            # in the order book, we need to see what side the execute trade is.
            # inventory stuff - need to pass in order id too to check if the order from the exchange is one of ours that has been executed.
            trade_type = self.ob.execute_order_side
            self.update_inventory(order_id, stock_id, quantity, trade_type)
        else:
             raise ValueError("Invalid order type")

        best_bid = self.order_book.return_best_bid(stock_id)
        best_ask = self.order_book.return_best_ask(stock_id)


        # trading logic stuff
        quote_bid, quote_ask = self.calculate_bid_and_ask_prices(timestamp, best_bid, best_ask)


        # order size 
        # Order Quantity Estimation
        order_quantity = 100 * (SHAPE_PARAMETER * self.update_inventory(order_id, stock_id, quantity, trade_type)) # where do we get inventory_state from?
        
        # output orders
        if(trade_type):
            return order_quantity, quote_bid
        else:
            return order_quantity, quote_ask

    def update_buffer(self, stock_id, element):
        if 0 <= stock_id <= 3:
            self.volatility_buffer[stock_id].append(element)
        else:
            print("Index out of range. Please use an index between 0 and 3.")

    def buffer_var(self, stock_id):
        temp = self.volatility_buffer[stock_id]
        mean = np.mean(temp)
        # Calculate the variance
        variance = np.mean([(x - mean) ** 2 for x in temp])
        return variance
    
    def calculate_bid_and_ask_prices(self, timestamp, best_bid, best_ask, stock_id, inventory_state):
        # volatility + is full logic
        # zero protection logic
        # spread
        # ref price
        # maths

        # Volatility
        curr_price = (best_ask + best_bid) / 2
        self.update_buffer(stock_id, curr_price)
        volatility = self.buffer_var(stock_id)

        # Spread
        spread = 0.125 * volatility * timestamp 

        # Ref Price 
        ref_price = curr_price - (inventory_state * 0.125 * volatility * timestamp)

        # Quote Price
        quote_bid = ref_price - spread
        quote_ask = ref_price + spread

        return quote_bid, quote_ask

    
    def update_inventory(self, order_id, stock_id, quantity, order_side):
        MAX_INVENTORY_SIZE = 10000
        if(order_id >= 536870912):
            return
        else:
            if order_side.upper() == "BUY":
                multiplier = 1
            elif order_side.upper() == "SELL":
                multiplier = -1
            else:
                # didn't find the order - do nothing to inventory
                multiplier = 0

            self.inventory[stock_id] = self.inventory[stock_id] + (multiplier*quantity)/MAX_INVENTORY_SIZE

        return self.inventory[stock_id]

    