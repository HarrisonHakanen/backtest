import pandas as pd
import ta
import numpy as np


class RocBacktest:
    
    retornoRoc = []
    roc_config = []
    roc_df = []
    
    def __init__(self,data,retorno,roc_config,first):
        
        self.roc_config = roc_config
        self.roc_df = pd.DataFrame()
        
        if first:
            
                        
            for i in range(roc_config["qtd"]):

                indexStr = "Roc_"+str(i)
                roc = ta.momentum.ROCIndicator(data["Close"], roc_config["window"][i], False)
                        
                if i == 0:                        
                            
                    self.roc_df[indexStr] = roc.roc()
                    self.roc_df["Close"] = data["Close"].tail(len(self.roc_df))
                            
                    
                    for buyIndex in range(len(roc_config["buy"])):
                        
                        self.greaterThanValidationFirst("buy","Buy",buyIndex,indexStr)
                            
                        
                    for sellIndex in range(len(roc_config["sell"])):
                        
                        self.greaterThanValidationFirst("sell","Sell",sellIndex,indexStr)
                            

                else:
                    
                    self.roc_df[str(i)] = roc.roc()
                    self.roc_df["Close"] = data["Close"].tail(len(self.roc_df))

                    for buyIndex in range(len(roc_config["buy"])):

                        self.greaterThanValidation("buy","Buy",buyIndex,indexStr)                                                 
        
                    
                    for sellIndex in range(len(roc_config["sell"])):
                        
                        self.greaterThanValidation("sell","Sell",sellIndex,indexStr)                    

                
                retorno[indexStr] = self.roc_df[indexStr]
                retorno["Buy"] = self.roc_df["Buy"]
                retorno["Sell"] = self.roc_df["Sell"]
                retorno["Close"] = self.roc_df["Close"]
                
        else:
            
            
            for i in range(roc_config["qtd"]):

                indexStr = "Roc_"+str(i)
                roc = ta.momentum.ROCIndicator(data["Close"], roc_config["window"][i], False)                
                self.roc_df[indexStr] = roc.roc()
                self.roc_df["Close"] = data["Close"].tail(len(self.roc_df))
        
                for buyIndex in range(len(roc_config["buy"])):
                    
                    self.greaterThanValidation("buy","Buy",buyIndex,indexStr)                    
                    
                
                for sellIndex in range(len(roc_config["sell"])):

                    
                    self.greaterThanValidation("sell","Sell",sellIndex,indexStr)
                        
                
            retorno[indexStr] = self.roc_df[indexStr]
            retorno["Buy"] = self.roc_df["Buy"]
            retorno["Sell"] = self.roc_df["Sell"]
            retorno["Close"] = self.roc_df["Close"]
            
        self.retornoRoc = retorno
        
        
                
    def greaterThanValidation(self,column_config,column_df,column_transct,indexStr):
        
        value = self.roc_config[column_config][column_transct]["value"]
        
        if self.roc_config[column_config][column_transct]["greaterThan"]:                                        
            self.roc_df[column_df] = np.where(
                (self.roc_df[indexStr] > value) & (pd.notna(self.roc_df[column_df])),self.roc_df["Close"],
                np.nan
            )
        else:                        
            self.roc_df[column_df] = np.where(
                (self.roc_df[indexStr] < value) & (pd.notna(self.roc_df[column_df])),self.roc_df["Close"],
                np.nan
            )                
    
    
    def greaterThanValidationFirst(self,column_config,column_df,column_transct,indexStr):
    
        value = self.roc_config[column_config][column_transct]["value"]    
    
        if column_transct == 0:
                                    
            if self.roc_config[column_config][column_transct]["greaterThan"]:                    
                self.roc_df.loc[self.roc_df[indexStr] > value, column_df] = self.roc_df["Close"]
            else:    
                self.roc_df.loc[self.roc_df[indexStr] < value, column_df] = self.roc_df["Close"]
        else:
            if self.roc_config[column_config][column_transct]["greaterThan"]:
                self.roc_df.loc[(self.roc_df[indexStr] > value) & (pd.notna(self.roc_df[column_df])), column_df] = self.roc_df["Close"]
            else:
                self.roc_df.loc[(self.roc_df[indexStr] < value) & (pd.notna(self.roc_df[column_df])), column_df] = self.roc_df["Close"]
                    
        