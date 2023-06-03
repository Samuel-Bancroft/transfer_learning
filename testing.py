import polars

q = (polars.scan_csv('new_train.csv').filter(polars.col('age') > 50).groupby('age').agg(polars.all().sum()))

df = q.collect()
print(df)

if df.isnull().values.ravel().sum() > 0:
    csv_file_dropna = csv_file.dropna()
    if count <= 3:
        count += 1
        check_file(obj=obj, csv_file=csv_file, count=count)