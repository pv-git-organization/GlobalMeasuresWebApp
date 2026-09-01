import os
import mssql_python
from dotenv import load_dotenv

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def execute_query(query=None):
    query = """
        SELECT *
        FROM [dbo].[GlobalMeasures]
        Where MeasureYear = '2026'
        AND Pillar = 'Top Safety Performance'
        AND Measure = 'Days Away Restricted Transferred (DART)'
    """

    rows = []

    with mssql_python.connect(CONNECTION_STRING) as conn:
        cursor = conn.cursor()
        # Replace with your real query. Use parameters (cursor.execute(sql, params))
        # for anything derived from the request instead of string-formatting it in.
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(rows)

    return rows
 

 

@app.route('/')
def index():

    rows = execute_query()
    actual_value = rows[0].get("ActualValue")
   
    print('Request for index page received')
    return render_template('index.html', actual_value=actual_value)

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
