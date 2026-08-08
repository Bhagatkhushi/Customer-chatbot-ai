import os
from flask import Flask, render_template, request, jsonify
from chatbot import get_response

app = Flask(__name__,
        static_folder="static",
        template_folder="templates")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chatbot_response():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "")
    response = get_response(user_msg)
    return jsonify({"reply": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)