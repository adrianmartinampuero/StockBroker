
import alpaca_trade_api as tradeapi
from flask import Flask, render_template, request
from werkzeug.utils import redirect


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods={'POST'})
def getvalue():
    sim_empresa = request.form['simboloempresa']
    num_acciones = request.form['numeroacciones']
    lim_operacion = request.form['limiteoperacion']
    print('El simbolo de la empresa es', sim_empresa)
    print('El numero de acciones es', num_acciones)
    print('El limite de la operacion es', lim_operacion)

    # INITIAL ALPACA CONNECTION TEST
    # Alpaca API lib must be installed on Terminal window: pip3 install alpaca-trade-api
    alpaca_endpoint = 'https://paper-api.alpaca.markets'
    api = tradeapi.REST('PKN0R0DM1Q0Q91HI5EMI','ZytjvMeu8rlWlKkZQmF55pDYKpuqebKzKqQXA7tJ', alpaca_endpoint)
    account = api.get_account()
    print('Your Alpaca connection is', account.status)
            # For the trading during this assignment we will follow the Martingale strategy

    class Martingale(object):
                def __init__(self):
                    self.key = 'PKN0R0DM1Q0Q91HI5EMI'
                    self.secretkey = 'ZytjvMeu8rlWlKkZQmF55pDYKpuqebKzKqQXA7tJ'
                    self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
                    self.api = tradeapi.REST(self.key, self.secretkey, self.alpaca_endpoint)
                    self.symbol = sim_empresa                  # Share symbol we want to study                                                         
                    self.current_order = None                   # Means that when the variable is not "None", we have an open order
                    self.last_price = int(lim_operacion)             # Last closing price == Limit BUY Alpaca
                

                # Here we define our position (reminder: Finance position = Amount of what we own in our portfolio)

                    try:
                        self.position = int(self.api.get_position(self.symbol).qty)
                    except:
                        self.position = 0


                # The function submit_order will be the one in charge of sending the orders to Alpaca

                def submit_order(self, target):
                    # In order to simplify the bot we are gonna trade with one share at a time
                    if self.current_order is not None:
                        self.api.cancel_order(self.current_order.id)

                    # Delta compares the change of price of an asset with the corresponding change of price of an option
                    # Usually Delta e [1,-1]        
                    delta = target - self.position
                    if delta == 0:
                        return
                    print(f'Processing the order for {target} shares')

                    # If DELTA is bigger than 0, we want to buy
                    if delta > 0:
                        buy_quantity = delta
                        if self.position < 0:
                            buy_quantity = min(abs(self.position), buy_quantity)
                        print(f'Buying {buy_quantity} shares')
                        self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)

                    # If DELTA is less than 0 we want to sell
                    elif delta < 0:
                        sell_quantity = abs(delta)
                        if self.position > 0:
                            sell_quantity = min(abs(self.position), sell_quantity)
                        print(f'Selling {sell_quantity} shares') 
                        self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)


            # Wat the conditional if __name__ == '__main__' basically does is differentiate if the script is the main one or it is an import
            # The variable __name__ is assigned by the compiler with __main__ if it is the executed file or with the name of the module or package if it is a file that is imported

    go_trading = Martingale()
    go_trading.submit_order(int(num_acciones))      

    return redirect("https://app.alpaca.markets/login", code=302)
 

if __name__ == '__main__':
    app.run(debug=True)
      


