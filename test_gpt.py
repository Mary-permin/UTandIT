from g4f.client import Client


def info_wolfram(query):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content


print(info_wolfram("Я очень добрый и всегда всем помогаю. На какого персонажа я похож?"))

