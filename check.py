import duckdb

table = input("Which table do you want to check? ")
where = input("Any filter? (press Enter to skip) ")

con = duckdb.connect('/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db')

query = f'SELECT * FROM {table}'
if where:
    query += f' WHERE {where}'
query += ' LIMIT 5'

print(con.execute(query).fetchdf())