import io
import pandas as pd
import duckdb

con = duckdb.connect(database='data/exercise_sql_tables.duckdb', read_only=False)

#EXERCISE LIST
data = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "size_and_trademarks"],
    "tables": [["beverages","food_items"],["sizes", "trademarks"]],
    "last_reviewed": ["1980-01-01","1970-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.register('memory_state_df',memory_state_df)
con.execute("DROP TABLE IF EXISTS memory_state")
con.execute("CREATE TABLE memory_state AS SELECT * FROM memory_state_df")


# CROSS JOIN
CSV = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(CSV))
con.register('beverages_tmp',beverages)
con.execute("DROP TABLE IF EXISTS beverages")
con.execute('CREATE TABLE beverages AS SELECT * FROM beverages_tmp')

CSV2 = '''
food_tem,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(CSV2))
con.register('food_items_tmp',food_items)
con.execute("DROP TABLE IF EXISTS food_items")
con.execute('CREATE TABLE food_items AS SELECT * FROM food_items_tmp')

# CROSS JOIN - size & marks
sizes = '''
size
XS
M
L
XL
'''
sizes = pd.read_csv(io.StringIO(sizes))
con.register('sizes_tmp',sizes)
con.execute("DROP TABLE IF EXISTS sizes")
con.execute('CREATE TABLE sizes AS SELECT * FROM sizes_tmp')

trademarks = '''
trademark
Nike
Asphalte
Abercrombie
Lewis
'''
trademarks = pd.read_csv(io.StringIO(trademarks))
con.register('trademarks_tmp',trademarks)
con.execute("DROP TABLE IF EXISTS trademarks")
con.execute('CREATE TABLE trademarks AS SELECT * FROM trademarks_tmp')
