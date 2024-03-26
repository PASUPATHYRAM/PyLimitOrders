from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener
from collections import deque
import random


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client=execution_client
        self.orders=deque()

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        limit_price=round(random.uniform(price*.95,price*1.1),2)
        return product_id,limit_price

    def add_order(self,flag:str, product_id: str, amount: int, limit: int ):
        '''
        It accepts the flag, product_id amount, limit
        '''
        if flag not in ['BUY','SELL']:
            raise Exception("Flag should be either BUY or SELL")
        self.orders.append((product_id, amount, limit, flag))

    def buy_orders(self,product_id,price):
        product_id,current_price=self.on_price_tick(product_id=product_id,price=price)
        if len(self.orders)>0:
            for order in self.orders:
                if order[-1]=='BUY' and float(order[2])<=current_price:
                    self.execution_client.buy(order[0],order[1])
                elif order[-1]=='SELL' and order[2]>=current_price: # implementing sell
                    self.execution_client.sell(order[0], order[1])
                else:
                    print(" Current price is greater/lesser than provided limit")

    def buy_dummy(self,amount=1000,limit=100,pro_id='IBM',f='BUY'):
        shares=amount//limit
        temp_amount=amount
        for i in range(shares):
            self.add_order(flag=f,product_id=pro_id,amount=temp_amount,limit=limit)
            temp_amount=temp_amount-limit
        self.buy_orders(product_id=pro_id,price=amount)
























