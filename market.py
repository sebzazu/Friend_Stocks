import pygame
import os
import time

pygame.init()

num_trades = 0

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)

FPS = 30


class Ticker:
    def __init__(self, code, price):
        self.code = code
        self.price = price


class Trader:
    def __init__(self, ticker, money, portfolio=None):
        self.money = money
        self.portfolio = portfolio
        self.ticker = ticker

    def buy(self):
        prop_buy = input("Enter ticker, and price separated by commas: ").replace(" ", '')

        pb_elems = prop_buy.split(',')
        pb_tick = pb_elems[0]

        pb_price = float(pb_elems[1])

        prop_buy = [pb_tick, pb_price, self.ticker]
        # Returns proposed buy that will be added to proposed buys list
        # During game loop this list will be checked against proposed sells
        return prop_buy

    def sell(self):
        prop_sell = input("Enter ticker, and price separated by commas: ").replace(" ", '')

        ps_elems = prop_sell.split(',')
        ps_tick = ps_elems[0]
        # ps_num = int(ps_elems[1])
        ps_price = float(ps_elems[1])

        prop_sell = [ps_tick, ps_price, self.ticker]
        # Returns proposed sell that will be added to proposed sells list
        # During game loop this list will be checked against proposed buys
        return prop_sell

    def value_portfolio(self):
        portfolio_val = 0
        for stock in self.portfolio:
            portfolio_val += stock.price

        return portfolio_val


def main():
    open_buys = []
    open_sales = []
    closed_trades = {}
    tickers = []
    traders = {}
    num_trades = 0
    market_open = False
    clock = pygame.time.Clock()

    main_font = pygame.font.SysFont('sfnsmono', 30)

    def create_market():  # Creates trader and ticker objects
        create_traders = input("Pass list of trader tickers separated by commas").replace(" ", '')

        trader_names = create_traders.split(",")

        for trader_name in trader_names:
            # appends traders to dictionary where key is Ticker value
            traders[trader_name] = Trader(trader_name, len(trader_names) * 100, [])

            # Creates list of ticker objects, assigns each ticker to variable which is uppercase ticker
            ticker = Ticker(trader_name, 1)
            tickers.append(ticker)

        for trader in trader_names:
            for trader2 in trader_names:
                i = 0
                while i < 10:
                    traders[trader].portfolio.append(trader2)
                    i += 1

    def close_trade(num_trades):  # Checks open_buys against open_sells and matches trades to each other
        for buy in open_buys:
            for sale in open_sales:
                '''
                   buy and sale are lists containing [ticker, price, trader]. checks if tickers are same and then if 
                   proposed buying price is greater than or equal to a proposed selling price. If prices are different
                   trade will be executed at the average of the two proposed prices. Will only check the oldest standing open sale
                   that fits a proposed buy's criteria, not the most favorable option for buyer.
                                                                                                                                 '''
                if buy[0] == sale[0] and buy[1] >= sale[1]:
                    close_price = (buy[1] + sale[1]) / 2.0
                    closed_trade = [buy[0], close_price]
                    # Adds value to seller "money", removes from buyer "money"
                    for trader in traders:
                        if trader == buy[2]:
                            traders[trader].money -= close_price
                        if trader == sale[2]:
                            traders[trader].money += close_price

                    # Adjusts ticker price to last sale value
                    for ticker in tickers:
                        if ticker.code == buy[0]:
                            print(ticker.price)
                            ticker.price = close_price

                    num_trades += 1

                    open_sales.remove(sale)
                    open_buys.remove(buy)
                    # Adds closed trade list [ticker, price] to closed trade dict.
                    closed_trades[num_trades] = closed_trade
                    print(closed_trades)
                    print(close_price)


    def draw_window():  # creates pygame window

        WIN.fill(BLACK)
        # value for ticker label placement
        ticker_label_x = 20

        for ticker in tickers:
            # Draw ticker code ie APPL
            ticker_label = main_font.render(ticker.code, 1, (0, 255, 0))
            WIN.blit(ticker_label, (ticker_label_x, 20))

            # Draw ticker price below code
            ticker_price_label = main_font.render(str(ticker.price), 1, (0, 255, 0))
            WIN.blit(ticker_price_label, (ticker_label_x, 50))

            ticker_label_x += 100

        pygame.display.update()

    # Opens Market, initializes tickers and players
    create_market()
    market_open = True

    while market_open:
        clock.tick(FPS)
        draw_window()
        close_trade()
        # Initializes key object
        key = pygame.key.get_pressed()

        # Trade button logic
        if key[pygame.K_t]:
            valid_trader = False
            # while loop to validate traders existence
            while valid_trader == False:
                active_trader = input("Who would like to trade: ")

                if active_trader in traders:
                    active_trader_action = input("Would you like to buy or sell(b/s)")

                    if active_trader_action == 'b':
                        prop_buy = traders[active_trader].buy()
                        # appends buy method return value to open_buys list, Return type: list[Ticker, price, trader]
                        open_buys.append(prop_buy)
                        valid_trader = True

                    elif active_trader_action == 's':
                        prop_sale = traders[active_trader].sell()
                        # appends sell method return value to open_sales list, Return type: list[Ticker, price, trader]
                        open_sales.append(prop_sale)
                        valid_trader = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                market_open = False


if __name__ == "__main__":
    main()
