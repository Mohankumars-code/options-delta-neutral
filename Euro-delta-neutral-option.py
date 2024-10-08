#!/usr/bin/env python
# coding: utf-8


import time
from pandas import DataFrame
import requests
from optionprice import Option

print("European option pricing is used!")

def web_scrapper(stock,date):
    headers = {
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.nasdaq.com/',
    'referer': 'https://www.nasdaq.com/',
    'accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

    data = requests.get('https://api.nasdaq.com/api/quote/'+stock+'/option-chain?assetclass=stocks&date='+date+'&money=all', headers=headers).json()
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
    call_bid = call_ask = strike = put_bid = put_ask = call_Bid = call_Ask = Strike = put_Bid = put_Ask = []
    for i in table:
        call_bid.append(i["c_Bid"])
        call_ask.append(i["c_Ask"])
        put_bid.append(i["p_Bid"])
        put_ask.append(i["p_Ask"])
        strike.append(i['strike'])
    call_bid.pop(0),call_ask.pop(0),put_bid.pop(0),put_ask.pop(0),strike.pop(0)
    for i in call_bid:
        try:
            call_Bid.append(round(float(i),3))
        except ValueError:
            call_Bid.append(0.010)
    for i in call_ask:
        try:
            call_Ask.append(round(float(i),3))
        except ValueError:
            call_Ask.append(0.010)
    for i in put_bid:
        try:
            put_Bid.append(round(float(i),3))
        except ValueError:
            put_Bid.append(0.010)
    for i in put_ask:
        try:
            put_Ask.append(round(float(i),3))
        except ValueError:
            put_Ask.append(0.010)
    for i in strike:
        try:
            Strike.append(round(float(i),3))
        except ValueError:
            Strike.append(0.010)
            
    return call_Bid,call_Ask,put_Bid,put_Ask,Strike


def option_price(stock_price,Strike,time_to_expiry,volatility,risk_free_rate):
    european = True
    dv=0
    call_value = []
    put_value = []
    Type = "call"
    for i in Strike:
        Value = Option(european,Type,stock_price,i,time_to_expiry,volatility,risk_free_rate,dv)
        call_value.append(round(Value.getPrice(),3))
    Type = "put"
    for i in Strike:
        Value = Option(european,Type,stock_price,i,time_to_expiry,volatility,risk_free_rate,dv)
        put_value.append(round(Value.getPrice(),3))
        
    return call_value,put_value


def premium_checker(call_Bid,call_Ask,put_Bid,put_Ask,Strike,call_value,put_value):
    call_pre = []
    put_pre =[]
    for i in call_value:
        if(call_Bid[call_value.index(i)] <= i <= call_Ask[call_value.index(i)]):
            call_pre.append("Price at Neutral")
        elif(call_Bid[call_value.index(i)] <= call_Ask[call_value.index(i)] < i):
            call_pre.append("Price at Premium")
        elif(i < call_Bid[call_value.index(i)] <= call_Ask[call_value.index(i)]):
            call_pre.append("Price at Discount")
    for i in put_value:
        if(put_Bid[put_value.index(i)] <= i <= put_Ask[put_value.index(i)]):
            put_pre.append("Neutral Price")
        elif(put_Bid[put_value.index(i)] <= put_Ask[put_value.index(i)] < i):
            put_pre.append("Premium Price")
        elif(i < put_Bid[put_value.index(i)] <= put_Ask[put_value.index(i)]):
            put_pre.append("Discount Price")
    return call_pre,put_pre


while(True):
    stock = input("Enter the stock ticker (Ex. AAPL): ")
    date = input("Enter the Expiration date (Ex. 2024-09-30): ")
    stock_price = float(input("Enter the stock Price (Ex. 226.58): "))
    risk_free_rate = (float(input("Enter the Interest Rate(%) (Ex. 5): "))/100)
    time_to_expiry = float(input("Enter the Days Until Expiration in DTE (Ex. 61): "))
    volatility = (float(input("Enter the Volatility(%) (Ex. 12.5): "))/100)
    table = web_scrapper(stock,date)
    if table != "NULL":
        call_Bid,call_Ask,put_Bid,put_Ask,Strike = list_return(table)
        call_value,put_value = option_price(stock_price,Strike,time_to_expiry,volatility,risk_free_rate)
        call_pre,put_pre = premium_checker(call_Bid,call_Ask,put_Bid,put_Ask,Strike,call_value,put_value)

        print("For the Given Ticker {}".format(stock))
        for i in Strike:
            print("The Call Option Strike Price: {0} Actual Price {1} and Calculated Price {2} is Trading at {3}".format(i,round((call_Bid[Strike.index(i)]+call_Ask[Strike.index(i)])/2,3),call_value[Strike.index(i)],call_pre[Strike.index(i)]))
        for i in Strike:
            print("The Put Option Strike Price: {0} Actual Price {1} and Calculated Price {2} is Trading at {3}".format(i,round((put_Bid[Strike.index(i)]+put_Ask[Strike.index(i)])/2,3),put_value[Strike.index(i)],put_pre[Strike.index(i)]))
    else:
        Print("Try New stock ticker")




