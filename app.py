from flask import Flask, render_template, request, redirect, url_for, session
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.secret_key = "translator_secret_key"  # required for session


@app.route("/", methods=["GET", "POST"])
def index():

    # POST → translate & store temporarily
    if request.method == "POST":
        text = request.form.get("text")
        source = request.form.get("source")
        target = request.form.get("target")

        translated_text = ""
        if text:
            translated_text = GoogleTranslator(
                source=source,
                target=target
            ).translate(text)

        # store ONE-TIME data
        session["original"] = text
        session["output"] = translated_text

        return redirect(url_for("index"))

    # GET → read once & clear
    original = session.pop("original", "")
    output = session.pop("output", "")

    return render_template(
        "index.html",
        original=original,
        output=output,
        source="auto",
        target="en"
    )

if __name__ == "__main__":
    app.run()
