from unittest import TestCase, main
import ssc2ce_cpp as m


class DeribitParser(TestCase):
    def setUp(self):
        self.parser = m.DeribitParser()
        self.book = self.parser.get_book("ETH-PERPETUAL")
        self.top_bid = 0
        self.top_ask = 0
        self.book_setup_count = 0
        self.parser.set_on_book_setup(self.handle_book_setup)
        self.book_update_count = 0
        self.parser.set_on_book_update(self.handle_book_update)

    def handle_book_setup(self, book):
        self.top_bid = book.top_bid_price()
        self.top_ask = book.top_ask_price()
        self.book_setup_count += 1

    def handle_book_update(self, book):
        self.top_bid = book.top_bid_price()
        self.top_ask = book.top_ask_price()
        self.book_update_count += 1

    def test_snapshot(self):
        book_snapshot = '{"jsonrpc":"2.0","method":"subscription","params":{"channel":"book.ETH-PERPETUAL.raw",' \
            '"data":{"timestamp":1592049683328,"instrument_name":"ETH-PERPETUAL","change_id":600242265,' \
            '"bids":[["new",235.3,26441.0],["new",235.25,5882.0],["new",235.2,15126.0]],' \
            '"asks":[["new",235.4,2120.0],["new",235.45,15892.0],["new",235.5,34249.0]]}}}'

        self.assertEqual(self.parser.parse(book_snapshot), True)
        self.assertEqual(self.book.top_bid_price(), 235.3)
        self.assertEqual(self.book.top_ask_price(), 235.4)
        self.assertEqual(self.top_bid, 235.3)
        self.assertEqual(self.top_ask, 235.4)
        self.assertEqual(self.book_setup_count, 1)
        self.assertEqual(self.book_update_count, 0)

    def test_update(self):
        book_snapshot = '{"jsonrpc":"2.0","method":"subscription","params":{"channel":"book.ETH-PERPETUAL.raw",' \
            '"data":{"timestamp":1592049683328,"instrument_name":"ETH-PERPETUAL","change_id":600242265,' \
            '"bids":[["new",235.3,26441.0],["new",235.25,5882.0],["new",235.2,15126.0]],' \
            '"asks":[["new",235.4,2120.0],["new",235.45,15892.0],["new",235.5,34249.0]]}}}'

        self.assertEqual(self.parser.parse(book_snapshot), True)

        book_update = '{"jsonrpc":"2.0","method":"subscription","params":{"channel":"book.ETH-PERPETUAL.raw",' \
            '"data":{"timestamp":1592049685338,"prev_change_id":600242265,"instrument_name":"ETH-PERPETUAL","change_id":600242267,' \
            '"bids":[["new",235.4,111.0]],"asks":[["delete",235.4],["new",235.46,236066.0]]}}}'

        self.assertEqual(self.parser.parse(book_update), True)
        self.assertEqual(self.top_bid, 235.4)
        self.assertEqual(self.top_ask, 235.45)
        self.assertEqual(self.book_setup_count, 1)
        self.assertEqual(self.book_update_count, 1)


if __name__ == '__main__':
    main()
