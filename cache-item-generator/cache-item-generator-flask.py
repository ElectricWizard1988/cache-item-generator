from flask import Flask, render_template, request
from datetime import datetime, timezone

app = Flask(__name__)


def generate_cache(imei, supplier):
    # Get Date
    now = datetime.now(timezone.utc)
    formatted_date = now.strftime('%a %b %d %Y %H:%M:%S GMT%z')
    formatted_date = formatted_date[:-2] + formatted_date[-2:].rjust(5, '0')

    if supplier == "teltonika":
        return f'set {supplier}-last-{imei} "{{\\"IMEI\\":\\"{imei}\\",\\"Recieved\\":\\"{formatted_date}\\"}}"'
    else:
        return f'set {supplier}-last-{imei} "{{\\"IMEI\\":\\"{imei}\\",\\"Recieved\\":\\"{formatted_date}\\",\\"LastProtocol\\":\\"GTLBS\\""}}'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        supplier_input = request.form['supplier']
        imei_input = request.form['imei']

        if supplier_input not in ["teltonika", "queclink"]:
            return "Invalid supplier selected"

        result = generate_cache(imei_input, supplier_input)
        return render_template('index.html', result=result)

    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(debug=True)