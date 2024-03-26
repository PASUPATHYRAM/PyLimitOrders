from unittest import TestCase
from unittest.mock import Mock,patch
from limit.limit_order_agent import LimitOrderAgent
from collections import deque

class LimitOrderAgentTest(TestCase):

    def setUp(self):
        self.execution_client=Mock()
        self.tester=LimitOrderAgent(self.execution_client)

    def test_add_orders(self):

        #ord_typ: str, ord_price: float, p_id: str,amount: float
        self.tester.add_order('BUY',100,'IBM',1000)
        self.assertEqual(len(self.tester.orders),1)
    @patch('limit.limit_order_agent.random.uniform',return_value=100)
    def test_price_tik(self,mock_random):
        product_id,limit_price=self.tester.on_price_tick('IBM',99)
        self.assertEqual(product_id,"IBM")
        self.assertEqual(limit_price, 100)
    @patch('limit.limit_order_agent.LimitOrderAgent')
    def test_buy_orders(self,mock_price):
        m=Mock(spec=deque)
        m.append(("IBM",1000,100,'BUY'))
        mock_price.on_price_tick.return_value="IBM",100
        mock_price.add_order.return_value=m
        mock_price.execution_client.buy.return_value='test'
        self.tester.buy_orders('IBM',100)








