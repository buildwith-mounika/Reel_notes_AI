from flask import Flask, render_template, request, jsonify
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini Client
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Extract YouTube Video ID
def get_video_id(url):
    match = re.search(r"(?:v=|shorts/|youtu\.be/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():

    data = request.get_json()

    url = data.get("url")
    language = data.get("language")

    video_id = get_video_id(url)

    if not video_id:
        return jsonify({
            "summary": "❌ Invalid YouTube URL"
        })

    try:

        # Get transcript
        transcript = YouTubeTranscriptApi().fetch(video_id)

        # Convert transcript to plain text
        text = " ".join([item.text for item in transcript])

        # Prompt based on language
        if language == "telugu":

            prompt = f"""
ఈ YouTube వీడియో ట్రాన్స్‌క్రిప్ట్‌ను సులభమైన తెలుగులో వివరించు.

నియమాలు:
- బుల్లెట్ పాయింట్లలో రాయాలి.
- సులభమైన తెలుగు ఉపయోగించాలి.
- ముఖ్యమైన విషయాలు మాత్రమే చెప్పాలి.

Transcript:

{text}
"""

        else:

            prompt = f"""
Summarize this YouTube transcript in simple English.

Rules:
- Use bullet points.
- Keep the language simple.
- Mention only important points.

Transcript:

{text}
"""

        # Gemini Summary
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return jsonify({
            "summary": response.text
        })

    except Exception as e:

        return jsonify({
            "summary": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)