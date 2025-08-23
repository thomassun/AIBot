from http.client import responses

from rich.box import MARKDOWN
from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Input, Button, Header, Footer, Static, RichLog, Switch
from rich.text import Text
from rich.markdown import Markdown
import asyncio
import time
import simpleaudio as sa
import wave
from google import genai
from google.genai import types
import wave


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


client = genai.Client(api_key='AIzaSyDxD_6QbBZEpZeYVbDgEtOC0LZC8_074Qk')


class Bott(Static):
    async def speech(self, val):
        responses = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=val,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Kore',
                            )
                        )
                    ),
                )
            )
        data = responses.candidates[0].content.parts[0].inline_data.data
        file_name = 'out.wav'
        wave_file(file_name, data)
    async def user_input(self, a: Input):
        ans = ''
        log = self.app.query_one("#text", RichLog)
        log.write(f"[bold green]Q:[/] [bold blue]{a.value}")
        a.placeholder = "Loading..."
        a.disabled = True
        button_send = self.query_one("#button_send", Button)
        button_send.disabled = True
        log.write(f"[bold red]A:")
        async for chunk in await client.aio.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=a.value
        ):
            log.write(f"[bold blue]{chunk.text}")
            ans = ans + chunk.text
        a.disabled = False
        button_send.disabled = False
        a.clear()
        a.placeholder = "next"
        if self.app.query_one("#switch_voice", Switch).value:
            await self.speech(ans)

    @on(Button.Pressed)
    async def pressed(self):
        input = self.query_one("#input", Input)
        await self.user_input(input)

    @on(Input.Submitted)
    async def input_submit(self, message: Input.Submitted):
        await self.user_input(message.input)

    def compose(self) -> ComposeResult:
        yield Input(id="input")
        yield Button("send", variant="success", id="button_send")
        yield Static("voice:", classes="label")
        yield Switch(value=False, name="voice", animate=True, id="switch_voice")


class Ai(App):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle dark mode")
    ]
    CSS_PATH = "AIbot.css"
    def compose(self) -> ComposeResult:
        self.title = "This is a chat robot"
        yield Header(show_clock=True)
        yield Footer()
        yield RichLog(id="text", auto_scroll=True, markup=True)
        #        with ScrollableContainer():
        yield Bott()


#    def action_toggle_dark_mode(self):
#        self.dark=not self.dark
if __name__ == "__main__":
    Ai().run()
