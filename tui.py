from textual.app import App
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.events import Mount
from textual.widgets import Header, Input, RichLog, Button
from textual import on
from gemini import genai_client
from gemini import config


def markdown_stream_splitter(chunk: str) -> tuple[str, str | None]:
    """
    Splits a markdown chunk into a tuple of (text, markdown).
    This is a placeholder function; actual implementation may vary.
    """
    # For simplicity, we assume the chunk is already in the desired format.
    return (chunk, None)


class Asking(HorizontalGroup):
    @on(Input.Submitted)
    async def user_input_submitted(self, message: Input.Submitted):
        question = message.value.strip()
        message.input.clear()
        message.input.placeholder = "Thinking..."
        message.input.disabled = True

        log = self.app.query_one("#text", RichLog)
        log.write(f"[bold green]Q:[/] [bold blue]{message.value}")
        async for chunk in await genai_client.aio.models.generate_content_stream(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=question,
            config=config,
        ):
            if chunk.candidates[0].content.parts[0].function_call:
                function_call = chunk.candidates[0].content.parts[0].function_call
                log.write(f"Function to call: {function_call.name}")
                log.write(f"Arguments: {function_call.args}")

            log.write(chunk.text)
        message.input.disabled = False
        message.input.placeholder = "ready to answer..."
        message.input.focus()

    def compose(self) -> ComposeResult:
        yield Input(id="user_input")
        yield Button("Ask")


class MyTUI(App):
    BINDINGS = [("q", "quit", "QUIT")]
    CSS_PATH = "aibot.css"

    def compose(self) -> ComposeResult:
        self.title = "The TUI"
        yield Header(show_clock=True)
        yield RichLog(id="text", auto_scroll=True, markup=True)
        yield Asking()

    async def on_mount(self, event: Mount):
        user_input = self.query_one("#user_input", Input)
        user_input.placeholder = "ready to answer..."
        user_input.focus()

    async def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = MyTUI()
    app.run()
