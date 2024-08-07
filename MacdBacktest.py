import pandas as pd
import ta
import numpy as np


class MacdBacktest:
    
    retornoMacd = []
    
    def __init__(self,data,retorno,macd_config,first):

        macd_df = pd.DataFrame();

        if first:
            
            
            for i in range(macd_config["qtd"]):
                
                indexStr = "macd_"+str(i)
                signalIndex = "sinal_"+str(i)
                diffIndex = "diff_"+str(i)

                slow = macd_config["config"][i]["slow"]
                fast = macd_config["config"][i]["fast"]
                window = macd_config["config"][i]["window"]            
                macd = ta.trend.MACD(data["Close"],slow, fast, window,False)
                
                if i == 0:
                                
                    macd_df[indexStr] = macd.macd()
                    macd_df[signalIndex] = macd.macd_signal()
                    macd_df[diffIndex] = macd.macd_diff()
                    macd_df["Close"] = data["Close"].tail(len(macd_df))
                    
                    for buyIndex in range(len(macd_config["buy"])):
                                      
                        '''
                        Pode ser que um dos values sejam string ou int, se um deles for int
                        então não vai ser um index do dataframe e sim um valor fixo, se for
                        string se é entendido que é uma coluna do dataframe.
                        '''
                        if(isinstance(macd_config["buy"][buyIndex]["value1"], str) & isinstance(macd_config["buy"][buyIndex]["value2"], str)):
                        
                            value1 = str(macd_config["buy"][buyIndex]["value1"])+"_"+str(i)
                            value2 = str(macd_config["buy"][buyIndex]["value2"])+"_"+str(i)    
                        
                            if buyIndex == 0:
                                
                                if macd_config["buy"][buyIndex]["greaterThan"]:                        
                                    macd_df.loc[macd_df[value1] > macd_df[value2], "Buy"] = macd_df["Close"]
                                else:                        
                                    macd_df.loc[macd_df[value1] < macd_df[value2], "Buy"] = macd_df["Close"]
        
                            else:
                                
                                if macd_config["buy"][buyIndex]["greaterThan"]:
                                    macd_df.loc[(macd_df[value1] > macd_df[value2]) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                                else:
                                    macd_df.loc[(macd_df[value1] < macd_df[value2]) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                        else:
                            
                            if (isinstance(macd_config["buy"][buyIndex]["value1"], str) & ~isinstance(macd_config["buy"][buyIndex]["value2"], str)):
                                
                                value1 = str(macd_config["buy"][buyIndex]["value1"])+"_"+str(i)
                                value2 = macd_config["buy"][buyIndex]["value2"]
                                
                                if buyIndex == 0:
                                    
                                    if macd_config["buy"][buyIndex]["greaterThan"]:                        
                                        macd_df.loc[macd_df[value1] > value2, "Buy"] = macd_df["Close"]
                                    else:                        
                                        macd_df.loc[macd_df[value1] < value2, "Buy"] = macd_df["Close"]
            
                                else:
                                    
                                    if macd_config["buy"][buyIndex]["greaterThan"]:
                                        macd_df.loc[(macd_df[value1] > value2) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                                    else:
                                        macd_df.loc[(macd_df[value1] < value2) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                            else:
                                
                                value1 = macd_config["buy"][buyIndex]["value1"]
                                value2 = str(macd_config["buy"][buyIndex]["value2"])+"_"+str(i)
                                
                                if buyIndex == 0:
                                    
                                    if macd_config["buy"][buyIndex]["greaterThan"]:                        
                                        macd_df.loc[value1 > macd_df[value2], "Buy"] = macd_df["Close"]
                                    else:                        
                                        macd_df.loc[value1 < macd_df[value2], "Buy"] = macd_df["Close"]
            
                                else:
                                    
                                    if macd_config["buy"][buyIndex]["greaterThan"]:
                                        macd_df.loc[(value1 > macd_df[value2]) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                                    else:
                                        macd_df.loc[(value1 < macd_df[value2]) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                                
                     
                        

                    for sellIndex in range(len(macd_config["sell"])):
                        
                        
                        if(isinstance(macd_config["sell"][sellIndex]["value1"], str) & isinstance(macd_config["sell"][sellIndex]["value2"], str)):

                            value1 = macd_config["sell"][sellIndex]["value1"]+"_"+str(i)
                            value2 = macd_config["sell"][sellIndex]["value2"]+"_"+str(i)
                            
                            if sellIndex == 0:
            
                                if macd_config["sell"][sellIndex]["greaterThan"]:                        
                                    macd_df.loc[macd_df[value1] > macd_df[value2], "Sell"] = macd_df["Close"]
                                else:                        
                                    macd_df.loc[macd_df[value1] < macd_df[value2], "Sell"] = macd_df["Close"]
                                    
                            else:
                                if macd_config["sell"][sellIndex]["greaterThan"]:
                                    macd_df.loc[(macd_df[value1] > macd_df[value2]) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                                else:
                                    macd_df.loc[(macd_df[value1] < macd_df[value2]) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                       
                        else:
                          
                            if (isinstance(macd_config["sell"][sellIndex]["value1"], str) & ~isinstance(macd_config["buy"][sellIndex]["value2"], str)):
                              
                                value1 = str(macd_config["sell"][buyIndex]["value1"])+"_"+str(i)
                                value2 = macd_config["sell"][buyIndex]["value2"]  
                                
                                                        
                                if sellIndex == 0:
                                
                                    if macd_config["sell"][sellIndex]["greaterThan"]:                        
                                        macd_df.loc[macd_df[value1] > value2, "Sell"] = macd_df["Close"]
                                    else:                        
                                        macd_df.loc[macd_df[value1] < value2, "Sell"] = macd_df["Close"]
                                        
                                else:
                                    if macd_config["sell"][sellIndex]["greaterThan"]:
                                        macd_df.loc[(macd_df[value1] > value2) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                                    else:
                                        macd_df.loc[(macd_df[value1] < value2) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                             
                            else:
                                
                                
                                value1 = macd_config["sell"][buyIndex]["value1"]  
                                value2 = str(macd_config["sell"][buyIndex]["value2"])+"_"+str(i)                                
                                                        
                                if sellIndex == 0:
                
                                    if macd_config["sell"][sellIndex]["greaterThan"]:                        
                                        macd_df.loc[value1 > macd_df[value2], "Sell"] = macd_df["Close"]
                                    else:                        
                                        macd_df.loc[value1 < macd_df[value2], "Sell"] = macd_df["Close"]
                                        
                                else:
                                    if macd_config["sell"][sellIndex]["greaterThan"]:
                                        macd_df.loc[(value1 > macd_df[value2]) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                                    else:
                                        macd_df.loc[(value1 < macd_df[value2]) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                                                                                                
                
                retorno[indexStr] = macd_df[indexStr]
                retorno["Buy"] = macd_df["Buy"]
                retorno["Sell"] = macd_df["Sell"]
                retorno["Close"] = macd_df["Close"]
                
        
        else:
            
            
            for i in range(macd_config["qtd"]):
                
                indexStr = "macd_"+str(i)
                signalIndex = "sinal_"+str(i)
                diffIndex = "diff_"+str(i)

                slow = macd_config["config"][i]["slow"]
                fast = macd_config["config"][i]["fast"]
                window = macd_config["config"][i]["window"]            
                macd = ta.trend.MACD(data["Close"],slow, fast, window,False)
                
                macd_df[indexStr] = macd.macd()
                macd_df[signalIndex] = macd.macd_signal()
                macd_df[diffIndex] = macd.macd_diff()
                macd_df["Close"] = data["Close"].tail(len(macd_df))
                
                
                
                for buyIndex in range(len(macd_config["buy"])):
                    
                    
                    if(isinstance(macd_config["buy"][buyIndex]["value1"], str) & isinstance(macd_config["buy"][buyIndex]["value2"], str)):
                    
                        value1 = str(macd_config["buy"][buyIndex]["value1"])+"_"+str(i)
                        value2 = str(macd_config["buy"][buyIndex]["value2"])+"_"+str(i)    
                        
                        

                        if macd_config["buy"][buyIndex]["greaterThan"]:
                            macd_df.loc[(macd_df[value1] > macd_df[value2]) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                        else:
                            macd_df.loc[(macd_df[value1] < macd_df[value2]) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                            
                    else:
                        
                        if (isinstance(macd_config["buy"][buyIndex]["value1"], str) & ~isinstance(macd_config["buy"][buyIndex]["value2"], str)):
                            
                            value1 = str(macd_config["buy"][buyIndex]["value1"])+"_"+str(i)
                            value2 = macd_config["buy"][buyIndex]["value2"]
                        
                        
                            if macd_config["buy"][buyIndex]["greaterThan"]:
                                macd_df.loc[(macd_df[value1] > value2) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                            else:
                                macd_df.loc[(macd_df[value1] < value2) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                                
                                
                        else:
                            
                            value1 = macd_config["buy"][buyIndex]["value1"]
                            value2 = str(macd_config["buy"][buyIndex]["value2"])+"_"+str(i)
                            
                            if macd_config["buy"][buyIndex]["greaterThan"]:
                                macd_df.loc[(macd_df[value1] > value2) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                            else:
                                macd_df.loc[(macd_df[value1] < value2) & (pd.notna(macd_df["Buy"])), "Buy"] = macd_df["Close"]
                            
                            
                for sellIndex in range(len(macd_config["sell"])): 
                    
                    
                    if(isinstance(macd_config["sell"][sellIndex]["value1"], str) & isinstance(macd_config["sell"][sellIndex]["value2"], str)):
                    
                        value1 = str(macd_config["sell"][sellIndex]["value1"])+"_"+str(i)
                        value2 = str(macd_config["sell"][sellIndex]["value2"])+"_"+str(i)    

                        if macd_config["sell"][sellIndex]["greaterThan"]:
                            macd_df.loc[(macd_df[value1] > macd_df[value2]) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                        else:
                            macd_df.loc[(macd_df[value1] < macd_df[value2]) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                    
                    
                    else:
                        
                        if (isinstance(macd_config["sell"][sellIndex]["value1"], str) & ~isinstance(macd_config["sell"][sellIndex]["value2"], str)):
                            
                            value1 = str(macd_config["sell"][sellIndex]["value1"])+"_"+str(i)
                            value2 = macd_config["sell"][sellIndex]["value2"]
                        
                        
                            if macd_config["sell"][sellIndex]["greaterThan"]:
                                macd_df.loc[(macd_df[value1] > value2) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                            else:
                                macd_df.loc[(macd_df[value1] < value2) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                                
                        else:
                            
                            value1 = macd_config["sell"][sellIndex]["value1"]
                            value2 = str(macd_config["sell"][sellIndex]["value2"])+"_"+str(i)
                            
                            if macd_config["sell"][buyIndex]["greaterThan"]:
                                macd_df.loc[(macd_df[value1] > value2) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                            else:
                                macd_df.loc[(macd_df[value1] < value2) & (pd.notna(macd_df["Sell"])), "Sell"] = macd_df["Close"]
                            
                            
                                
                        
                retorno[indexStr] = macd_df[indexStr]
                retorno["Buy"] = macd_df["Buy"]
                retorno["Sell"] = macd_df["Sell"]
                retorno["Close"] = macd_df["Close"]
                        
        
        
        self.retornoMacd = retorno
