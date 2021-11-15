import pandas

queries = pandas.read_csv('search_history.csv')
popularities = pandas.read_csv('query_popularity.csv')


# query принимаем в качестве аргумента
query = ''

"""
Эта часть кода по сути делает то же, что сделал бы примерно такой SQL запрос

SELECT UQ, cnt, populatiry from popularities
JOIN queries on UQ = UQ
where UQ.Contain(query)
ORDER BY (cnt * popularity)

+ убирает одинаковые запросы, оставляя тот, где cnt оказался наибольшим

такое по сути должно уже максимально эффективно быть реализовано в СУБД,
а потому мы не сильно парились над оптимизацией этой части
"""

table = pandas.merge(popularities, queries.rename(columns={"UQ": "query"}), on="query")
table = table[table['query'].str.find(query) != -1].dropna()
table["cnt*query_popularity"] = table["cnt"] * table["query_popularity"]
table = table.sort_values(by="cnt*query_popularity", ascending=False)
table = table.drop_duplicates(subset=['query'], keep="first")


"""
этот чанк кода делает:

проверяет все слова из подходящих нам запросов
в случае, если последнее слово запроса неокончено, составляет массив из 10 наиболее вероятных слов,
которым может быть неоконченное слово пользователя
в случае, если последнее слово запроса закончено, составляет массив из 10 наиболее вероятных слов,
которые могут уточнить запрос пользователя

пример:
ввод: тру
в Hints могли бы быть: трус, трусы, труба

ввод: трусы
в Hints могли бы быть: мужские, зеленые, боксеры
"""
endsWithSpace = query[len(query) - 1] == ' '
Hints = []
tquery = query.split()
for i in range(0, len(table)):
    if len(Hints) > 9:
        break
    words = table.iloc[i]['query'].split()
    added = False
    for word in words:
        if added:
            break
        if word not in tquery:
            if  not endsWithSpace and len(Hints) < 10 and word not in Hints:
                for q in tquery:
                    if word.find(q) == 0:
                        Hints.append(word)
                        added = True
                        break
            elif len(Hints) < 10 and word not in Hints:
                Hints.append(word)
                added = True
print(Hints)