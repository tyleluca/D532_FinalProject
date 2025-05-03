import pandas as pd
import psycopg2

def upload_to_db(df, table_name, conn):
    cursor = conn.cursor()

    for index, row in df.iterrows():
        columns = ', '.join([f'"{col}"' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(row))
        values = tuple(None if pd.isna(value) else value for value in tuple(row))
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_sql, values)

    conn.commit()
    print(f"Uploaded data to '{table_name}'")

def run_local_upload():
    local_file_path = 'C:/Users/tyler/Documents/AppliedDatabaseTechnologies/coffee_shop_sales.xlsx'
    coffee_df = pd.read_excel(local_file_path)
    coffee_df['transactionDatetime'] = pd.to_datetime(coffee_df['transactionDate'].astype(str) + ' ' + coffee_df['transactionTime'].astype(str))
    coffee_df.drop(['transactionDate', 'transactionTime'], axis=1, inplace=True)  

    transaction_df = coffee_df[['transactionId', 'transactionQty', 'transactionDatetime', 'storeId', 'productId', 'unitPrice']].sort_values(by='transactionId')
    store_df = coffee_df[['storeId', 'storeLocation']].drop_duplicates().sort_values(by='storeId')
    product_df = coffee_df[['productId', 'productCategory', 'productType', 'productDetail']].drop_duplicates().sort_values(by='productId')

    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        dbname='x'
        user="y",
        password="z"
    )

    if conn:
        upload_to_db(store_df, 'store', conn)
        upload_to_db(product_df, 'product', conn)
        upload_to_db(transaction_df, 'transaction', conn)
        conn.close()
        print("All data uploaded successfully!")

if __name__ == "__main__":
    run_local_upload()

