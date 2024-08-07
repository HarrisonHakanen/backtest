import pandas as pd
import ta
import numpy as np


class TsiBacktest:
    
    retornoTsi = []
    
    def __init__(self,data,retorno,tsi_config,first):
        
        tsi_df = pd.DataFrame()
        
        
        if first:
    
            
            for i in range(tsi_config["qtd"]):
    
                indexStr = "Tsi_"+str(i)
                tsi = ta.momentum.TSIIndicator(data["Close"],tsi_config["config"][i]["slow"],tsi_config["config"][i]["fast"],False)
    
                if i == 0:                        
                            
                    tsi_df[indexStr] = tsi.tsi()
                    tsi_df["Close"] = data["Close"].tail(len(tsi_df))
                                        
                    
                    for buyIndex in range(len(tsi_config["buy"])):

                        value = tsi_config["buy"][buyIndex]["value"]
                        
                        if buyIndex == 0:
                            if tsi_config["buy"][buyIndex]["greaterThan"]:
                                tsi_df.loc[tsi_df[indexStr] > value, "Buy"] = tsi_df["Close"]
                            else:                                
                                tsi_df.loc[tsi_df[indexStr] < value, "Buy"] = tsi_df["Close"]
                        else:
                            if tsi_config["buy"][buyIndex]["greaterThan"]:
                                tsi_df.loc[(tsi_df[indexStr] > value) & (pd.notna(tsi_df["Buy"])), "Buy"] = tsi_df["Close"]
                            else:
                                tsi_df.loc[(tsi_df[indexStr] < value) & (pd.notna(tsi_df["Buy"])), "Buy"] = tsi_df["Close"]
                                            
                    
                    for sellIndex in range(len(tsi_config["sell"])):
    
                        value = tsi_config["sell"][sellIndex]["value"]
                        
                        if sellIndex == 0:
                            if tsi_config["sell"][sellIndex]["greaterThan"]:
                                tsi_df.loc[tsi_df[indexStr] > value, "Sell"] = tsi_df["Close"]
                            else:
                                tsi_df.loc[tsi_df[indexStr] < value, "Sell"] = tsi_df["Close"]
                        else:
                            if tsi_config["sell"][sellIndex]["greaterThan"]:
                                tsi_df.loc[(tsi_df[indexStr] > value) & (pd.notna(tsi_df["Sell"])), "Sell"] = tsi_df["Close"]
                            else:
                                tsi_df.loc[(tsi_df[indexStr] < value) & (pd.notna(tsi_df["Sell"])), "Sell"] = tsi_df["Close"]
                
                else:
                	
                    tsi_df[str(i)] = tsi.tsi()
                    tsi_df["Close"] = data["Close"].tail(len(tsi_df))
                
                    for buyIndex in range(len(tsi_config["buy"])):
    
                        value = tsi_config["buy"][buyIndex]["value"]
                        
                        if tsi_config["buy"][buyIndex]["greaterThan"]:                
                            tsi_df['Buy'] = np.where(
                                (tsi_df[indexStr] > value) & (pd.notna(tsi_df["Buy"])),tsi_df["Close"],
                                np.nan
                            )
                        else:                                                    
                            tsi_df['Buy'] = np.where(
                                (tsi_df[indexStr] < value) & (pd.notna(tsi_df["Buy"])),tsi_df["Close"],
                                np.nan
                            )
                
                	
                    for sellIndex in range(len(tsi_config["sell"])):
    
                        value = tsi_config["sell"][sellIndex]["value"]
                        
                        if tsi_config["sell"][sellIndex]["greaterThan"]:                                        
                            tsi_df['Sell'] = np.where(
                                (tsi_df[indexStr] > value) & (pd.notna(tsi_df["Sell"])),tsi_df["Close"],
                                np.nan
                            )
                        else:                        
                            tsi_df['Sell'] = np.where(
                                (tsi_df[indexStr] < value) & (pd.notna(tsi_df["Sell"])),tsi_df["Close"],
                                np.nan
                            )
                
                
                retorno[indexStr] = tsi_df[indexStr]
                retorno["Buy"] = tsi_df["Buy"]
                retorno["Sell"] = tsi_df["Sell"]
                retorno["Close"] = tsi_df["Close"]
                
        else:
            
            
            for i in range(tsi_config["qtd"]):
            
                indexStr = "Tsi_"+str(i)
                tsi = ta.momentum.TSIIndicator(data["Close"],tsi_config["config"][i]["slow"],tsi_config["config"][i]["fast"],False)
                tsi_df[indexStr] = tsi.tsi()
                tsi_df["Close"] = retorno["Close"].tail(len(tsi_df))
                
                
                for buyIndex in range(len(tsi_config["buy"])):
    
                    value = tsi_config["buy"][buyIndex]["value"]
                    
                    if tsi_config["buy"][buyIndex]["greaterThan"]:               
                        tsi_df['Buy'] = np.where(
                            (tsi_df[indexStr] > value) & (pd.notna(tsi_df["Buy"])),tsi_df["Close"],
                            np.nan
                        )
                    else:                                           
                        tsi_df['Buy'] = np.where(
                            (tsi_df[indexStr] < value) & (pd.notna(tsi_df["Buy"])),tsi_df["Close"],
                            np.nan
                        )            
                
                for sellIndex in range(len(tsi_config["sell"])):
    
                    value = tsi_config["sell"][sellIndex]["value"]
                    
                    if tsi_config["sell"][sellIndex]["greaterThan"]:                                        
                        tsi_df['Sell'] = np.where(
                            (tsi_df[indexStr] > value) & (pd.notna(tsi_df["Sell"])),tsi_df["Close"],
                            np.nan
                        )
                    else:                        
                        tsi_df['Sell'] = np.where(
                            (tsi_df[indexStr] < value) & (pd.notna(tsi_df["Sell"])),tsi_df["Close"],
                            np.nan
                        )
                
                
                retorno[indexStr] = tsi_df[indexStr]
                retorno["Buy"] = tsi_df["Buy"]
                retorno["Sell"] = tsi_df["Sell"]
                retorno["Close"] = tsi_df["Close"]
                        
        
        
        self.retornoTsi = retorno
        
        