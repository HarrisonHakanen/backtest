import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.offline import plot
from RocBacktest import RocBacktest
from TsiBacktest import TsiBacktest
from MacdBacktest import MacdBacktest



def backtest_analysis(data,indicator_list):
    
    first = True
    retorno = pd.DataFrame()
    
    for i in range(len(indicator_config["indicators"])):

        nome = indicator_config["indicators"][i]["indicator_name"]
        
        if nome == "roc":  
            
            rocObj = RocBacktest(data,retorno,indicator_config["indicators"][i],first)            
            retorno = rocObj.retornoRoc
            
            first = False            
            print("roc")
            
        if nome == "tsi":
            
            tsiObj = TsiBacktest(data,retorno,indicator_config["indicators"][i],first)
            retorno = tsiObj.retornoTsi
                        
            first = False
            print("tsi")
        
        if nome == "macd":

            macdObj = MacdBacktest(data,retorno,indicator_config["indicators"][i],first)            
            retorno = macdObj.retornoMacd
            
            first = False            
            print("macd")

    
    return retorno



start_ = "2023-10-01"
end_ = "2024-08-03"

data = yf.download("CRFB3.SA", start= start_,end=end_)


roc_config = {
    "indicator_name":"roc",
    "qtd":1,
    "window":[9],
    "buy":[
        {
            "value":-4,
            "greaterThan":False,            
        }
    ],
    "sell":[
        {
            "value":8,
            "greaterThan":True,           
        }        
    ],
    "mm":{
        "medias":[]
    }
}

tsi_config = {
    "indicator_name":"tsi",
    "qtd":1,
    "config":[
            {
                "slow":25,
                "fast":5
            }
    ],
    "buy":[
        {
            "value":-28,
            "greaterThan":False,            
        }
    ],
    "sell":[
        {
            "value":33,
            "greaterThan":True,           
        }        
    ],
    "mm":{
        "medias":[]
    }
}

macd_config = {
    "indicator_name":"macd",
    "qtd":1,
    "config":[
            {
                "slow":26,
                "fast":12,
                "window":9
            }
    ],
    "buy":[
        {
            "value1":"sinal",
            "value2":"macd",
            "greaterThan":True,
        },
        {
            "value1":"sinal",
            "value2":0,
            "greaterThan":False,
        }
    ],
    "sell":[
        {
            "value1":"sinal",
            "value2":"macd",
            "greaterThan":False,
        }
    ],
    "mm":{
        "medias":[]
    }
}


indicator_config ={
    "indicators":[
        #roc_config,
        #tsi_config,
        macd_config
    ]
}


indicators_backtest = backtest_analysis(data,indicator_config)




fig = go.Figure()

fig.add_trace(go.Scatter(x=indicators_backtest.index, y=indicators_backtest["Close"],
                    mode='lines',name = "Close",line=dict(color='blue', width=1)))

fig.add_trace(go.Scatter(x=indicators_backtest.index, y=indicators_backtest["Buy"],
                    mode='markers', name='Buy',line=dict(color='green', width=1)))

fig.add_trace(go.Scatter(x=indicators_backtest.index, y=indicators_backtest["Sell"],
                    mode='markers', name='Sell',line=dict(color='red', width=1)))

plot(fig, auto_open=True)