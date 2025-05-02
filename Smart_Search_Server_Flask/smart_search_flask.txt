
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Store all submitted strings
all_strings = []

# Updated HTML form template
form_html = '''
<!DOCTYPE html>
<html>
<head>
	<title>String Echo</title>
</head>
<body>
	<h1>Enter a String</h1>
	<form action="/api/value" method="get">
    	<label for="user_string">Your String:</label>
    	<input type="text" id="user_string" name="user_string" placeholder="Enter your text here"><br><br>

    	<label for="insertOrNot">Insert? (1 = yes, 0 = search):</label>
    	<input type="number" id="insertOrNot" name="insertOrNot" min="0" max="1" value="1"><br><br>

    	<button type="submit">Submit</button>
	</form>

	{% if values %}
    	<h2>Results:</h2>
    	<ul>
    	{% for val in values %}
        	<li>{{ val }}</li>
    	{% endfor %}
    	</ul>
	{% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
	return render_template_string(form_html, values=None)

@app.route('/api/value', methods=['GET'])
def get_value():
	global all_strings

	# Get user input
	user_input = request.args.get('user_string', type=str)
	insert_or_not = request.args.get('insertOrNot', default=1, type=int)

	# Initialize results
	results = []

	if insert_or_not == 1:
    	# Insert new string if provided
    	if user_input:
        	all_strings.append(user_input)
    	results = all_strings

	elif insert_or_not == 0:
    	if not user_input:
        	# No input, return all stored strings
        	results = all_strings
    	else:
        	# Search: split input into words and find matching strings
        	input_words = set(user_input.lower().split())
        	for s in all_strings:
            	string_words = set(s.lower().split())
            	if input_words & string_words:  # Intersection is not empty
                	results.append(s)

	# If the request is from a browser form, return HTML
	if 'text/html' in request.headers.get('Accept', ''):
    	return render_template_string(form_html, values=results)

	# Otherwise return JSON
	return jsonify({'strings': results})

if __name__ == '__main__':
	app.run(debug=True)

