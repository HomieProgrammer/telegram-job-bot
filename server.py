# server.py
from flask import Flask
import threading
from main import main  # your bot runner

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running on Render!"

threading.Thread(target=main).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
