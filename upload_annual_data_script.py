import sqlite3
import pandas as pd


def get_db_connection():
    conn = sqlite3.connect('well_data.db')
    conn.row_factory = sqlite3.Row  
    return conn



def load_data_from_xls(str_path):
    df = pd.read_excel(str_path)
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

    print('Data populated successfully')


if __name__ == '__main__':

    str_xls_path = '20210309_2020_1-4.xls'
    load_data_from_xls(str_xls_path)