import threading

@app.route("/summarize", methods=["POST"])
def summarize():
    user_input = request.form.get("text", "").strip()
    response_url = request.form.get("response_url")

    if not user_input:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Please provide text to summarize."
        })

    # Respond immediately so Slack doesn't timeout
    threading.Thread(target=process_summary, args=(user_input, response_url)).start()
    return "", 200

def process_summary(user_input, response_url):
    try:
        if user_input.startswith("http"):
            page = requests.get(user_input, proxies=proxies, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "Untitled"
            paragraphs = soup.find_all("p")
            content = " ".join(p.get_text() for p in paragraphs[:10])
            content_to_summarize = f"Title: {title}\n\n{content}"
        else:
            content_to_summarize = user_input

        prompt = f"""
Please generate a concise news-style output from the following content. Your response should be between 2-5 paragraphs and structured as follows:

1. A clear, engaging headline.
2. A 1-2 paragraph summary of the article’s main content and reporting.
3. A final paragraph (or two) labeled “Why it matters:” that gives context and significance — why this story is important, notable, or has broader implications.

Here is the source content:
{content_to_summarize}
"""
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        story = completion.choices[0].message.content.strip()
        requests.post(response_url, json={"text": f"*Summary by GPT-3.5-turbo:*\n{story}"})
    except Exception as e:
        requests.post(response_url, json={"text": f"Something went wrong: {str(e)}"})
