from flask import Flask, request, jsonify
import openai
import os
import hmac
import hashlib

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

def verify_slack_request(req):
    timestamp = req.headers.get('X-Slack-Request-Timestamp')
    sig_basestring = f"v0:{timestamp}:{req.get_data(as_text=True)}"
    my_signature = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    slack_signature = req.headers.get('X-Slack-Signature')
    return hmac.compare_digest(my_signature, slack_signature)

@app.route("/summarize", methods=["POST"])
def summarize():
    if not verify_slack_request(request):
        return "Unauthorized", 403

    user_input = request.form.get("text", "")
    prompt = f"""Write a short, news-style summary of the following message:\n\n{user_input}"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )

    story = response.choices[0].message.content.strip()

    return jsonify({
        "response_type": "in_channel",
        "text": f"*Summary by GPT-4:*\n{story}"
    })

@app.route("/", methods=["GET"])
def health_check():
    return "Summarize bot is running!", 200



if __name__ == "__main__":
    app.run()
