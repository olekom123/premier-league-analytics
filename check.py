import duckdb

table = input("Which table do you want to check? ")
where = input("Which season? Ex value format '2425' (press Enter to skip) ")

con = duckdb.connect('/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db')

query = f'SELECT * FROM {table}'
if where:
    query += f' WHERE season = {where}'
query += ' LIMIT 5'

print(con.execute(query).fetchdf())