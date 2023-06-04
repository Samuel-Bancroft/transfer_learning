removed =['word', 'sam']
converted = ['word','sam','max']

for column in converted[:]:
    if column in removed:
        converted.remove(column)

