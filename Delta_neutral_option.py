#!/usr/bin/env python
# coding: utf-8



import requests
import numpy as np



def web_scrapper(stock,date):
    headers = {
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.nasdaq.com/',
    'referer': 'https://www.nasdaq.com/',
    'accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    data = requests.get("https://api.nasdaq.com/api/quote/"+stock+"/option-chain/greeks?assetclass=stocks&date="+date, headers=headers).json()
    if (data != None):
        if (data["data"] != None):
            if (data["data"]["table"] != None):
                if (data["data"]["table"]["rows"] != None):
                    table = data["data"]["table"]["rows"]
                else:
                    table = "NULL"
            else:
                table = "NULL"
        else:
            table = "NULL"
    else:
        table = "NULL"

    return table



def list_return(table):
    call_delta = []
    strike = []
    put_delta = []
    for i in table:
        call_delta.append(i["cDelta"])

    for j in table:
        strike.append(j["strike"])

    for k in table:
        put_delta.append(k["pDelta"])
        
    return call_delta,strike,put_delta



def delta_checker(call_delta,put_delta,user_delta,strike):
    
    c_delta = np.asarray(call_delta)
    idx = (np.abs(c_delta - user_delta)).argmin()
    call_delta_value = call_delta[idx]
    call_delta_strike = strike[idx]
    p_delta = np.asarray(put_delta)
    idx = (np.abs(p_delta + user_delta)).argmin()
    put_delta_value = put_delta[idx]
    put_delta_strike = strike[idx]
    
    return call_delta_value,put_delta_value,call_delta_strike,put_delta_strike



while(True):
    stock = input("Enter the stock ticker (Ex. AAPL): ")
    date = input("Enter the date (Ex. 2024-10-30): ")
    user_delta = float(input("Enter the Delta (Ex. 0.5): "))
    table = web_scrapper(stock, date)
    if table != "NULL":
        call_delta, strike, put_delta = list_return(table)
        call_delta_value,put_delta_value,call_delta_strike,put_delta_strike = delta_checker(call_delta,put_delta,user_delta,strike)
        print("The Nearest Call Delta Value: {0} Associated strike Price: {1}".format(call_delta_value,call_delta_strike))
        print("The Nearest Put Delta Value: {0} Associated strike Price: {1}".format(put_delta_value,put_delta_strike))


