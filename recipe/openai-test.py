from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a recipe expert. Given any list of ingredients, you are able suggest delicious food recipes."},
    {"role": "user", "content": "Using the following ingredients: chicken breast, cheese, bread, mayonaise, tomatos, cheese; provide a list of 5 recipes of different types that I can make at home"}
  ]
)

print(completion.choices[0].message)