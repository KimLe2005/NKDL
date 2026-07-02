import duckdb

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBodW9uZ2R0MjM0MDZAc3QudWVsLmVkdS52biIsIm1kUmVnaW9uIjoiYXdzLXVzLWVhc3QtMSIsInNlc3Npb24iOiJwaHVvbmdkdDIzNDA2LnN0LnVlbC5lZHUudm4iLCJwYXQiOiJjY0ZXTUV3RUJMS1B5eHZwWU1rQkVudk04R0Q5MGF2aWI4OW1RVkd5Vlp3IiwidXNlcklkIjoiOWRjYzQwMWMtZjdlNC00MWQ0LTkwMjAtMzA0ZmUzMTY0YmY0IiwiaXNzIjoibWRfcGF0IiwicmVhZE9ubHkiOmZhbHNlLCJ0b2tlblR5cGUiOiJyZWFkX3dyaXRlIiwiaWF0IjoxNzgxOTM2NTcxfQ.DYWM4ZniVCR3U4u9oALHFMTfQhSU-oDqIR-i5v2Y26w"
try:
    con = duckdb.connect(f"md:?motherduck_token={token}")
    print("DATABASES:")
    dbs = con.execute("SHOW DATABASES").fetchall()
    print(dbs)
    for db in dbs:
        db_name = db[0]
        print(f"\nTABLES in {db_name}:")
        try:
            tables = con.execute(f"SHOW TABLES FROM {db_name}").fetchall()
            for table in tables:
                table_name = table[0]
                print(f" - {table_name}")
                print(f"   Schema of {table_name}:")
                schema = con.execute(f"DESCRIBE {db_name}.main.{table_name}").fetchall()
                for col in schema:
                    print(f"     {col[0]}: {col[1]}")
        except Exception as e:
            print(f"Error accessing tables in {db_name}: {e}")
except Exception as e:
    print(f"Connection error: {e}")
