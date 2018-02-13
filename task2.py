import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

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
    mask = (df['timestamp'] >= '2018-01-01') & (df['timestamp'] <= '2018-01-31')
    df = df.loc[mask]

    #calculate the return
    y_train=(df['close']-df['open'])*100/(df['open'])


    df = pd.read_csv('index.csv')
    mask = (df['Date'] >= '2018-01-01') & (df['Date'] <= '2018-01-31')
    df = df.loc[mask]
    x_train = df['Close']
    #print((x_train))
    #print(y_train)
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
    print("Beta = ",w_val1)
    sess.close()
    plt.scatter(x_train, y_train)
    y_learned = x_train*w_val1+w_val2
    plt.plot(x_train, y_learned, 'r')
    plt.show()


def regressStatsModel(x_train,y_train):
    import statsmodels.api as sm
    model = sm.OLS(y_train, x_train)
    results = model.fit()
    print(results.params)


def regressSKLearn(x_train,y_train):
    from sklearn import datasets, linear_model
    from sklearn.metrics import mean_squared_error, r2_score

    regr = linear_model.LinearRegression()

    # Train the model using the training sets

    regr.fit(x_train.reshape(-1,1),y_train.reshape(-1,1))
    print('Coefficients: \n', regr.coef_)



regress_tensorflow(*load_data())
