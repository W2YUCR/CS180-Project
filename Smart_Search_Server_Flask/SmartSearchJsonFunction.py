# libraries
from flask import Flask, jsonify, request, render_template_string
import os
import re
import nltk
from nltk.corpus import wordnet
import praw

#experimental
import openai
openai.api_key = "Useyourkeybymakingadeveloperaccount"

# should pip install praw or nltk if not installed already


# API credentials: Reddit

# Create a reddit develepor account for your credentials
# I have used mine on the app
# Blurred out the password though

reddit = praw.Reddit(
    client_id="0xJRA2fY3PeOQYmZF_Qokw",
    client_secret="Pd2ddW-y9B4cs42c2QbRtnWvJvVoSg",
    password="UseYourPassword",
    user_agent="AnythingYouWant",
    username="UseYourUsername",
)

# Ensure NLTK is there, sometimes server goes idle and shuts it off
try:
    wordnet.synsets("dog")  # Check if wordnet is already downloaded

except LookupError:
    nltk.download("wordnet")
    nltk.download("omw-1.4")


app = Flask(__name__)


# File to store flashcards
user_home = os.path.expanduser("~")
flashcards_file = os.path.join(user_home, "AllFlashcards.txt")

# experimental, using praw.


# can change limit depending on how you want it
# also, you can call it multiple times with diff queries.
# only calling the top flashcard right now
def reddit_search(query, limit=5):
    try:
        results = []

        subreddit = reddit.subreddit("all")

        search_results = subreddit.search(query, limit=limit, sort="relevance")

        for submission in search_results:
            title = submission.title

            selftext = submission.selftext
            if not selftext:
                selftext = ""

            words = re.findall(r"\w+", selftext)

            if words:
                snippet = " ".join(words[:25])
            else:
                snippet = title

            subreddit_name = submission.subreddit.display_name

            upvotes = submission.score

            url = submission.url

            post_info = (
                "Subreddit: r/"
                + subreddit_name
                + "\n"
                + "Upvotes: "
                + str(upvotes)
                + "\n"
                + "Title: "
                + title
                + "\n"
                + "Snippet: "
                + snippet
                + "...\n"
                + "URL: "
                + url
                + "\n"
                + "-----------------------------"
            )

            results.append(post_info)

        return results

    except Exception as e:
        return [f"Reddit search error: {str(e)}"]


def expand_with_synonyms(words):
    expanded = set(words)
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name().replace("_", " "))
    return expanded


def compute_frequencies(text):
    words = re.findall(r"\w+", text.lower())
    freq: dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def bm25_score(query_words, doc_freq, doc_len):
    if doc_len == 0:
        return 0
    score = 0
    for word in query_words:
        freq = doc_freq.get(word, 0)
        if freq > 0:
            numerator = 2 * freq
            denominator = freq + (2 * (0.25 * (doc_len / 20)))
            score += numerator / denominator
    return score


# Load existing flashcards into memory
# Are stored and indexed in backend JSON file
def load_flashcards():

    if os.path.exists(flashcards_file):
        with open(flashcards_file, "r", encoding="utf-8") as f:
            cards = []
            for line in f:
                line = line.strip()
                if line:
                    match = re.match(r"\[ID: (\d+), Frequencies: (.*?)\](.*)", line)
                    if match:
                        id_num = int(match.group(1))
                        freq_str = match.group(2)
                        content = match.group(3).strip()
                        try:
                            freq_dict = eval(freq_str)
                        except:
                            freq_dict = {}
                        cards.append(
                            {"id": id_num, "frequencies": freq_dict, "content": content}
                        )
            return cards
    return []


def save_flashcards(cards):

    with open(flashcards_file, "w", encoding="utf-8") as f:
        for card in cards:
            line = f"[ID: {card['id']}, Frequencies: {card['frequencies']}] {card['content']}"
            f.write(line + "\n")


# Init
all_flashcards = load_flashcards()


# HTML
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Flashcard App</title>
</head>
<body>
    <h1>Enter Flashcards</h1>
    <form action="/api/value" method="get">
        <label for="user_string">Your String:</label><br>
        <textarea id="user_string" name="user_string" rows="5" cols="50" placeholder="Enter one or more flashcards (newline-separated)..."></textarea><br><br>

        <label for="user_id">Flashcard ID (optional):</label>
        <input type="number" id="user_id" name="user_id" placeholder="Defaults to 0"><br><br>

        <label for="insertOrNot">Insert? (1 = yes, 0 = search):</label>
        <input type="number" id="insertOrNot" name="insertOrNot" min="0" max="1" value="1"><br><br>

        <button type="submit">Submit</button>
    </form>

    {% if values %}
        <h2>Results:</h2>
        <ul>
        {% for val in values %}
            <li style="white-space: pre-line;">{{ val }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(form_html, values=None)


@app.route("/api/value", methods=["GET"])
def get_value():
    global all_flashcards

    user_input = request.args.get("user_string", type=str)
    insert_or_not = request.args.get("insertOrNot", default=1, type=int)
    user_id = request.args.get("user_id", default=0, type=int)

    results = []

    if insert_or_not == 1:
        if user_input:
            lines = user_input.strip().split("\n")
            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    frequencies = compute_frequencies(clean_line)
                    card = {
                        "id": user_id,
                        "frequencies": frequencies,
                        "content": clean_line,
                    }
                    all_flashcards.append(card)
            save_flashcards(all_flashcards)

        results = [
            f"[ID: {card['id']}, Frequencies: {card['frequencies']}] {card['content']}"
            for card in all_flashcards
        ]

    elif insert_or_not == 0:
        # Filter by ID if specified
        # If there is no ID just return all relavent results
        # ID is primarily meant to get the set of flashcards
        # No ID means just search flashcards
        matching_cards = all_flashcards
        if user_id != 0:
            matching_cards = [card for card in all_flashcards if card["id"] == user_id]

        if not user_input:
            results = [
                f"[ID: {card['id']}, Frequencies: {card['frequencies']}] {card['content']}"
                for card in matching_cards
            ]
        else:
            input_words = re.findall(r"\w+", user_input.lower())
            expanded_query_words = expand_with_synonyms(input_words)

            scored_cards = []
            for card in matching_cards:
                doc_len = sum(card["frequencies"].values())

                # this is the actual bm25 scoring, might modify it to include things like dirichlet smoothing and vector space/cosine sim
                # and then ensemble them
                # that way the results will be REALLY good
                score = bm25_score(expanded_query_words, card["frequencies"], doc_len)

                if score > 0:
                    scored_cards.append((score, card))

            scored_cards.sort(key=lambda x: x[0], reverse=True)
            results = [
                f"[ID: {card['id']}, Frequencies: {card['frequencies']}] {card['content']}"
                for score, card in scored_cards
            ]

            if scored_cards:
                top_card = scored_cards[0][1]
                reddit_results = reddit_search(top_card["content"], limit=5)
                results.append("\nRelated Reddit Posts:")
                results.extend(reddit_results)

    # Return either HTML or JSON
    # if 'text/html' in request.headers.get('Accept', ''):
    #    return render_template_string(form_html, values=results)

    return jsonify({"strings": results})


if __name__ == "__main__":
    app.run(debug=True)