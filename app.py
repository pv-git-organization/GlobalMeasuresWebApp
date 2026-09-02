import os
import mssql_python
import datetime
import json
from dotenv import load_dotenv
from azure.appconfiguration.provider import load
from azure.identity import ManagedIdentityCredential

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def execute_query(query, params=None):
    rows = []

    with mssql_python.connect(CONNECTION_STRING) as conn:
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return rows

@app.route('/')
def index():

    query = """
        SELECT
            Pillar,
            Measure,
            MeasureYear,
            ActualValue,
            TargetValue,
            GlobalMeasureID,
            MeasureSort,
            YearSort
        FROM dbo.GlobalMeasures
        ORDER BY MeasureSort, MeasureYear
    """

    rows = execute_query(query)

    return render_template('index.html', metrics_json=json.dumps(rows))

@app.route('/api/measures')
def api_measures():

    query = """
        SELECT
            Pillar,
            Measure,
            MeasureYear,
            ActualValue,
            TargetValue,
            GlobalMeasureID,
            MeasureSort,
            YearSort
        FROM dbo.GlobalMeasures
        ORDER BY MeasureSort, MeasureYear
    """

    return execute_query(query)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
