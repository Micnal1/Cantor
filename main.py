from flask import Flask, request, render_template
import requests, csv, math

app = Flask(__name__)


@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.form
        code = data.get('code')
        quantity = data.get('quantity')

        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
        data = response.json()
        kursy = data[0]['rates']

        with open("kursy.csv", 'w') as dict_csv:
            fieldnames = ['currency', 'code', 'bid', 'ask']
            writer = csv.DictWriter(dict_csv, fieldnames=fieldnames)

            writer.writeheader()
            for i in kursy:
                writer.writerow(i)

        with open("kursy.csv") as dict_reader:
            reader = csv.DictReader(dict_reader)

            for exchange_rate in reader:
                if exchange_rate['code'] == code:
                    break

            prize = '{:.2f}'.format(math.prod([float(quantity),float(exchange_rate['ask'])]))

        return f"Kupujesz {quantity} {exchange_rate['currency']} za {prize} złociszy!"

    return render_template("waluty.html")


if __name__ == "__main__":
    app.run(debug=True)
    pass
