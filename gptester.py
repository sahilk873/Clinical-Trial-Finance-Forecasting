from openai import OpenAI
key = "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"
client = OpenAI(api_key = key)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response)
