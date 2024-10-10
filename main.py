import sqlite3
import pandas as pd
from flask import Flask, request, jsonify


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('well_data.db')
    conn.row_factory = sqlite3.Row  
    return conn


@app.route('/insert_data', methods=['GET'])
def load_data_from_xls():
    df = pd.read_excel('20210309_2020_1-4.xls')
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS annual_production (
            pk_bint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vchr_well_number varcahr(250),
            dbl_oil decimal(10,2),
            dbl_gas decimal(10,2),
            dbl_brine decimal(10,2)
        )
    ''')


    dct_annual_data = {}

    for index, row in df.iterrows():

        if row.get('API WELL  NUMBER') in dct_annual_data:

            str_well_no = row.get('API WELL  NUMBER')
            dct_annual_data[str_well_no]['OIL'] += row.get('OIL') 
            dct_annual_data[str_well_no]['GAS'] += row.get('GAS') 
            dct_annual_data[str_well_no]['BRINE'] += row.get('BRINE') 
        else:
            str_well_no = row.get('API WELL  NUMBER')
            dct_annual_data[str_well_no] = {}
            dct_annual_data[str_well_no]['OIL'] = row.get('OIL') 
            dct_annual_data[str_well_no]['GAS'] = row.get('GAS') 
            dct_annual_data[str_well_no]['BRINE'] = row.get('BRINE') 

    data_to_insert = [(well_number, data['OIL'], data['GAS'], data['BRINE']) for well_number, data in dct_annual_data.items()]

    c.executemany('''
        INSERT OR REPLACE INTO annual_production (vchr_well_number, dbl_oil, dbl_gas, dbl_brine)
        VALUES (?, ?, ?, ?)
    ''', data_to_insert)

    conn.commit()
    conn.close()

    return jsonify({'Message': 'Data populated successfully'})

# API for fetching data based on well number
@app.route('/data', methods=['GET'])
def get_annual_data():

    well_number = request.args.get('well')

    if not well_number:
        return jsonify({"error": "well number is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''SELECT dbl_oil, dbl_gas, dbl_brine FROM annual_production WHERE vchr_well_number = '''+str(well_number))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "well number not found"}), 404

    return jsonify({
        "oil": row['dbl_oil'],
        "gas": row['dbl_gas'],
        "brine": row['dbl_brine']
    })

   

if __name__ == '__main__':

    app.run(port=8080, debug=True)

    