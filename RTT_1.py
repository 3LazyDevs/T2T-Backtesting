import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px 
import plotly.graph_objects as go

# global prev_dict
global excel_dict
global excel_df
# global msl
# global tsl
global profit

line = None
buy = 0
sell = 0
profit = 0
day_count = 0
msl = 0
prev_dict = {"Top": 0, "Bottom": 0}
trades = []


# Calculate previous top and previous bottom
def prev_tb(i, fig, ind_vals, ind_date, ind_history, line):
    if(i == 0):
        pass
    else:
        # logic (for top: present value should be greater than previous and next value) 
        #(for bottom: present value should be less than previous value and next value)
        try:
            if ((ind_vals[i - 1] < ind_vals[i]) and (ind_vals[i + 1] < ind_vals[i])):
                    print(ind_vals[i], "Top", str(ind_date[i]))
                    fig.add_trace(go.Scatter(x=[ind_history[line].index[i]], y=[ind_history[line][i]], mode='markers', marker=dict(color='blue', size=5),showlegend=False, text=f"Type: Top<br>Value: {ind_vals[i]}<br>Date: {ind_date[i].strftime('%Y-%m-%d')}"))
                    # fig.add_annotation(x = ind_history[line].index[i], y = ind_history[line][i], text = "Top<br>" + str(ind_vals[i]), showarrow= True)
                    prev_dict["Top"] = ind_vals[i]
            if ((ind_vals[i - 1] > ind_vals[i]) and (ind_vals[i + 1] > ind_vals[i])):
                    print(ind_vals[i], "Bottom", str(ind_date[i]))
                    fig.add_trace(go.Scatter(x=[ind_history[line].index[i]], y=[ind_history[line][i]], mode='markers', marker=dict(color='yellow', size=5),showlegend=False, text=f"Type: Bottom<br>Value: {ind_vals[i]}<br>Date: {ind_date[i].strftime('%Y-%m-%d')}"))
                    # fig.add_annotation(x = ind_history[line].index[i], y = ind_history[line][i], text = "Bottom<br>" + str(ind_vals[i]), showarrow= True)
                    prev_dict["Bottom"] = ind_vals[i]

            return prev_dict

        except IndexError:
            pass

def trade(tsl_1, tsl_2, entry_buff, exit_buff, val,val_open,val_high,val_low,val_close, i, fig, prev_dict, ind_date, ind_history, line):
    global day_count
    candle = None
    trade_date, trade_action, trade_ls = ind_date[i], "null", "null" 
    buff_top = prev_dict["Top"] * entry_buff * 0.01 # buffer to exeute buy
    buff_bottom = prev_dict["Bottom"] * entry_buff * 0.01 # buffer to execute sell
    buffer_high = prev_dict["Top"] + buff_top # top + buffer
    buffer_low = prev_dict["Bottom"] - buff_bottom # bottom - buffer

    #calculate if the candle is a red candle or green candle
    if(val_close > val_open):
        candle = "Green"
    else:
        candle = "Red"
    
    if(prev_dict["Top"] and prev_dict["Bottom"]):
        try:
            if((val_open > buffer_high or val_high > buffer_high) and (val_open < buffer_low or val_low < buffer_low)):
                print("anomaly")
                check_backtesting_anomaly(tsl_1, ind_date, buffer_high, buffer_low,val,val_open, val_high, val_low, val_close, candle, i, fig, prev_dict, ind_history, line)

            else:

                try:
                    if(trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short"):
                        day_count += 1
                        tsl = trades[-1]["Stop_Loss"]
                        sell = trades[-1]["Entry_Value"]
                        tsl = sell + (sell * tsl_2 * 0.01)
                        trades[-1]["Stop_Loss"] = tsl
                        trade_exit(exit_buff, trades, val, val_open, val_close, val_high, val_low, ind_date, buffer_high, buffer_low, msl, i, candle, fig, prev_dict, ind_history, line)
                except Exception as e:
                    print("Caught at 1st exit", e)
                # check OHLC for buying
                if((val_open >= (buffer_high) or val_high >= (buffer_high))):
                    if((trades) and (trades[-1]["Action"] == "Buy" and trades[-1]["Trade_LS"] == "Long")):                        #print("Hold")
                        pass
                    else:  
                        Buy(tsl_1, ind_date, val_open, val_high,val_low, buffer_high, i, fig, prev_dict, ind_history, line)
                        day_count = 1
                
                if((trades) and trades[-1]["Action"] == "Buy" and trades[-1]["Trade_LS"] == "Long"):
                    day_count += 1
                    buy = trades[-1]["Entry_Value"]
                    tsl = trades[-1]["Stop_Loss"]
                    if(tsl == buy):
                        pass
                    else:
                        threshold = buy + (buy * 0.02)
                        if (val_high >= threshold):
                            tsl = buy
                        else:
                            if(day_count > 1):
                                tsl = buy - (buy * tsl_2 * 0.01)
                        trades[-1]["Stop_Loss"] = tsl
                
                if((trades) and trades[-1]["Action"] == "Buy" and trades[-1]["Trade_LS"] == "Long"):
                    trade_exit(exit_buff, trades, val, val_open, val_close, val_high, val_low, ind_date, buffer_high, buffer_low, msl, i, candle, fig, prev_dict, ind_history, line)

            # check OHLC for selling 
                if((val_open <= (buffer_low) or val_low <= (buffer_low))):
                    if((trades) and (trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short")):
                        # print("Hold")
                        pass

                    else:
                        # print("Entered Sell")
                        Sell(tsl_1, ind_date, val_open, val_low, val_high, buffer_low, i, fig, prev_dict, ind_history, line)
                        day_count = 1
                    
                if((trades) and trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short"):
                    sell = trades[-1]["Entry_Value"]
                    day_count += 1
                    tsl = trades[-1]["Stop_Loss"]
                    if(tsl == sell):
                        pass
                    else:
                        threshold = sell - (sell * 0.02)
                        if(val_high <= threshold):
                                tsl = sell
                        else:
                            if(day_count > 1):
                                tsl = sell + (sell * tsl_2 * 0.01)
                                
                        trades[-1]["Stop_Loss"] = tsl

                if((trades) and trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short"):
                    trade_exit(exit_buff, trades, val, val_open, val_close, val_high, val_low, ind_date, buffer_high, buffer_low, msl, i, candle, fig, prev_dict, ind_history, line)

                print(f"day_count = {day_count}")        
        
        except Exception as e:
            print(e)


def Buy(tsl_1, ind_date, val_open, val_high, val_low, buffer_high, i, fig, prev_dict, ind_history, line):
    print("Buy", ind_date[i])
    # print(trades)      
    # msl =  buffer_high - (buffer_high * risk_percent * 0.01)
    buy = buffer_high
    #to make sure buy sell does not happen outside the graph
    if(buffer_high < val_low):
        buy = val_open

    tsl = buy - (buy * tsl_1 * 0.01)
    threshold = buy + (buy * 0.02)
    if (val_high >= threshold):
        tsl = buy
    # fig.add_trace(go.Scatter(x=[ind_history[line].index[i]], y=[buy], mode='markers', marker=dict(color='blue', size=12),showlegend=False, text=f"Action: Buy<br>Entry: {buy}<br>Date: {ind_date[i].strftime('%Y-%m-%d')}"))
    fig.add_annotation(x = ind_history[line].index[i], y = buy, ax = 50, ay = -40, text = "Buy<br>" + str(buy), showarrow= True, arrowhead= 5)
    trades.append({"Action":"Buy", "Trade_LS": "Long", "Entry_Date" : ind_date[i].strftime("%Y-%m-%d"), "Prev_Top" :  prev_dict["Top"], 
    "Prev_Bottom" : prev_dict["Bottom"], "Entry_Value" : buy,"Exit_Value" : 0, "Exit_Date": 0, "Profit_Loss" : 0, "Stop_Loss" : tsl})

def Sell(tsl_1, ind_date, val_open, val_low, val_high, buffer_low, i, fig, prev_dict, ind_history, line):
    print("Sell", ind_date[i])
    # print(trades)
    # msl =  buffer_low + (buffer_low * risk_percent * 0.01)
    sell = buffer_low
    if(buffer_low > val_high):
        sell = val_open
    tsl = sell + (sell * tsl_1 * 0.01)
    threshold = sell - (sell * 0.02)
    if (val_low <= threshold):
        tsl = sell
    # fig.add_trace(go.Scatter(x=[ind_history[line].index[i]], y=[sell], mode='markers', marker=dict(color='yellow', size=12),showlegend=False, text=f"Action: Sell<br>Entry: {sell}<br>Date: {ind_date[i].strftime('%Y-%m-%d')}"))
    fig.add_annotation(x = ind_history[line].index[i], y = sell, ax = 20, ay = 50, text = "Sell<br>" + str(sell), showarrow= True,arrowhead= 5)
    trades.append({"Action":"Sell", "Trade_LS": "Short", "Entry_Date" : ind_date[i].strftime("%Y-%m-%d"), "Prev_Top" :  prev_dict["Top"], 
    "Prev_Bottom" : prev_dict["Bottom"], "Entry_Value" : sell,"Exit_Value" : 0, "Exit_Date": 0,"Profit_Loss" : 0, "Stop_Loss" : tsl})                          


def check_backtesting_anomaly(tsl_1, ind_date, buffer_high, buffer_low,val,val_open, val_high, val_low, val_close, candle, i, fig, prev_dict, ind_history, line):
    if(abs(val_high - val_close) < abs(val_low - val_close)):
        if((trades) and (trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short")):
            pass
        else:
            Sell(tsl_1, ind_date, val_open, val_low, val_high, buffer_low, i, fig, prev_dict, ind_history, line) 
        
        Buy(tsl_1, ind_date, val_open, val_high,val_low, buffer_high, i, fig, prev_dict, ind_history, line)
        
    else:
        if((trades) and (trades[-1]["Action"] == "Buy" and trades[-1]["Trade_LS"] == "Long")):                        #print("Hold")
            pass
        else:
            Buy(tsl_1, ind_date, val_open, val_high,val_low, buffer_high, i, fig, prev_dict, ind_history, line)
        
        Sell(tsl_1, ind_date, val_open, val_low, val_high, buffer_low, i, fig, prev_dict, ind_history, line) 
    

def trade_exit(exit_buff, trades, val, val_open, val_close, val_high, val_low, ind_date, buffer_high, buffer_low, msl, i, candle, fig, prev_dict, ind_history, line):
    tsl = trades[-1]["Stop_Loss"]
    print(f"tsl = {tsl}, date = {ind_date[i].strftime('%Y-%m-%d')}")
    print(trades[-1]["Action"], trades[-1]["Trade_LS"])
    if(trades[-1]["Action"] == "Buy"  and trades[-1]["Trade_LS"] == "Long"): #and (val_open > val_close)#
        buff_exit = prev_dict["Bottom"] - (prev_dict["Bottom"] * exit_buff * 0.01)
        if(tsl > val_open or tsl > val_low or tsl > val_high or tsl > val_close):
            trades[-1]["Trade_LS"] = "Exit"
            trades[-1]["Exit_Date"] = ind_date[i].strftime("%Y-%m-%d")
            trades[-1]["Exit_Value"] = tsl
            fig.add_trace(go.Scatter(x=[ind_history[line].index[i]], y=[tsl], mode='markers', marker=dict(color='#000', size=12,line=dict(width=2, color='#c7c7c7')),showlegend=False, text=f"Action: Exit Buy<br>Exit Value: {tsl}<br>Date: {ind_date[i].strftime('%Y-%m-%d')}"))
            # fig.add_annotation(x = ind_history[line].index[i], y = tsl,ax = 20,ay= 50, text = "Exit<br>" + str(tsl), showarrow= True,arrowhead= 5,bordercolor="#c7c7c7", borderwidth=2, borderpad=4, bgcolor="#ff7f0e", opacity=0.8)
        elif(buff_exit > val_low and prev_dict["Bottom"] and (entry_buff != exit_buff)):
            print("val_low = ", val_low, "Buffer exit = ", buff_exit)
            trades[-1]["Trade_LS"] = "Exit buffer triggered"  
            trades[-1]["Exit_Date"] = date_val.strftime("%Y-%m-%d")
            trades[-1]["Exit_Value"] = buff_exit
            fig.add_annotation(x = ind_history[line].index[i + days], y = buff_exit,ax = days,ay= 50, text = "Exit<br>" + str(tsl), showarrow= True,arrowhead= 5,bordercolor="#c7c7c7", borderwidth=2, borderpad=4, bgcolor="#ff7f0e", opacity=0.8)


    if(trades[-1]["Action"] == "Sell" and (tsl < val_close or tsl < val_high or tsl < val_open or tsl < val_low) and trades[-1]["Trade_LS"] == "Short"): # and (val_open < val_close)
        buff_exit = prev_dict["Top"] + (prev_dict["Top"] * exit_buff * 0.01)
        print("Entered Sell exit")
        if(tsl < val_close or tsl < val_high or tsl < val_open or tsl < val_low):
            trades[-1]["Trade_LS"] = "Exit"
            trades[-1]["Exit_Date"] = ind_date[i].strftime("%Y-%m-%d")
            trades[-1]["Exit_Value"] = tsl
            fig.add_trace(go.Scatter(x=[ind_history[line].index[i]], y=[tsl], mode='markers', marker=dict(color='#000', size=12,line=dict(width=2, color='#c7c7c7')),showlegend=False, text=f"Action: Exit Sell<br>Exit Value: {tsl}<br>Date: {ind_date[i].strftime('%Y-%m-%d')}"))
            # fig.add_annotation(x = ind_history[line].index[i], y = tsl,ax = 20,ay= 50, text = "Exit<br>" + str(tsl), showarrow= True,arrowhead= 5,bordercolor="#c7c7c7", borderwidth=2, borderpad=4, bgcolor="#ff7f0e", opacity=0.8)              
        elif(buff_exit < val_high and prev_dict["Top"] and (entry_buff != exit_buff)):
            trades[-1]["Trade_LS"] = "Exit buffer triggered"  
            trades[-1]["Exit_Date"] = date_val.strftime("%Y-%m-%d")
            trades[-1]["Exit_Value"] = buff_exit
            fig.add_annotation(x = ind_history[line].index[i + days], y = buff_exit,ax = days,ay= 50, text = "Exit<br>" + str(tsl), showarrow= True,arrowhead= 5,bordercolor="#c7c7c7", borderwidth=2, borderpad=4, bgcolor="#ff7f0e", opacity=0.8)


excel_df = pd.DataFrame(columns=["Action","Trade_LS", "Entry_Date", "Prev_Top","Prev_Bottom", "Entry_Value", "Exit_Value", "Exit_Date","Profit_Loss", "Stop_Loss"])
def report():
    for i in range(1,len(trades)):
        try:
            if(trades[i-1]["Exit_Value"] == 0):
                trades[i-1]["Exit_Value"] = trades[i]["Entry_Value"]
                trades[i-1]["Exit_Date"] = trades[i]["Entry_Date"]
            if trades[i-1]["Action"] == "Buy":
                trades[i-1]["Profit_Loss"] = trades[i-1]["Exit_Value"] - trades[i-1]["Entry_Value"]
            else:
                trades[i-1]["Profit_Loss"] = trades[i-1]["Entry_Value"] - trades[i-1]["Exit_Value"]
        except:
            pass
    excel_df = pd.DataFrame()
    for i in trades:
        row = pd.DataFrame([i])
        excel_df = pd.concat([excel_df, row], ignore_index= True)
        
    print("\nexcel after appending:")
    print(excel_df)
    print("\n\n")
    excel_df.to_csv("reports/report.csv")

def complete(fig):
    print(trades)
    # print(prev_dict)
    report()
    fig.update_layout(xaxis_title='Dates', yaxis_title='Price')

    # fig.show()

def run(info):
    
    index = info[0]
    line = info[1]
    entry_buff = info[2]
    exit_buff = info[3]
    risk_percent = info[4]
    tsl_1 = info[5]
    tsl_2 = info[6]
    start_date = info[7]
    end_date = info[8]

    ind = yf.Ticker(index)
    ind_history = ind.history(start= start_date, end = end_date)
    #ind_history = ind.history(start= "2022-09-27", end = "2022-11-26")
    ind_date = pd.Index.tolist(ind_history[line].index)
    ind_vals = pd.Series.tolist(ind_history[line])

    print(ind_history)

    ind_open = pd.Series.tolist(ind_history['Open']) # open values
    ind_high = pd.Series.tolist(ind_history['High']) # high values
    ind_low = pd.Series.tolist(ind_history['Low'])# low values
    ind_close = pd.Series.tolist(ind_history['Close'])# close values

    ind_history = ind_history.drop(['Volume', 'Dividends', 'Stock Splits'],axis = 1)
    print(type(ind_history))
    
    candlestick_chart = go.Candlestick(x = ind_history[line].index, open = ind_history["Open"], high = ind_history["High"], low = ind_history["Low"], close = ind_history["Close"])
    line_chart = go.Scatter(x = ind_history[line].index, y = ind_history["Close"], mode='lines', line=dict(color='white', width=1))
    fig = go.Figure(data = [candlestick_chart, line_chart])

    # fig = px.line(ind_history, x = ind_history[line].index, y = [ind_history["Open"],ind_history["High"],ind_history["Low"],ind_history["Close"]])#.plot(label='Open')
    fig.update_yaxes(fixedrange=False)
    # fig.update_layout(xaxis_rangeslider_visible=False)
    print(fig.layout.xaxis.range)

        # print(ind_vals)
    for j in range(len(ind_vals)):
        #3. get entry date
        if(j < 3):
            prev_dict = prev_tb(j, fig, ind_vals, ind_date, ind_history, line)
        else:
            try:  
                trade(tsl_1, tsl_2, entry_buff, exit_buff, ind_vals[j+1],ind_open[j+1],ind_high[j+1],ind_low[j+1],ind_close[j+1], j+1, fig, prev_dict, ind_date, ind_history, line)
            except Exception as e:
                print(e) 

            prev_dict = prev_tb(j, fig, ind_vals, ind_date, ind_history, line)

    complete(fig)
    return fig
    
