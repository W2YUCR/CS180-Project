from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "sk-proj-kQHNo0S3IzFwctIo0e7NxbyEzV1q4E5kfr_jj9Mifvi9Cinyj-89vIYAA"

system_prompt = {
    "role": "system",
    "content": "You are an AI, a helpful assistant. Summarize the following flashcard. Only give a summary, somewhat short. Dont ask any questions.",
}


@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("message")
    if not user_message:
        return jsonify({"error": "Missing 'message' parameter"}), 400

    messages = [
        {"role": "system", "content": system_prompt["content"]},
        {"role": "user", "content": str(user_message)},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )
        answer = (response.choices[0].message.content or "").strip()
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()
