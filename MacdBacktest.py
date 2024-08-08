import pandas as pd
import ta
import numpy as np


class MacdBacktest:
    
    retornoMacd = []
    macd_config = []
    
    
    def __init__(self,data,retorno,macd_config,first):

        self.macd_config = macd_config
        self.macd_df = pd.DataFrame();

        if first:
            
            
            for i in range(self.macd_config["qtd"]):
                
                indexStr = "macd_"+str(i)
                signalIndex = "sinal_"+str(i)
                diffIndex = "diff_"+str(i)

                slow = self.macd_config["config"][i]["slow"]
                fast = self.macd_config["config"][i]["fast"]
                window = self.macd_config["config"][i]["window"]            
                macd = ta.trend.MACD(data["Close"],slow, fast, window,False)
                
                if i == 0:
                                
                    self.macd_df[indexStr] = macd.macd()
                    self.macd_df[signalIndex] = macd.macd_signal()
                    self.macd_df[diffIndex] = macd.macd_diff()
                    self.macd_df["Close"] = data["Close"].tail(len(self.macd_df))
                    
                    
                    
                    for buyIndex in range(len(self.macd_config["buy"])):
                                      
                        '''
                        Pode ser que um dos values sejam string ou int, se um deles for int
                        então não vai ser um index do dataframe e sim um valor fixo, se for
                        string se é entendido que é uma coluna do dataframe.
                        '''
                        if(isinstance(self.macd_config["buy"][buyIndex]["value1"], str) & isinstance(self.macd_config["buy"][buyIndex]["value2"], str)):
                                                                            
                            self.greaterThanValidationFirst("buy","Buy",buyIndex,indexStr,i)
                        
                            
                        else:
                                                                                                                
                            self.allValidationsDifferentTypes("buy","Buy",buyIndex,indexStr,i)
                                
                                        
                        retorno["Buy"] = self.macd_df["Buy"]
                        
                         
                    for sellIndex in range(len(self.macd_config["sell"])):
                        
                        
                        if(isinstance(self.macd_config["sell"][sellIndex]["value1"], str) & isinstance(self.macd_config["sell"][sellIndex]["value2"], str)):
                            
                            self.greaterThanValidationFirst("sell","Sell",sellIndex,indexStr,i)                                                        
                       
                        
                        else:
                          
                            self.allValidationsDifferentTypes("sell","Sell",sellIndex,indexStr,i)
                                                        
                        retorno["Sell"] = self.macd_df["Sell"]
                

                retorno[indexStr] = self.macd_df[indexStr]
                retorno["Close"] = self.macd_df["Close"]
                
        
        else:
            
            self.macd_df["Buy"] = retorno["Buy"]
            self.macd_df["Sell"] = retorno["Sell"]
            
            for i in range(macd_config["qtd"]):
                
                indexStr = "macd_"+str(i)
                signalIndex = "sinal_"+str(i)
                diffIndex = "diff_"+str(i)

                slow = macd_config["config"][i]["slow"]
                fast = macd_config["config"][i]["fast"]
                window = macd_config["config"][i]["window"]            
                macd = ta.trend.MACD(data["Close"],slow, fast, window,False)
                
                self.macd_df[indexStr] = macd.macd()
                self.macd_df[signalIndex] = macd.macd_signal()
                self.macd_df[diffIndex] = macd.macd_diff()
                self.macd_df["Close"] = data["Close"].tail(len(self.macd_df))
                
                
                
                for buyIndex in range(len(macd_config["buy"])):
                    
                    
                    self.allValidations("buy","Buy",buyIndex,indexStr,i)
                    retorno["Buy"] = self.macd_df["Buy"]
                    
                            
                for sellIndex in range(len(macd_config["sell"])): 
                    
                    
                    self.allValidations("sell","Sell",sellIndex,indexStr,i)
                    
                    retorno["Sell"] = self.macd_df["Sell"]                                        
                                
                        
                retorno[indexStr] = self.macd_df[indexStr]                                                                
                retorno["Close"] = self.macd_df["Close"]
                        
        
        
        self.retornoMacd = retorno


    def greaterThanValidationFirst(self,column_config,column_df,column_transct,indexStr,i):            
            
        value1 = str(self.macd_config[column_config][column_transct]["value1"])+"_"+str(i)
        value2 = str(self.macd_config[column_config][column_transct]["value2"])+"_"+str(i)    
    
        if column_transct == 0:
            
            if self.macd_config[column_config][column_transct]["greaterThan"]: 
                self.macd_df.loc[self.macd_df[value1] > self.macd_df[value2], column_df] = self.macd_df["Close"]
            else:                                                                      
                self.macd_df.loc[self.macd_df[value1] < self.macd_df[value2], column_df] = self.macd_df["Close"]

        else:
            
            if self.macd_config[column_config][column_transct]["greaterThan"]:
                self.macd_df.loc[(self.macd_df[value1] > self.macd_df[value2]) & (pd.notna(self.macd_df[column_df])), "Buy"] = self.macd_df["Close"]
            else:
                self.macd_df.loc[(self.macd_df[value1] < self.macd_df[value2]) & (pd.notna(self.macd_df[column_df])), "Buy"] = self.macd_df["Close"]
                
                
                
    def allValidationsDifferentTypes(self,column_config,column_df,column_transct,indexStr,i):    
        
        if (isinstance(self.macd_config[column_config][column_transct]["value1"], str) & ~isinstance(self.macd_config[column_config][column_transct]["value2"], str)):
            
            value1 = str(self.macd_config[column_config][column_transct]["value1"])+"_"+str(i)
            value2 = self.macd_config[column_config][column_transct]["value2"]  
            
                                    
            if column_transct == 0:
            
                if self.macd_config[column_config][column_transct]["greaterThan"]:                        
                    self.macd_df.loc[self.macd_df[value1] > value2, column_df] = self.macd_df["Close"]
                else:                        
                    self.macd_df.loc[self.macd_df[value1] < value2, column_df] = self.macd_df["Close"]
                    
            else:
                if self.macd_config[column_config][column_transct]["greaterThan"]:
                    self.macd_df.loc[(self.macd_df[value1] > value2) & (pd.notna(self.macd_df[column_df])), column_df] = self.macd_df["Close"]
                else:
                    self.macd_df.loc[(self.macd_df[value1] < value2) & (pd.notna(self.macd_df[column_df])), column_df] = self.macd_df["Close"]
         
        else:
            
            
            value1 = self.macd_config[column_config][column_transct]["value1"]  
            value2 = str(self.macd_config[column_config][column_transct]["value2"])+"_"+str(i)                                
                                    
            if column_transct == 0:

                if self.macd_config[column_config][column_transct]["greaterThan"]:                        
                    self.macd_df.loc[value1 > self.macd_df[value2], column_df] = self.macd_df["Close"]
                else:                        
                    self.macd_df.loc[value1 < self.macd_df[value2], column_df] = self.macd_df["Close"]
                    
            else:
                if self.macd_config[column_config][column_transct]["greaterThan"]:
                    self.macd_df.loc[(value1 > self.macd_df[value2]) & (pd.notna(self.macd_df[column_df])), column_df] = self.macd_df["Close"]
                else:
                    self.macd_df.loc[(value1 < self.macd_df[value2]) & (pd.notna(self.macd_df[column_df])), column_df] = self.macd_df["Close"]
        
                
                
    def allValidations(self,column_config,column_df,column_transct,indexStr,i):
        
        
        #print(self.macd_df)
        if(isinstance(self.macd_config[column_config][column_transct]["value1"], str) & isinstance(self.macd_config[column_config][column_transct]["value2"], str)):
                    
            value1 = str(self.macd_config[column_config][column_transct]["value1"])+"_"+str(i)
            value2 = str(self.macd_config[column_config][column_transct]["value2"])+"_"+str(i)    

            if self.macd_config[column_config][column_transct]["greaterThan"]:
                
                self.macd_df[column_df] = np.where(
                    (self.macd_df[value1] > self.macd_df[value2]) 
                    & 
                    (pd.notna(self.macd_df[column_df])),
                    self.macd_df["Close"],
                    np.nan)                                                
            else:
                                
                self.macd_df[column_df] = np.where(
                    (self.macd_df[value1] < self.macd_df[value2]) 
                    & 
                    (pd.notna(self.macd_df[column_df])),
                    self.macd_df["Close"],
                    np.nan
                )
                                
        
        
        else:
            
            if (isinstance(self.macd_config[column_config][column_transct]["value1"], str) & ~isinstance(self.macd_config[column_config][column_transct]["value2"], str)):
                                
                value1 = str(self.macd_config[column_config][column_transct]["value1"])+"_"+str(i)
                value2 = self.macd_config[column_config][column_transct]["value2"]
            
            
                if self.macd_config[column_config][column_transct]["greaterThan"]:
                   
                
                   self.macd_df[column_df] = np.where(
                        (self.macd_df[value1] > value2) 
                        &
                        (pd.notna(self.macd_df[column_df])),
                        self.macd_df["Close"],
                        np.nan
                    )
                                      
                else:
                    
                    self.macd_df[column_df] = np.where(
                         (self.macd_df[value1] < value2)
                         & 
                         (pd.notna(self.macd_df[column_df])),
                         self.macd_df["Close"],
                         np.nan
                     )                    
                    
                    
            else:
                
                value1 = self.macd_config[column_config][column_transct]["value1"]
                value2 = str(self.macd_config[column_config][column_transct]["value2"])+"_"+str(i)
                
                if self.macd_config[column_config][column_transct]["greaterThan"]:
                    
                    
                    self.macd_df[column_df] = np.where(
                         (value1 > self.macd_df[value2]) 
                         & 
                         (pd.notna(self.macd_df[column_df])),
                         self.macd_df["Close"],
                         np.nan
                     )
                    
                else:
                    
                    self.macd_df[column_df] = np.where(
                         (value1 < self.macd_df[value2]) 
                         & 
                         (pd.notna(self.macd_df[column_df])),
                         self.macd_df["Close"],
                         np.nan
                     )