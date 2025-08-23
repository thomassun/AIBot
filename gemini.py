from google import genai
from google.genai import types
import asyncio

genai_client = genai.Client(api_key="AIzaSyB_eFBnC_TcLQ6ByXV5sk3ND4yR21jB7wM")
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}
tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])


async def tts_async(text: str) -> bytes:
    loop = asyncio.get_running_loop()
    client = genai.Client()
    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
            )
        ),
    )
    response = await loop.run_in_executor(
        None,
        lambda: client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=config,
        ),
    )
    return response.candidates[0].content.parts[0].inline_data.data
