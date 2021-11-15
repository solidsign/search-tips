import pandas

queries = pandas.read_csv('search_history.csv')
popularities = pandas.read_csv('query_popularity.csv')
print(queries)
queries_group = queries.groupby(queries['wbuser_id'].tolist(),as_index=False).size() #объединение запросов от одниаковых пользователей  с подсчетом их количество
queries = queries.dropna().loc[queries['cnt'] != 0] # проверка на ошибки запросов
filter_queries = queries_group['size'] > 100 # фильтрация количество сообщений от одного пользователя !!доделать! среднее значения и сравнивать относительного него)
queries_group = queries_group.loc[filter_queries]
print(queries_group)

spammers = queries_group['index'].to_list()
length = len(spammers)
for i in range(length): # из исходных данных убираем подозрительные аккаунты
    queries = queries.loc[queries['wbuser_id'] != spammers[i]]
print(queries)
queries_group.to_csv('new_search_history.csv', sep ='\t') #создание отфильтрованного документа
