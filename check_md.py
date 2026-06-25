import duckdb

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFuaHBwdjIzNDA2QHN0LnVlbC5lZHUudm4iLCJtZFJlZ2lvbiI6ImF3cy11cy1lYXN0LTEiLCJzZXNzaW9uIjoiYW5ocHB2MjM0MDYuc3QudWVsLmVkdS52biIsInBhdCI6IjVFZEVSNzlZZFpjN2FST1ROSkdTTUlPOHpqTkZfcWV3MzNUaks1bXRnQ3ciLCJ1c2VySWQiOiJkZTIzN2EzMS0yMTg5LTRkNWYtYmIwYS0zZjQ5MzgzOTExOTEiLCJpc3MiOiJtZF9wYXQiLCJyZWFkT25seSI6ZmFsc2UsInRva2VuVHlwZSI6InJlYWRfd3JpdGUiLCJpYXQiOjE3ODIzMTMzNzd9.7g-rGoWNcYNXUEGU5tileJWrBtnGXDlghTtiisqY_eg"
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
