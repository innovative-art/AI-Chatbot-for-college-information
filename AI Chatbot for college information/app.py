from flask import Flask, render_template, request, jsonify, send_file, url_for
import json
import os

app = Flask(__name__)

# Landing page
@app.route('/')
def landing():
    about_content = (
        "SDM Institute of Technology is an ambition-driven technological institution situated in Ujire within the homely ambiance of SDM Institutions "
        "and the serenity of the Western Ghats. Managed by SDM Educational Society Ujire under the impeccable leadership of Sri. D. Veerendra Heggade, "
        "the institution has thrived over the years in the areas of academics, innovation, and extracurricular activities. "
        "With more than 1500 students availing quality education every year, the college flaunts a testimony of over 2500 alumni who are exceptionally well placed in society today. "
        "For the last 13 years, SDMIT has been successfully delivering the promise of education rooted in discipline and the holistic development of students."
    )
    vision = "Excellence in Education, Commitment to Society"
    mission = (
        "Create an atmosphere that facilitates sensitizing the young technocrats to the needs of the community "
        "with relevant inputs of academic, innovative and research capabilities."
    )
    core_values = [
        "Achieve Excellence",
        "Demonstrate high Ethical values",
        "Be a Team player",
        "Nurture Inquisitiveness",
        "Inculcate Professionalism",
    ]
    return render_template(
        'landing.html', about=about_content, vision=vision, mission=mission, core_values=core_values
    )

@app.route('/chat')
def chat():
    return render_template('index.html')

# Load datasets
datasets_path = os.path.join(os.getcwd(), 'static', 'datasets')
with open(os.path.join(datasets_path, 'admissions.json')) as f:
    admissions = json.load(f)
with open(os.path.join(datasets_path, 'fees.json')) as f:
    fees = json.load(f)
with open(os.path.join(datasets_path, 'courses.json')) as f:
    courses = json.load(f)
with open(os.path.join(datasets_path, 'lecturers.json')) as f:
    lecturers = json.load(f)
with open(os.path.join(datasets_path, 'syllabus.json')) as f:
    syllabus = json.load(f)

# Principal details
principal_info = {
    "name": "Dr. Ashok Kumar",
    "designation": "Principal, SDM Institute of Technology",
    "about": (
        "Dr. Ashok Kumar obtained BE in Electronics & Communication Engineering from MCE, Hassan, and ME in Digital Electronics from SDM College of Engg & Technology, Dharwad. "
        "In 2010, he was awarded Ph.D. from VTU under the guidance of Dr. Shivaprakash Koliwad and Dr. Dwarakish."
    ),
    "hobbies": "Cartoon sketching, writing articles, Indian Classical Music, Photography",
    "message": "Welcome to SDMIT, where we empower students to achieve academic excellence and personal growth.",
    "photo": "static/images/principal.jpg",
}

# College images
college_images = [
    "static/images/college1.jpeg",
    "static/images/college2.jpg",
    "static/images/college3.jpg",
    "static/images/college4.jpeg",
    "static/images/college5.jpg",
    "static/images/college6.jpeg",
]

# Placement details
placement_details = {
    "2023-24": "Placed 78% of the eligible students | 75+ companies and 253+ appointment offers.",
    "2022-23": "Placed 78% of the eligible students | 110+ companies and 294+ appointment offers.",
    "2021-22": "Placed 83% of the eligible students | 150+ companies and 430+ appointment offers.",
    "2020-21": "Placed 53% of the eligible students | 110+ companies and 230+ appointment offers.",
}

# CET and COMEDK codes
college_codes = {
    "cet": "E152",
    "comedk": "E118",
}

# Chat history
search_history = []

# Keyword analysis
def extract_keywords(query):
    """
    Extract and analyze keywords from the user query.
    """
    keywords = [word.lower() for word in query.split() if len(word) > 3]
    return keywords

# Format responses
def process_query(query):
    query = query.lower()
    keywords = extract_keywords(query)

    # Greetings and polite phrases
    if any(word in query for word in ["hi", "hello", "hey"]):
        return "Hello! How can I assist you today? 😊"

    if "bye" in query or "goodbye" in query:
        return "Bye! Have a great day ahead! 😊"

    if "thank you" in query or "thanks" in query:
        return "You're welcome! Feel free to ask if you need further assistance. 😊"

    # Principal information
    if "principal" in keywords:
        return (
            f"<b>{principal_info['name']}</b><br>"
            f"<b>{principal_info['designation']}</b><br>"
            f"{principal_info['about']}<br><br>"
            f"<b>Hobbies:</b> {principal_info['hobbies']}<br>"
            f"<b>Message:</b> {principal_info['message']}<br>"
            f"<img src='{principal_info['photo']}' alt='Principal Photo' style='width:200px;'>"
        )

    # About, Vision, Mission, and Core Values
    if "about college" in keywords:
        return (
            "SDM Institute of Technology is an ambition-driven technological institution situated in Ujire within the homely ambiance of SDM Institutions "
            "and the serenity of the Western Ghats..."
        )
    if "vision" in keywords:
        return "Vision: Excellence in Education, Commitment to Society"
    if "mission" in keywords:
        return (
            "Mission: Create an atmosphere that facilitates sensitizing the young technocrats to the needs of the community "
            "with relevant inputs of academic, innovative and research capabilities."
        )
    if "values" in keywords:
        return (
            "Core Values:<br>"
            "1. Achieve Excellence<br>"
            "2. Demonstrate high Ethical values<br>"
            "3. Be a Team player<br>"
            "4. Nurture Inquisitiveness<br>"
            "5. Inculcate Professionalism"
        )
    # CET and COMEDK codes
    if "cet" in query:
        return f"The CET code for SDM Institute of Technology is: <b>{college_codes['cet']}</b>."
    if "comedk" in query:
        return f"The COMEDK code for SDM Institute of Technology is: <b>{college_codes['comedk']}</b>."

    # Placement details
    if "placement" in query:
        placement_info = "<br>".join([f"<b>{year}:</b> {details}" for year, details in placement_details.items()])
        return f"PLACEMENT TRACK RECORD:<br>{placement_info}"
    

    # Dataset responses
    if "admission" in keywords:
        return admissions.get("general_info", "Admissions are open for the academic year 2024-25. For details, visit the admissions office or contact office@sdmit.in.")
    if "fees" in keywords:
        return format_json_response(fees)
    if "courses" in keywords:
        return format_courses_response(courses)
    if "lecturers" in keywords:
        return format_lecturers_response(lecturers)
    if "syllabus" in keywords:
        for branch in syllabus.keys():
            if branch.lower() in query:
                return f"Here is the <a href='/download/{branch}' target='_blank'>{branch} syllabus</a> 📄."
        return "Please specify the branch for the syllabus, e.g., 'computer science syllabus'. 😊"

    # College images
    if "images" in keywords:
        images_html = "<br>".join([f"<img src='{image}' alt='College Image' style='width:200px; margin:5px;'>" for image in college_images])
        return f"Here are some images of our college:<br>{images_html}"

    return "Sorry, I couldn't find relevant information. Please try again! 😊"

def format_json_response(data):
    return "<br>".join([f"<b>{key}:</b> {value}" for key, value in data.items()])

def format_courses_response(courses):
    return "<br><br>".join([f"<b>{branch}:</b> " + "<br>".join(subjects) for branch, subjects in courses.items()])

def format_lecturers_response(lecturers):
    return "<br><br>".join([f"<b>Name:</b> {lec['name']}<br><b>Department:</b> {lec['department']}<br><b>Designation:</b> {lec['designation']}" for lec in lecturers])

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    if user_query:
        response = process_query(user_query)
        search_history.append({"query": user_query, "response": response})
        return jsonify({"response": response, "history": search_history})
    return jsonify({"response": "Please ask a valid question."})

@app.route('/download/<branch>')
def download(branch):
    file_path = os.path.join('static', 'syllabus_files', f'{branch}_syllabus.pdf')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Syllabus file not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
