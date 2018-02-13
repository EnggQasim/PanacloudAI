from flask import Flask, render_template, url_for, request, session
import numpy as np
import requests
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import tensorflow as tf

app = Flask(__name__)
'''
Create price function for task1
'''
def price(symbol, comparison_symbols=['USD'], exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    print(url)
    return data

# Task2 function
def daily_price_historical(symbol, comparison_symbol, all_data=True, limit=1, aggregate=1, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df
def plotChart(axis,df,symbol,comparison_symbol):
    axis.plot(df.timestamp, df.close)
    axis.set_title(symbol + ' Vs ' + comparison_symbol)
    axis.set_ylabel('Price In ' + comparison_symbol)
    axis.set_xlabel('Year')

@app.route("/", methods=['GET','POST'])
def index():
    if request.method=="POST" and request.form['checker']=='BTC':
        session['btcCon']=request.form['btcCon']
    else:
        session['btcCon']='USD'
    
    if request.method=="POST" and request.form['checker']=='ETH':
        session['ethCon']=request.form['ethCon']
    else:
        session['ethCon']='USD'

    df1 = daily_price_historical('BTC',session['btcCon'])
    df2 = daily_price_historical('ETH',session['ethCon'])
    f, axarr = plt.subplots(2)
    plotChart(axarr[0],df1,'BTC',session['btcCon'])
    plotChart(axarr[1],df1,'ETH',session['ethCon'])
    plt.subplots_adjust(hspace=0.5)
    plt.savefig('static/abc.png')
    
    session['btcPrice']=price('BTC',[session['btcCon']])
    session['ethPrice']=price('ETH',[session['ethCon']])
    
    return render_template('index.html')
#for ajax Request
@app.route('/prices', methods=["POST","GET"])
def prices():
    if request.method=="POST" and request.form['checker']=='BTC':
        session['btcCon']=request.form['btcCon']
    else:
        session['btcCon']='USD'
    
    if request.method=="POST" and request.form['checker']=='ETH':
        session['ethCon']=request.form['ethCon']
    else:
        session['ethCon']='USD'

    btcPrice=price('BTC',[session['btcCon']])
    ethPrice=price('ETH',[session['ethCon']])
    return render_template('priceForm.html')

@app.route('/update/<iname>', methods=["POST","GET"])
def uimage(iname):
    return '<div id="img"><img src="'+url_for('static',filename=iname+'.png')+'"></div>'
# Task2 Regression With TensorFlow


def daily_price_historical(symbol, comparison_symbol, all_data=True, limit=1, aggregate=1, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


def load_data():
    #Get daily price data for January only
    df = daily_price_historical('BTC','USD')
    mask = (df['timestamp'] >= '2017-01-01') & (df['timestamp'] <= '2018-01-31')
    df = df.loc[mask]

    #calculate the return
    y_train=(df['close']-df['open'])*100/(df['open'])
    # load data from local csv file
    df = pd.read_csv('index.csv')
    mask = (df['Date'] >= '2017-01-01') & (df['Date'] <= '2018-01-31')
    df = df.loc[mask]
    x_train = (df['Close']-df['Open'])*100/(df['Open'])
    return x_train,y_train




def model(X, w1,w2):
    return tf.add(tf.multiply(X, w1),w2)

def regress_tensorflow(x_train,y_train):
    learning_rate = 0.000001
    training_epochs = 1000
    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)


    w1 = tf.Variable(0.0, name="weight1")
    w2 = tf.Variable(0.0, name="weight2")

    y_model = model(X, w1,w2)

    cost = tf.square(Y-y_model)
    train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    for epoch in range(training_epochs):
        for (x, y) in zip(x_train, y_train):
            sess.run(train_op, feed_dict={X: x, Y: y})

    w_val1 = sess.run(w1)
    w_val2 = sess.run(w2)
  
    sess.close()
    plt.scatter(x_train, y_train)
    y_learned = x_train*w_val1+w_val2
    plt.plot(x_train, y_learned, 'r')
    plt.title("Beta ="+str(w_val1))
    plt.savefig('static/regression.png')
    











@app.route("/Regression", methods=['POST','GET'])
def reg():
    d=datetime.datetime.now()
    #start=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
    #regress_tensorflow(*load_data())
    e=datetime.datetime.now()#endDate
    ed=d.day # end day
    em=d.month # end month
    ey=d.year # end year
    sdate=datetime.date(ey,em-1,ed) # same data last month
    edate=datetime.date.isoformat(e) # EndDate final ISO format Y-m-d
    start=datetime.date.isoformat(d) # StartDate ISO format Y-m-d
    session['start']=sdate
    session['end']=edate
    if request.method=="POST":
        session['start']=request.form['start']
        session['end']=request.form['end']
    regress_tensorflow(*load_data())
    return render_template('reg.html', start= session['start'], end=session['end'])


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.run(debug=True)
