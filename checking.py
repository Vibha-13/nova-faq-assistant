from openai import OpenAI

client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxx")

models = client.models.list()
print(models)
