from operator import truediv

from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.widget import Widget
from textual.message import Message
import time


# Define a custom message
class GreetMessage(Message):
    def __init__(self, sender: Widget, text: str) -> None:
        self.text = text
        super().__init__()


# The widget that will receive messages
class Receiver(Static):
    def on_greet_message(self, message: GreetMessage) -> None:
        self.update(f"🎉 Received: {message.text}")


# The widget that will send messages
class Sender(Button):
    def on_button_pressed(self) -> None:
        # Find the receiver by ID and send a message
        receiver = self.app.query_one("#receiver", expect_type=Receiver)
        receiver.post_message(GreetMessage(self, "Hello from Sender!"))
        while True:
            time.sleep(10)


# The app
class MessageDemo(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    BINDINGS = [("q", "quit", "QUIT")]

    def compose(self) -> ComposeResult:
        yield Sender("Click Me")
        yield Receiver("Waiting...", id="receiver")

    async def action_quit(self):
        self.app.exit()


if __name__ == "__main__":
    MessageDemo().run()
