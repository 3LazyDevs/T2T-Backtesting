from flask import Flask, render_template, request
import plotly.express as px
import RTT_1 as rtt
# import AB20 as ab20

app = Flask(__name__)

lines = ['Open','Close', 'High', 'Low']
systems = {1:'RTT', 2:'20 Akasha Bhumi', 3:'Highs Lows'}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        system = request.form.get('system')
        plot_div = ""

        match system:
            case "1":
                scripcode = request.form.get('scripcode')
                start_date = request.form.get('start_date')
                end_date = request.form.get('end_date')
                entry_buffer = float(request.form.get('entry_buffer'))
                exit_buffer = float(request.form.get('exit_buffer'))
                msl = float(request.form.get('msl'))
                tsl1 = float(request.form.get('tsl1'))
                tsl2 = float(request.form.get('tsl2'))

                
                info = [scripcode, "Close", entry_buffer, exit_buffer, msl, tsl1, tsl2, start_date, end_date]
                info = tuple(info)
                fig = rtt.run(info)

                fig.update_layout(plot_bgcolor='#27293d')
                fig.update_layout(paper_bgcolor='#27293d')
                fig.update_layout(font_color='#ffffff')
                        # Convert the Plotly chart to HTML
                plot_div = fig.to_html(full_html=False)

            # case "2":
            #     scripcode = request.args.get('scripcode')
            #     start_date = request.args.get('start_date')
            #     end_date = request.args.get('end_date')
            #     entry_buffer = float(request.args.get('entry_buffer'))
            #     exit_buffer = float(request.args.get('exit_buffer'))
            #     msl = float(request.args.get('msl'))
            #     bep = request.args.get('bep')

            #     info = [scripcode, "Close", entry_buffer, exit_buffer, " ", msl, bep, start_date, end_date]
            #     info = tuple(info)
            #     fig = ab20.run(info)


                # info.append(int(input("Enter the value to be considered for simple moving averages ")))

                return render_template('index.html', plot_div=plot_div, lines=lines, systems = systems)
            case _ :
                return "FAIL"
            


    return render_template('index.html', lines=lines, systems = systems)



if __name__ == '__main__':
    app.run(debug=True)
 
