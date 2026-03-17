import duckdb

table = input("Which table do you want to check? ")
where = input("Any filter? (press Enter to skip) ")

con = duckdb.connect('/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db')

order_by = input("Order by column? (press Enter to skip) ")

query = f'SELECT * FROM {table}'
if where:
    query += f' WHERE {where}'
if order_by:
    query += f' ORDER BY {order_by} DESC'
query += ' LIMIT 5'

print(con.execute(query).fetchdf())