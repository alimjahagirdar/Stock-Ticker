from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pandas as pd
import pyrebase
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
from numerize import numerize
from flask import *
from prophet import Prophet
from prophet.plot import plot_plotly
from yahooquery import Ticker

main2 = Flask(__name__)



path = "C:/Users/alimj/AppData/Local/Programs/Python/Python311/stocks.csv"
df = pd.read_csv(path)

firebaseConfig = {
    "apiKey": "",
    "authDomain": "",
     "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
  }
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@main2.route("/login")
def login():
    return render_template("login.html")

#Sign up/ Register
@main2.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@main2.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        
        bse = yf.Ticker("^BSESN") 
        sen = bse.info["regularMarketOpen"]
        curr_price_bse = "{0:,.2f}".format(sen)
        previous_bse_price = bse.info['regularMarketPreviousClose']
        sengrow = sen - previous_bse_price
        sengroww = "{0:,.2f}".format(sengrow)
          
        
        nse = yf.Ticker("^NSEI")
        nif = nse.info["regularMarketOpen"]
        curr_price_nif = "{0:,.2f}".format(nif)
        previous_nse_price = nse.info["regularMarketPreviousClose"]
        nifgrow = nif - previous_nse_price
        nifgrowa = "{0:,.2f}".format(nifgrow)


        nse100 = yf.Ticker('^CNX100')
        nif100 = nse100.info["regularMarketOpen"]
        curr_price_nif100 = "{0:,.2f}".format(nif100)
        previous_nse100_price = nse100.info["regularMarketPreviousClose"]
        nifgroww100 = nif100 - previous_nse100_price
        nifgroww100a = "{0:,.2f}".format(nifgroww100)


        niftybank = yf.Ticker('^NSEBANK')
        nifbank = niftybank.info["regularMarketOpen"]
        curr_price_nifbank = "{0:,.2f}".format(nifbank)
        previous_nsebank_price = niftybank.info["regularMarketPreviousClose"]
        nifgrowwbank = nifbank - previous_nsebank_price
        nifgrowwbanka = "{0:,.2f}".format(nifgrowwbank)


        return render_template("user.html",email = person["email"], name = person["name"],sensex=curr_price_bse,sengroww=sengroww,NIFTY50=curr_price_nif,nifgroww=nifgrowa, NIFTY100=curr_price_nif100,nifgrow100=nifgroww100a,NIFTYBANK=curr_price_nifbank,NIFTYBANKGROWW=nifgrowwbanka)
    else:
        return redirect('/')




@main2.route("/profile")
def profile():
    if person["is_logged_in"] == True:
        return render_template("profile.html",emailp = person["email"], namep = person["name"])
    else:
        return redirect(url_for('login'))

@main2.route("/home")
def move():
    return redirect(url_for('welcome'))

#If someone clicks on login, they are redirected to /result
@main2.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@main2.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True 
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            
            #Append data to the firebase realtime database
            data = {"name": name, "email": email,"password":password}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

@main2.route('/')
def home():
    person["is_logged_in"] = False 
    bse = yf.Ticker("^BSESN") 
    sen = bse.info["regularMarketOpen"]
    curr_price_bse = "{0:,.2f}".format(sen)
    previous_bse_price = bse.info['regularMarketPreviousClose']
    sengrow = sen - previous_bse_price
    sengroww = "{0:,.2f}".format(sengrow)
        
    nse = yf.Ticker("^NSEI")
    nif = nse.info["regularMarketOpen"]
    curr_price_nif = "{0:,.2f}".format(nif)
    previous_nse_price = nse.info["regularMarketPreviousClose"]
    nifgrow = nif - previous_nse_price
    nifgrowa = "{0:,.2f}".format(nifgrow)

    nse100 = yf.Ticker('^CNX100')
    nif100 = nse100.info["regularMarketOpen"]
    curr_price_nif100 = "{0:,.2f}".format(nif100)
    previous_nse100_price = nse100.info["regularMarketPreviousClose"]
    nifgroww100 = nif100 - previous_nse100_price
    nifgroww100a = "{0:,.2f}".format(nifgroww100)

    niftybank = yf.Ticker('^NSEBANK')
    nifbank = niftybank.info["regularMarketOpen"]
    curr_price_nifbank = "{0:,.2f}".format(nifbank)
    previous_nsebank_price = niftybank.info["regularMarketPreviousClose"]
    nifgrowwbank = nifbank - previous_nsebank_price
    nifgrowwbanka = "{0:,.2f}".format(nifgrowwbank)

    return render_template("Home.html",sensex=curr_price_bse,sengroww=sengroww,NIFTY50=curr_price_nif,nifgroww=nifgrowa, NIFTY100=curr_price_nif100,nifgrow100=nifgroww100a,NIFTYBANK=curr_price_nifbank,NIFTYBANKGROWW=nifgrowwbanka)





@main2.route('/search',methods=['POST','GET'])
def search():
    tickers = yf.Tickers(list(df.Symbol))
    search = request.form['stock']
    Stock_name = tickers.tickers[search].info["longName"]
    PRICE = tickers.tickers[search].info["currentPrice"]
    #date = tickers.tickers[search].info["regularMarketTime"]
    PRICEa = "{0:,.2f}".format(PRICE)
    previous_market_price = tickers.tickers[search].info["regularMarketPreviousClose"]
    growth = PRICE - previous_market_price
    growtha = "{0:,.2f}".format(growth)

    hist = tickers.tickers[search].history(period='max')
    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Line(x = hist.index,y = hist['Close'],name='Price',fill='tozeroy'),secondary_y=False)
    fig.add_trace(go.Bar(x=hist.index,y=hist['Volume'],name='Volume'),secondary_y=True)
    fig.update_yaxes(range=[0,7000000000],secondary_y=True)
    fig.update_yaxes(visible=False, secondary_y=True)
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(
    autosize=True)
    fig.update_yaxes(color='white') 
    fig.update_xaxes(color='white',zeroline=False) 
    fig.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
    )

    graph = fig.to_html(full_html=False,default_height=500, default_width=800)
   
    ticker = Ticker(search)
    data = ticker.asset_profile[search]
    comapny = data['longBusinessSummary']
    name = tickers.tickers[search].info["shortName"]
    open = tickers.tickers[search].info["open"]
    close = tickers.tickers[search].info["previousClose"]
    thigh = tickers.tickers[search].info["dayHigh"]
    tlow = tickers.tickers[search].info["dayLow"]
    flow = tickers.tickers[search].info["fiftyTwoWeekLow"]
    fhigh = tickers.tickers[search].info["fiftyTwoWeekHigh"]
    mc = tickers.tickers[search].info["marketCap"]
    a = numerize.numerize(mc)
    #roe = ticker[search].info["returnOnEquity"]
    pe = tickers.tickers[search].info["trailingPE"]
    macap = "{0:,.2f}".format(pe)
    eps = tickers.tickers[search].info["trailingEps"]
    pb = tickers.tickers[search].info["priceToBook"]
    b = "{0:,.2f}".format(pb)
    #div = tickers.tickers[search].info["dividendYield"]
    bv = tickers.tickers[search].info["bookValue"]
    data1=ticker.financial_data[search]
    de = data1['debtToEquity']

    sector=data["sector"]
    Emp=data['fullTimeEmployees']
    phone=data["phone"]
    city=data["city"]
    country=data["country"]
    industry=data["industry"]
    website=data["website"]
 
    
    news0 = tickers.tickers[search].news[0]
    title0 = news0['title']
    link0 = news0['link']
    pub0 =news0['publisher']

    news1 = tickers.tickers[search].news[1]
    title1 = news1['title']
    link1 = news1['link']
    pub1 =news1['publisher']
     
    F = tickers.tickers[search].major_holders.head(3)
    start, stop, step = 0, -1, 1
    F= F[0].str.slice(start, stop, step)
    v = tickers.tickers[search].major_holders.head(3)
    v[1] = v[1].replace(['% of Shares Held by All Insider'],'Promoters')
    type =v[1]
    
    fig = go.Figure(data=[go.Pie(labels=type, values=F, hole=.4)])
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(
    autosize=True,
    font_color="white")
    pie = fig.to_html(full_html=False)


    
    stat = ticker.income_statement(trailing=False)
    reve = stat[["asOfDate","TotalRevenue"]]
    regraph = (reve.rename(columns={'asOfDate':'Revenue'}))
    figre = px.bar(regraph,x="Revenue", y ="TotalRevenue")
    figre.update_layout(showlegend=False)
    figre.update_yaxes(visible=False)
    figre.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    figre.update_xaxes(color='white') 
    figre.update_layout(
    autosize=False,
    minreducedwidth=250,
    minreducedheight=250,
    width=400,
    height=350)
    graphrev = figre.to_html(full_html=False)



    net = stat[["asOfDate","NetIncome"]]
    netgraph = (net.rename(columns={'asOfDate':'Net Income'}))
    fign = px.bar(netgraph,x="Net Income", y ="NetIncome")
    fign.update_layout(showlegend=False)
    fign.update_yaxes(visible=False)
    fign.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fign.update_xaxes(color='white') 
    fign.update_layout(
    autosize=False,
    minreducedwidth=250,
    minreducedheight=250,
    width=400,
    height=350)
    graphnet = fign.to_html(full_html=False)



    gross = stat[["asOfDate","GrossProfit"]]
    grossgraph = (gross.rename(columns={'asOfDate':'Gross Profit'}))
    figg = px.bar(grossgraph,x="Gross Profit", y ="GrossProfit")
    figg.update_layout(showlegend=False)
    figg.update_yaxes(visible=False) 
    figg.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    figg.update_xaxes(color='white') 
    figg.update_layout(
    autosize=False,
    minreducedwidth=250,
    minreducedheight=250,
    width=400,
    height=350)
    graphg = figg.to_html(full_html=False)


    stat["asOfDate"] = stat["asOfDate"].dt.date
    income =stat.T
    income.columns = income.iloc[0]
    In=income.loc[["asOfDate","TotalRevenue","CostOfRevenue","GrossProfit","OperatingExpense","DilutedEPS","OtherOperatingExpenses","NetIncome"
                          ,"EBIT","NormalizedEBITDA"]]
    In = In.iloc[1:, :]
    inc = In.to_html(header="true", table_id="table",border = '1',index='true',col_space='50')


    
    bal = ticker.balance_sheet()
    bal["asOfDate"] = bal["asOfDate"].dt.date
    Bal = bal.T
    Bal.columns = Bal.iloc[0]
    Bal = Bal.loc[['TotalAssets',"CurrentAssets","TotalNonCurrentAssets",'TotalLiabilitiesNetMinorityInterest','CurrentLiabilities','Payables'
                             ,'TotalTaxPayable','DividendsPayable','CurrentDebt','TotalNonCurrentLiabilitiesNetMinorityInterest','LongTermProvisions',
                             'LongTermDebt','TotalDebt','NetDebt']]
    balance = Bal.to_html(header="true", table_id="table",border ='1',index='true',col_space='50')


    cash = ticker.cash_flow(trailing=False)
    cash["asOfDate"] = cash["asOfDate"].dt.date
    cash = cash.T
    cash.columns = cash.iloc[0]
    cas= cash.iloc[1:, :]
    cashflow=cas.to_html(header="true", table_id="table",border = '1',index='true',col_space='50')



    if person["is_logged_in"] == True:
        prid=tickers.tickers[search].history(period='max')
        prid = prid.reset_index()
        df_train = prid[['Date','Close']]
        df_train = df_train.rename(columns={"Date":"ds","Close":"y"})
        df_train['ds'] = df_train['ds'].dt.tz_localize(None)
        m= Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)
        figs=plot_plotly(m,forecast)
        figs.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'})
        figs.update_xaxes(color='white') 
        figs.update_yaxes(color='white') 
        figs.update_xaxes(rangeslider_visible=False)
        figs.update_xaxes(showgrid=False,zeroline=False)
        figs.update_yaxes(showgrid=True,zeroline=False,gridcolor='white')
        figs.update_yaxes(title='')
        figs.update_xaxes(title='')
        figs.update_layout(showlegend=True)
        pred = figs.to_html(full_html=False,default_height=300, default_width=1500)

        #return render_template('stock.html',display=True,price=PRICEa,ticker=search,change=growtha,graph=graph,
                             #Open=open,Close=close,thigh=thigh,tlow=tlow,fthigh=fhigh,ftlow=flow,mkc=a,
                             #pred=pred)
    
        return render_template('stock.html',display=True,price=PRICEa,stock_name=Stock_name,ticker=search,change=growtha,graph=graph,company=comapny,name=name,
                             Open=open,Close=close,thigh=thigh,tlow=tlow,fthigh=fhigh,ftlow=flow,mkc=a,PE=macap,EP=eps,PB=b,DE=de,
                            Bv=bv,sector=sector,industry = industry,employ=Emp,city=city,country=country,phone=phone,web=website,title0 = title0,link0 = link0,
                            pub0 = pub0,title1=title1,link1=link1,pub1 = pub1,pie = pie,graph1=graphrev,graph2=graphnet,graph3=graphg,table=inc,table2=balance,table3=cashflow,pred=pred)
    else:
        
        #return render_template('stock.html',display=False,price=PRICEa,ticker=search,change=growtha,graph=graph,
                             #Open=open,Close=close,thigh=thigh,tlow=tlow,fthigh=fhigh,ftlow=flow,mkc=a)

        return render_template('stock.html',display=False,price=PRICEa,stock_name=Stock_name,ticker=search,change=growtha,graph=graph,company=comapny,name=name,
                             Open=open,Close=close,thigh=thigh,tlow=tlow,fthigh=fhigh,ftlow=flow,mkc=a,PE=macap,EP=eps,PB=b,DE=de
                            ,Bv=bv,sector=sector,industry = industry,employ=Emp,city=city,country=country,phone=phone,web=website,title0 = title0,link0 = link0,
                            pub0 = pub0,title1=title1,link1=link1,pub1 = pub1,pie = pie,graph1=graphrev,graph2=graphnet,graph3=graphg,table=inc,table2=balance,table3=cashflow)

 

if __name__=='__main__':
    main2.run(port=1226) 
  
