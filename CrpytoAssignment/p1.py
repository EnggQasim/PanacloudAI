import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def price(symbol, comparison_symbols=['USD'], exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    return data
x=[0]
y=[0]
fig = plt.gcf()
fig.show()
fig.canvas.draw()
plt.ylim([0, 20000])
i=0
while(True):
    data = price('BTC')
    i+=1
    x.append(i)
    y.append(data['USD'])
    plt.title("BTC Vs USD. Last updated at: "+str(datetime.datetime.now()))
    plt.plot(x,y)

    ax = fig.add_subplot(1,1,1) 
    fig.canvas.draw()
    

    plt.pause(1000)

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))