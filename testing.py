import polars

q = (polars.scan_csv('new_train.csv').filter(polars.col('age') > 50).groupby('age').agg(polars.all().sum()))

df = q.collect()
print(df)