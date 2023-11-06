import yfinance as yf
import pandas as pd

# import matplotlib.pyplot as plt
from datetime import datetime
import os
import csv
import plotly.express as px
import plotly.graph_objects as go

global sma
prev_hl = {"High": 0, "Low": 0}
sma = []
excel_df = pd.DataFrame(
    columns=[
        "Action",
        "Trade_LS",
        "Entry_Date",
        "SMA",
        "Entry_Value",
        "Exit_Value",
        "Exit_Date",
        "Profit_Loss",
        "Stop_Loss",
    ]
)
trades = []


def sma_calc(i, ind_vals, days):
    i = i + days - 1
    adder = 0
    for j in range(i, i - days, -1):
        adder = adder + ind_vals[j]

    sma.append(adder / days)


def flag(sma, val_close, val_high, val_low, candle):
    if (
        sma[-1] > val_close
    ):  # and candle == "Red") or (sma[-1] >= val_low and sma[-1] >= val_high)): #
        prev_hl["Low"] = val_low
        return "Sell"
    if (
        sma[-1] < val_close
    ):  # and candle == "Green") or (sma[-1] <= val_low and sma[-1] <= val_high)):
        prev_hl["High"] = val_high
        return "Buy"


def trade(
    fig,
    entry_buff,
    exit_buff,
    i,
    action,
    open_val,
    high_val,
    low_val,
    close_val,
    date_val,
    candle,
    ind_history,
    line,
    days,
    msl,
    bep,
):
    buff_high = prev_hl["High"] * entry_buff * 0.01  # buffer to exeute buy
    buff_low = prev_hl["Low"] * entry_buff * 0.01  # buffer to execute sell
    buffer_high = prev_hl["High"] + buff_high  # top + buffer
    buffer_low = prev_hl["Low"] - buff_low  # bottom - buffer

    try:
        if trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short":
            trade_exit(
                fig,
                entry_buff,
                exit_buff,
                trades,
                open_val,
                close_val,
                high_val,
                low_val,
                date_val,
                candle,
                i,
                ind_history,
                line,
                days,
            )
    except:
        pass

    try:
        # print(action)
        if action == "Buy":
            # print("Entered buy")
            if (
                (trades)
                and trades[-1]["Action"] == "Buy"
                and trades[-1]["Trade_LS"] != "Exit"
            ):
                # print("Hold")
                pass
            else:
                if high_val > buffer_high:
                    Buy(
                        fig,
                        buffer_high,
                        open_val,
                        high_val,
                        low_val,
                        date_val,
                        i,
                        ind_history,
                        line,
                        days,
                        msl,
                    )

        if (
            (trades)
            and trades[-1]["Action"] == "Buy"
            and trades[-1]["Trade_LS"] == "Long"
        ):
            buy = trades[-1]["Entry_Value"]
            sl = trades[-1]["Stop_Loss"]
            if sl == buy and bep == "yes":
                pass
            print("SMA = ", sma[-1], "SL = ", sl)
            if buy <= sma[-1]:
                sl = sma[-1]
                trades[-1]["Stop_Loss"] = sl
                print("passed sma for buy")
            if sl != buy and sl != sma[-1] and bep == "yes":
                threshold = buy + (buy * msl * 0.01)
                if high_val >= threshold:
                    sl = buy
                trades[-1]["Stop_Loss"] = sl

        if (
            (trades)
            and trades[-1]["Action"] == "Buy"
            and trades[-1]["Trade_LS"] == "Long"
        ):
            trade_exit(
                fig,
                entry_buff,
                exit_buff,
                trades,
                open_val,
                close_val,
                high_val,
                low_val,
                date_val,
                candle,
                i,
                ind_history,
                line,
                days,
            )

        if action == "Sell":
            if (
                (trades)
                and trades[-1]["Action"] == "Sell"
                and trades[-1]["Trade_LS"] != "Exit"
            ):
                # print("Hold")
                pass
            else:
                if low_val < buffer_low:
                    Sell(
                        fig,
                        buffer_low,
                        open_val,
                        low_val,
                        high_val,
                        date_val,
                        i,
                        ind_history,
                        line,
                        days,
                        msl,
                    )

        if (
            (trades)
            and trades[-1]["Action"] == "Sell"
            and trades[-1]["Trade_LS"] == "Short"
        ):
            sell = trades[-1]["Entry_Value"]
            sl = trades[-1]["Stop_Loss"]
            if sl == sell and bep == "yes":
                pass
            print("SMA = ", sma[-1], "SL = ", sl)
            if sell >= sma[-1]:
                sl = sma[-1]
                print("passed sma for buy")
                trades[-1]["Stop_Loss"] = sl

            if sl != sell and sl != sma[-1] and bep == "yes":
                threshold = sell - (sell * msl * 0.01)
                if low_val <= threshold:
                    sl = buy
                trades[-1]["Stop_Loss"] = sl

        if (
            (trades)
            and trades[-1]["Action"] == "Sell"
            and trades[-1]["Trade_LS"] == "Short"
        ):
            trade_exit(
                fig,
                entry_buff,
                exit_buff,
                trades,
                open_val,
                close_val,
                high_val,
                low_val,
                date_val,
                candle,
                i,
                ind_history,
                line,
                days,
            )

    except Exception as e:
        print(e)


def Buy(
    fig, buy_val, val_open, val_high, val_low, date_val, i, ind_history, line, days, msl
):
    print("Entered buy")
    buy = buy_val
    if buy < val_low:
        buy = val_open
    sl = buy - (buy * msl * 0.01)
    trades.append(
        {
            "Action": "Buy",
            "Trade_LS": "Long",
            "Entry_Date": date_val.strftime("%Y-%m-%d"),
            "SMA": sma[-1],
            "Entry_Value": buy,
            "Exit_Value": 0,
            "Exit_Date": 0,
            "Profit_Loss": 0,
            "Stop_Loss": sl,
        }
    )
    fig.add_annotation(
        x=ind_history[line].index[i + days],
        y=buy,
        ax=20,
        ay=50,
        text="Buy<br>" + str(buy),
        showarrow=True,
        arrowhead=5,
    )


def Sell(
    fig,
    sell_val,
    val_open,
    val_low,
    val_high,
    date_val,
    i,
    ind_history,
    line,
    days,
    msl,
):
    print("Entered Sell")
    sell = sell_val
    if sell > val_high:
        sell = val_open
    sl = sell + (sell * msl * 0.01)
    trades.append(
        {
            "Action": "Sell",
            "Trade_LS": "Short",
            "Entry_Date": date_val.strftime("%Y-%m-%d"),
            "SMA": sma[-1],
            "Entry_Value": sell,
            "Exit_Value": 0,
            "Exit_Date": 0,
            "Profit_Loss": 0,
            "Stop_Loss": sl,
        }
    )
    fig.add_annotation(
        x=ind_history[line].index[i + days],
        y=sell,
        ax=20,
        ay=50,
        text="Sell<br>" + str(sell),
        showarrow=True,
        arrowhead=5,
    )


def trade_exit(
    fig,
    entry_buff,
    exit_buff,
    trades,
    val_open,
    val_close,
    val_high,
    val_low,
    date_val,
    candle,
    i,
    ind_history,
    line,
    days,
):
    try:
        sl = trades[-1]["Stop_Loss"]

        # print(f"sl = {sl}, date = {date_val.strftime('%Y-%m-%d')}")
        # print(trades[-1]["Action"], trades[-1]["Trade_LS"])
        if (
            trades[-1]["Action"] == "Buy" and trades[-1]["Trade_LS"] == "Long"
        ):  # and (val_open > val_close)#
            buff_exit = prev_hl["Low"] - (prev_hl["Low"] * exit_buff * 0.01)
            if sl > val_open or sl > val_low or sl > val_high or sl > val_close:
                if sl > val_high:
                    sl = val_open
                trades[-1]["Trade_LS"] = "Stop Loss triggered"
                trades[-1]["Exit_Date"] = date_val.strftime("%Y-%m-%d")
                trades[-1]["Exit_Value"] = sl
                fig.add_annotation(
                    x=ind_history[line].index[i + days],
                    y=sl,
                    ax=20,
                    ay=50,
                    text="Exit<br>" + str(sl),
                    showarrow=True,
                    arrowhead=5,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="#ff7f0e",
                    opacity=0.8,
                )

            elif buff_exit > val_low and prev_hl["Low"] and (entry_buff != exit_buff):
                if buff_exit > val_high:
                    buff_exit = val_open
                print("val_low = ", val_low, "Buffer exit = ", buff_exit)
                trades[-1]["Trade_LS"] = "Exit buffer triggered"
                trades[-1]["Exit_Date"] = date_val.strftime("%Y-%m-%d")
                trades[-1]["Exit_Value"] = buff_exit
                fig.add_annotation(
                    x=ind_history[line].index[i + days],
                    y=buff_exit,
                    ax=20,
                    ay=50,
                    text="Exit<br>" + str(sl),
                    showarrow=True,
                    arrowhead=5,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="#ff7f0e",
                    opacity=0.8,
                )

        if (
            trades[-1]["Action"] == "Sell" and trades[-1]["Trade_LS"] == "Short"
        ):  # and (val_open < val_close)
            print("Entered sell Exit")
            buff_exit = prev_hl["High"] + (prev_hl["High"] * exit_buff * 0.01)
            if sl < val_close or sl < val_high or sl < val_open or sl < val_low:
                if sl < val_low:
                    sl = val_open
                trades[-1]["Trade_LS"] = "Exit"
                trades[-1]["Exit_Date"] = date_val.strftime("%Y-%m-%d")
                trades[-1]["Exit_Value"] = sl
                fig.add_annotation(
                    x=ind_history[line].index[i + days],
                    y=sl,
                    ax=20,
                    ay=50,
                    text="Exit<br>" + str(sl),
                    showarrow=True,
                    arrowhead=5,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="#ff7f0e",
                    opacity=0.8,
                )

            elif buff_exit < val_high and prev_hl["High"] and (entry_buff != exit_buff):
                if buff_exit < val_low:
                    buff_exit = val_open
                trades[-1]["Trade_LS"] = "Exit buffer triggered"
                trades[-1]["Exit_Date"] = date_val.strftime("%Y-%m-%d")
                trades[-1]["Exit_Value"] = buff_exit
                fig.add_annotation(
                    x=ind_history[line].index[i + days],
                    y=buff_exit,
                    ax=20,
                    ay=50,
                    text="Exit<br>" + str(sl),
                    showarrow=True,
                    arrowhead=5,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="#ff7f0e",
                    opacity=0.8,
                )

    except:
        pass


def report():
    for i in range(1, len(trades)):
        try:
            if trades[i - 1]["Exit_Value"] == 0:
                trades[i - 1]["Exit_Value"] = trades[i]["Entry_Value"]
                trades[i - 1]["Exit_Date"] = trades[i]["Entry_Date"]
            if trades[i - 1]["Action"] == "Buy":
                trades[i - 1]["Profit_Loss"] = (
                    trades[i - 1]["Exit_Value"] - trades[i - 1]["Entry_Value"]
                )
            else:
                trades[i - 1]["Profit_Loss"] = (
                    trades[i - 1]["Entry_Value"] - trades[i - 1]["Exit_Value"]
                )
        except:
            pass
    excel_df = pd.DataFrame()
    for i in trades:
        row = pd.DataFrame([i])
        excel_df = pd.concat([excel_df, row], ignore_index=True)

    print("\nexcel after appending:")
    print(excel_df)
    print("\n\n")

    # try:
    #     os.remove("reports/report.csv")
    # except:
    #     pass
    # with open("reports/report.csv", 'w', newline='') as csvfile:
    # # Create a CSV writer object
    #     csv_writer = csv.writer(csvfile)

    #     # Write the header row
    #     csv_writer.writerow(excel_df.columns)

    #     # Write the data rows
    #     for _, row in excel_df.iterrows():
    #         csv_writer.writerow(row)
    return excel_df


def run(info):
    index = info[0]
    line = info[1]
    entry_buff = info[2]
    exit_buff = info[3]
    days = info[4]
    msl = info[5]
    bep = info[6]
    start_date = info[7]
    end_date = info[8]

    ind = yf.Ticker(index)
    ind_history = ind.history(start=start_date, end=end_date)
    # ind_history = ind.history(start= "2022-09-27", end = "2022-11-26")
    ind_date = pd.Index.tolist(ind_history[line].index)
    ind_vals = pd.Series.tolist(ind_history[line])

    print(ind_history)

    ind_open_or = pd.Series.tolist(ind_history["Open"])  # open values
    ind_high_or = pd.Series.tolist(ind_history["High"])  # high values
    ind_low_or = pd.Series.tolist(ind_history["Low"])  # low values
    ind_close_or = pd.Series.tolist(ind_history["Close"])  # close values

    ind_date = ind_date[days:]
    ind_open = ind_open_or[days:]
    ind_high = ind_high_or[days:]
    ind_low = ind_low_or[days:]
    ind_close = ind_close_or[days:]

    # ind_history = ind_history.drop(['Volume', 'Dividends', 'Stock Splits'],axis = 1)
    print(type(ind_history))
    # fig = px.line(ind_history, x = ind_history[line].index, y = [ind_history["Open"],ind_history["High"],ind_history["Low"],ind_history["Close"]])#.plot(label='Open')
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=ind_date, open=ind_open, high=ind_high, low=ind_low, close=ind_close
            )
        ]
    )
    # print(fig.layout.xaxis.range)

    for i in range(0, len(ind_open)):
        try:
            candle = "None"
            if ind_open[i] > ind_close[i]:
                candle = "Red"
            else:
                candle = "Green"
            sma_calc(i, ind_vals, days)
            action = flag(sma, ind_close[i], ind_high[i], ind_low[i], candle)
            trade(
                fig,
                entry_buff,
                exit_buff,
                i + 1,
                action,
                ind_open[i + 1],
                ind_high[i + 1],
                ind_low[i + 1],
                ind_close[i + 1],
                ind_date[i + 1],
                candle,
                ind_history,
                line,
                days,
                msl,
                bep,
            )

        except Exception as e:
            print("Caught in for loop ", e)

    fig.add_trace(go.Scatter(x=ind_date, y=sma, line=dict(color="#0000ff")))
    # print(trades )
    excel_df = report()
    return excel_df
