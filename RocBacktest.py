import pandas as pd
import ta
import numpy as np


class RocBacktest:
    
    retornoRoc = []
    
    def __init__(self,data,retorno,roc_config,first):
        
        roc_df = pd.DataFrame()
        
        if first:
            
            for i in range(roc_config["qtd"]):

                indexStr = "Roc_"+str(i)
                roc = ta.momentum.ROCIndicator(data["Close"], roc_config["window"][i], False)
                        
                if i == 0:                        
                            
                    roc_df[indexStr] = roc.roc()
                    roc_df["Close"] = data["Close"].tail(len(roc_df))
                    
                    for buyIndex in range(len(roc_config["buy"])):

                        value = roc_config["buy"][buyIndex]["value"]
                        
                        if buyIndex == 0:                                                
                            if roc_config["buy"][buyIndex]["greaterThan"]:
                                roc_df.loc[roc_df[indexStr] > value, "Buy"] = roc_df["Close"]
                            else:                                
                                roc_df.loc[roc_df[indexStr] < value, "Buy"] = roc_df["Close"]
                        else:                        
                            if roc_config["buy"][buyIndex]["greaterThan"]:
                                roc_df.loc[(roc_df[indexStr] > value) & (pd.notna(roc_df["Buy"])), "Buy"] = roc_df["Close"]
                            else:
                                roc_df.loc[(roc_df[indexStr] < value) & (pd.notna(roc_df["Buy"])), "Buy"] = roc_df["Close"]
                            
                        
                    for sellIndex in range(len(roc_config["sell"])):                    

                        value = roc_config["sell"][sellIndex]["value"]
                        
                        if sellIndex == 0:
                                                    
                            if roc_config["sell"][sellIndex]["greaterThan"]:                    
                                roc_df.loc[roc_df[indexStr] > value, "Sell"] = roc_df["Close"]
                            else:    
                                roc_df.loc[roc_df[indexStr] < value, "Sell"] = roc_df["Close"]
                        else:
                            if roc_config["sell"][sellIndex]["greaterThan"]:
                                roc_df.loc[(roc_df[indexStr] > value) & (pd.notna(roc_df["Sell"])), "Sell"] = roc_df["Close"]
                            else:
                                roc_df.loc[(roc_df[indexStr] < value) & (pd.notna(roc_df["Sell"])), "Sell"] = roc_df["Close"]
                            

                else:
                    
                    roc_df[str(i)] = roc.roc()
                    roc_df["Close"] = data["Close"].tail(len(roc_df))

                    for buyIndex in range(len(roc_config["buy"])):

                        value = roc_config["buy"][buyIndex]["value"]
                        
                        if roc_config["buy"][buyIndex]["greaterThan"]:                                      
                            roc_df['Buy'] = np.where(
                                (roc_df[indexStr] > value) & (pd.notna(roc_df["Buy"])),roc_df["Close"],
                                np.nan
                            )                                        
                        else:                                                    
                            roc_df['Buy'] = np.where(
                                (roc_df[indexStr] < value) & (pd.notna(roc_df["Buy"])),roc_df["Close"],
                                np.nan
                            )
        
                    
                    for sellIndex in range(len(roc_config["sell"])):

                        value = roc_config["sell"][sellIndex]["value"]
                        
                        if roc_config["sell"][sellIndex]["greaterThan"]:                                        
                            roc_df['Sell'] = np.where(
                                (roc_df[indexStr] > value) & (pd.notna(roc_df["Sell"])),roc_df["Close"],
                                np.nan
                            )
                        else:                        
                            roc_df['Sell'] = np.where(
                                (roc_df[indexStr] < value) & (pd.notna(roc_df["Sell"])),roc_df["Close"],
                                np.nan
                            )

                
                retorno[indexStr] = roc_df[indexStr]
                retorno["Buy"] = roc_df["Buy"]
                retorno["Sell"] = roc_df["Sell"]
                retorno["Close"] = roc_df["Close"]
        else:
            
            for i in range(roc_config["qtd"]):

                indexStr = "Roc_"+str(i)
                roc = ta.momentum.ROCIndicator(data["Close"], roc_config["window"][i], False)                
                roc_df[indexStr] = roc.roc()
                roc_df["Close"] = data["Close"].tail(len(roc_df))
        
                for buyIndex in range(len(roc_config["buy"])):

                    value = roc_config["buy"][buyIndex]["value"]
                    
                    if roc_config["buy"][buyIndex]["greaterThan"]:                                      
                        roc_df['Buy'] = np.where(
                            (roc_df[indexStr] > value) & (pd.notna(roc_df["Buy"])),roc_df["Close"],
                            np.nan
                        )                                        
                    else:                                                    
                        roc_df['Buy'] = np.where(
                            (roc_df[indexStr] < value) & (pd.notna(roc_df["Buy"])),roc_df["Close"],
                            np.nan
                        )

                
                for sellIndex in range(len(roc_config["sell"])):

                    value = roc_config["sell"][sellIndex]["value"]
                    
                    if roc_config["sell"][sellIndex]["greaterThan"]:                                        
                        roc_df['Sell'] = np.where(
                            (roc_df[indexStr] > value) & (pd.notna(roc_df["Sell"])),roc_df["Close"],
                            np.nan
                        )
                    else:                        
                        roc_df['Sell'] = np.where(
                            (roc_df[indexStr] < value) & (pd.notna(roc_df["Sell"])),roc_df["Close"],
                            np.nan
                        )
                        
                
            retorno[indexStr] = roc_df[indexStr]
            retorno["Buy"] = roc_df["Buy"]
            retorno["Sell"] = roc_df["Sell"]
            retorno["Close"] = roc_df["Close"]
            
        
        self.retornoRoc = retorno