import requests
from bs4 import BeautifulSoup

@app.route("/summarize", methods=["POST"])
def summarize():
    # if not verify_slack_request(request):
    #     return "Unauthorized", 403

    user_input = request.form.get("text", "").strip()
    
    if not user_input:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Please provide text to summarize."
        })

    # 🔍 URL Detected
    if user_input.startswith("http"):
        try:
            page = requests.get(user_input, timeout=5)
            soup = BeautifulSoup(page.text, "html.parser")
            title = soup.title.string if soup.title else ""
            paragraphs = soup.find_all("p")
            body_text = " ".join(p.get_text() for p in paragraphs[:10])  # Limit to 10 <p> tags

            content_to_summarize = f"Title: {title}\n\nContent: {body_text}"
        except Exception as e:
            return jsonify({
                "response_type": "ephemeral",
                "text": f"Failed to fetch or parse URL: {str(e)}"
            })
    else:
        content_to_summarize = user_input

    prompt = f"""Write a short, news-style summary of the following content:\n\n{content_to_summarize}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        story = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"Something went wrong: {str(e)}"
        })

    return jsonify({
        "response_type": "in_channel",
        "text": f"*Summary by GPT-3.5-turbo:*\n{story}"
    })
