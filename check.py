import duckdb                                                                                                                                            
                  
table = input("Which table do you want to check? ")                                                                                                      
                  
con = duckdb.connect('/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db')
print(con.execute(f'SELECT * FROM {table} LIMIT 5').fetchdf())