from flask import Flask
from flask import json
from flask import render_template

from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    proxima_fecha = None

    with open('fechas.json', 'r') as f:
        fechas = json.loads(f.read())
        for fecha in fechas:
            try:
                hasta = datetime.strptime(fecha['hasta'], '%Y-%m-%d')
            except ValueError:
                pass
            else:
                quien = fecha['quien']
                que = fecha['que']

                if proxima_fecha is None:
                    if hasta > datetime.today():
                        proxima_fecha = dict(hasta=hasta, quien=quien, que=que)
                elif hasta == proxima_fecha['hasta']:
                    proxima_fecha['quien2'] = fecha['quien']
                    proxima_fecha['que2'] = fecha['que']

    hace_dias = (datetime.today() - datetime(2017, 7, 12)).days
    en_dias = (proxima_fecha['hasta'] - datetime.today()).days
    quien = proxima_fecha['quien']
    que = proxima_fecha['que']
    quien2 = proxima_fecha.get('quien2')
    que2 = proxima_fecha.get('que2')
    return render_template('index.html', hace_dias=hace_dias, en_dias=en_dias, quien=quien, que=que, quien2=quien2, que2=que2)


@app.route('/fechas-pasadas')
def get_fechas_pasadas():
    fechas_pasadas = []
    with open('fechas.json', 'r') as f:
        fechas = json.loads(f.read())
        for fecha in fechas:
            try:
                hasta = datetime.strptime(fecha['hasta'], '%Y-%m-%d')
            except ValueError:
                pass
            else:
                quien = fecha['quien']
                que = fecha['que']
            if hasta < datetime.now():
                fechas_pasadas.append(dict(hasta=hasta.strftime('%d %b %Y'), quien=quien, que=que))
        return render_template('fechas_pasadas.html', fechas_pasadas=fechas_pasadas)


if __name__ == "__main__":
    app.run(host='127.0.0.1')

