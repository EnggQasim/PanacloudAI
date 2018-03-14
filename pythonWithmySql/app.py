from flask import Flask, render_template
from flaskext.mysql import MySQL
import ccxt
import pyodbc
import pandas as pd


app = Flask(__name__)

#Congifgration with mysql
'''
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)'''


#Connect with SQL server
con = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=demo1;Trusted_Connection=yes;')
'''
sir g there is method to connect with pyodbc it working :)
'''
# Get Data From cctx API
bitfinex   = ccxt.bitfinex({
    'apiKey': 'hdPHGGOYKaKAR2BDWF7l4J6YJCBYrJGi9H8YJYfht4A ',
    'secret': 'Pc7cKpsoohDXF8EAx3VjkoWE8NJPAjwvVPSVRDXVnrn',
});
kraken = ccxt.kraken({
    'apikey': 'HE4JSPoApgKjeGEkFfp9BdC1oB8y8TZJGyyy/8EWAzyjUIX60Bvz3xkO',
    'secret': '5C+arBvOogTCDoKhcTYUPK8BBPy67D/hq5tgkkdao7oAJXvIjCdwbpCJr3fAUfdPP2O12/q12LnxRsjjTZ8eRw=='
})
poloniex = ccxt.poloniex({
    'apikey':'CHCOY03G-994D931A-ZBSHR59I-BWZXIB7K',
    'secret': '577d50d89352722a1a36b63ebaa8c04ff5308c847c5ef92987a8d001a7153fd78902d12d5a8b4c8c9735e73e77f04e3a372599506ce9b9f415ffcd95c1720647'
})
quoinex = ccxt.quoinex({
    'apikey':'362191',
    'secret': 'rh1lyIQkX0cyo1+hvihqluVblukpnP4AnW7q2P38s8HHFLbuLd5wlwdujjM/+254foiOdxR0hxlYr5aHfps5Iw=='
})

@app.route("/")
def index():
    cursor = con.cursor()
    cursor.execute("select * from abc")
    #data = cursor.fetchone()
    data = cursor.fetchall()
    
    
    return render_template('index.html',data=data)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/exchanges")
def exchange():
    cursor = con.cursor()
    #kraken = ccxt.kraken()
    #df= kraken.fetchTicker('BTC/USD')
    #df.pop('info')
    df = {'ask': 10031.2,
    'average': None,
    'baseVolume': 15986.87540788,
    'bid': 10010.9,
    'change': None,
    'close': None,
    'datetime': '2018-03-08T11:28:34.170Z',
    'first': None,
    'high': 10723.8,
    'last': 10031.3,
    'low': 9388.1,
    'open': 9903.0,
    'percentage': None,
    'quoteVolume': 158913884.5489005,
    'symbol': 'BTC/USD',
    'timestamp': 1520508514170,
    'vwap': 9940.27166}

    df1 = [(x,y) for x,y in df.items()]
    print(df1)
    #df = pd.to_json(df)
    #cursor.execute("insert into exchanges(data) values('"+str(df1)+")'")
    #df1 = "insert into exchanges(data) values("+str(df1)+")"
    
    return render_template('exchangeSummer.hmtl',data=df1)

app.run(debug=True)