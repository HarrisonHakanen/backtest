import pandas as pd
import ta
import numpy as np


class TsiBacktest:
    
    
    retornoTsi = []
    tsi_config = []
    tsi_df = []
    
    
    def __init__(self,data,retorno,tsi_config,first):
        
        
        self.tsi_config = tsi_config
        self.tsi_df = pd.DataFrame()        
        
        
        if first:
    
            
            for i in range(self.tsi_config["qtd"]):
    
                indexStr = "Tsi_"+str(i)
                tsi = ta.momentum.TSIIndicator(data["Close"],self.tsi_config["config"][i]["slow"],self.tsi_config["config"][i]["fast"],False)
    
                if i == 0:                        
                            
                    self.tsi_df[indexStr] = tsi.tsi()
                    self.tsi_df["Close"] = data["Close"].tail(len(self.tsi_df))
                                        
                    
                    for buyIndex in range(len(self.tsi_config["buy"])):

                        self.greaterThanValidationFirst("buy","Buy",buyIndex,indexStr)
                                            
                    
                    for sellIndex in range(len(self.tsi_config["sell"])):
    
                        self.greaterThanValidationFirst("sell","Sell",sellIndex,indexStr)
                        
                
                else:
                	
                    self.tsi_df[str(i)] = tsi.tsi()
                    self.tsi_df["Close"] = data["Close"].tail(len(self.tsi_df))
                
                    for buyIndex in range(len(self.tsi_config["buy"])):
                            
                        self.greaterThanValidation("buy","Buy",buyIndex,indexStr)
                                                                
                	
                    for sellIndex in range(len(self.tsi_config["sell"])):
    
                        self.greaterThanValidation("sell","Sell",sellIndex,indexStr)
                       
                
                
                retorno[indexStr] = self.tsi_df[indexStr]
                retorno["Buy"] = self.tsi_df["Buy"]
                retorno["Sell"] = self.tsi_df["Sell"]
                retorno["Close"] = self.tsi_df["Close"]
                
        else:
            
            self.tsi_df["Buy"] = retorno["Buy"]
            self.tsi_df["Sell"] = retorno["Sell"]
            
            for i in range(tsi_config["qtd"]):
            
                indexStr = "Tsi_"+str(i)
                tsi = ta.momentum.TSIIndicator(data["Close"],tsi_config["config"][i]["slow"],tsi_config["config"][i]["fast"],False)
                self.tsi_df[indexStr] = tsi.tsi()
                self.tsi_df["Close"] = retorno["Close"].tail(len(self.tsi_df))
                
                
                for buyIndex in range(len(tsi_config["buy"])):
                    
                    self.greaterThanValidation("buy","Buy",buyIndex,indexStr)
                                        
                
                for sellIndex in range(len(tsi_config["sell"])):
                        
                    self.greaterThanValidation("sell","Sell",sellIndex,indexStr)
                                        
                
                
                retorno[indexStr] = self.tsi_df[indexStr]
                retorno["Buy"] = self.tsi_df["Buy"]
                retorno["Sell"] = self.tsi_df["Sell"]
                retorno["Close"] = self.tsi_df["Close"]
                        
        
        
        self.retornoTsi = retorno
        
        
        
    def greaterThanValidation(self,column_config,column_df,column_transct,indexStr):
        
        value = self.tsi_config[column_config][column_transct]["value"]
        
        if self.tsi_config[column_config][column_transct]["greaterThan"]:                                        
            self.tsi_df[column_df] = np.where(
                (self.tsi_df[indexStr] > value) & (pd.notna(self.tsi_df[column_df])),self.tsi_df["Close"],
                np.nan
            )
        else:                        
            self.tsi_df[column_df] = np.where(
                (self.tsi_df[indexStr] < value) & (pd.notna(self.tsi_df[column_df])),self.tsi_df["Close"],
                np.nan
            )
            
            
    def greaterThanValidationFirst(self,column_config,column_df,column_transct,indexStr):            
    
        value = self.tsi_config[column_config][column_transct]["value"]    
    
        if column_transct == 0:
                                    
            if self.tsi_config[column_config][column_transct]["greaterThan"]:                    
                self.tsi_df.loc[self.tsi_df[indexStr] > value, column_df] = self.tsi_df["Close"]
            else:    
                self.tsi_df.loc[self.tsi_df[indexStr] < value, column_df] = self.tsi_df["Close"]
        else:
            if self.tsi_config[column_config][column_transct]["greaterThan"]:
                self.tsi_df.loc[(self.tsi_df[indexStr] > value) & (pd.notna(self.tsi_df[column_df])), column_df] = self.tsi_df["Close"]
            else:
                self.tsi_df.loc[(self.tsi_df[indexStr] < value) & (pd.notna(self.tsi_df[column_df])), column_df] = self.tsi_df["Close"]