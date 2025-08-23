from gemini import genai_client

response = genai_client.models.generate_content(
    model="gemini-2.5-flash-lite-preview-06-17",
    contents="告诉我夏天的感觉",
)

print(response.text)