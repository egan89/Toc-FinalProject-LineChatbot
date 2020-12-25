import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()


machine = TocMachine(
    states=["user", "input_2currency", "check", "calculate", "input_number"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "input_2currency",
            "conditions": "is_going_to_input_2currency",
        },
        {
            "trigger": "advance",
            "source": "input_2currency",
            "dest": "check",
            "conditions": "is_going_to_check",
        },
        {
            "trigger": "advance",
            "source": "input_2currency",
            "dest": "calculate",
            "conditions": "is_going_to_calculate",
        },
        {
            "trigger": "advance",
            "source": "calculate",
            "dest": "input_number",
            "conditions": "is_going_to_input_number",
        },
        {"trigger": "go_back", "source": ["check", "input_number", "calculate", "input_2currency"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        
        response = machine.advance(event)
        if response == False:
            if machine.state == "user":
                if event.message.text.lower() == 'fsm':
                    send_image_message(event.reply_token, 'https://drive.google.com/file/d/1CAtrQR0leEkBFqfNoaZAvXcUX6UMWaWM/view?usp=sharing')
                else:
                    send_text_message(event.reply_token, "請正確輸入兩種貨幣 ex: TWD JPY")
            elif machine.state == "input_2currency":
                send_text_message(event.reply_token, "請輸入 check or calculate")
            elif machine.state == "calculate":
                send_text_message(event.reply_token, "請輸入一個合法數字")
        
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
