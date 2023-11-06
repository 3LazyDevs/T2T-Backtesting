from flask import (
    Flask,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
)
import plotly.express as px
import pandas as pd
import os
import csv
import futures as fut
from json import dumps
import RTT_1 as rtt
import AB20 as ab20

app = Flask(__name__)


lines = ["Open", "Close", "High", "Low"]
systems = {1: "RTT", 2: "Akasha Bhumi", 3: "Highs Lows"}
criteria = ["2 Days", "3 Days", "4 Days", "1 Week", "2 Weeks"]


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        system = request.form.get("system")

        if system == "1":
            scripcode = request.form.get("scripcode")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            entry_buffer = float(request.form.get("entry_buffer"))
            exit_buffer = float(request.form.get("exit_buffer"))
            # msl = float(request.form.get("msl"))
            tsl1 = float(request.form.get("tsl1"))
            tsl2 = float(request.form.get("tsl2"))

            info = [
                scripcode,
                "Close",
                entry_buffer,
                exit_buffer,
                "5",
                tsl1,
                tsl2,
                start_date,
                end_date,
            ]
            info = tuple(info)
            excel_df = rtt.run(info)
            # fig.update_layout(plot_bgcolor='#27293d')
            # fig.update_layout(paper_bgcolor='#27293d')
            # fig.update_layout(font_color='#ffffff')
            # plot_div = excel_df.to_html()

            # with open("reports/report.csv", "r") as file:
            #     csv_reader = csv.reader(file)
            #     data = list(csv_reader)

            return render_template(
                "index.html",
                data=None,
                lines=lines,
                systems=systems,
                downflag=True,
            )

        elif system == "2":
            scripcode = request.form.get("scripcode")
            scripcode = scripcode.split()[0]
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            entry_buffer = float(request.form.get("entry_buffer"))
            exit_buffer = float(request.form.get("exit_buffer"))
            days = int(request.form.get("days"))
            msl = float(request.form.get("msl"))
            bep = request.form.get("bep")

            info = [
                scripcode,
                "Close",
                entry_buffer,
                exit_buffer,
                days,
                msl,
                bep,
                start_date,
                end_date,
            ]
            info = tuple(info)
            excel_df = ab20.run(info)

            excel_df.to_csv("reports/report.csv")

            # with open("reports/report.csv", "r") as file:
            #     csv_reader = csv.reader(file)
            #     data = list(csv_reader)

            return render_template(
                "index.html", data=None, lines=lines, systems=systems, downflag=True
            )

        elif system == "3":
            return render_template(
                "index.html",
                data=None,
                lines=lines,
                systems=systems,
                downflag=True,
                criteria=criteria,
            )
        else:
            return "FAIL"

    return render_template(
        "index.html",
        data=None,
        lines=lines,
        systems=systems,
        downflag=False,
    )


@app.route("/getPlotCSV")
def getPlotCSV():
    try:
        # Read the CSV file content as a string
        with open("reports/report.csv", "r") as fp:
            csv_content = fp.read()

        # Send the CSV file as a response
        response = send_file(
            "reports/report.csv",
            mimetype="text/csv",
            as_attachment=True,
            download_name="myplot.csv",
        )

        return response

    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for("index"))


@app.route("/getSuggestions")
def get_suggestions():
    # Get the user input from the query parameters
    user_input = request.args.get("input")
    options = fut.get_all_symbols_list()

    # Filter suggestions from the 'options' list based on user input
    suggestions = [option for option in options if user_input.lower() in option.lower()]

    # Return the suggestions as a JSON response
    return dumps(suggestions)


if __name__ == "__main__":
    app.run(debug=True)
