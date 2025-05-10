from flask import Flask, render_template, request, url_for, redirect
import chemback
import chemcursor
import re
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource (compatible with PyInstaller)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__,
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

# When accessing DBs or files:
db_path = resource_path("compounds.db")

# app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Route to Splash/Welcome Screen
@app.route('/', methods=['GET'])
def splash():
    return render_template('splash.html')

# Route to Homepage
@app.route('/index', methods=['GET', 'POST'])
def index():
    # When user submit something (formula) skskskks
    if request.method == 'POST':
        formula = request.form['inputFormula'].strip()
        if not formula:
            error = "Please enter a chemical formula."
            return render_template('index.html', error=error, results=None)

        # Some Error Happened :( meow meow meow meow
        results = chemback.retrieve_compounds(formula)
        if not results or 'error' in results:
            error = results['error'] if results else "Unknown error occurred."
            samples = chemcursor.sample_compounds()
            return render_template('index.html', error=error, results=None, samples=samples)

        return render_template('index.html', error=None, results=results, samples=None)
    else:
        # default homepage
        samples = chemcursor.sample_compounds()
        return render_template('index.html', error=None, results=None, samples=samples)

# When user clicked on a compound card on homepage
@app.route('/compound-details', methods=['POST'])
def compound_details():
    compound_id = request.form.get('compound_id')
    compound = chemback.generate_structure(compound_id)
    # TBH di na need this, meh tamad ko magdelete
    if not compound:
        return "Compound not found", 404

    return render_template('result.html', compound=compound)

# Route for choosing difficulty
@app.route('/test-difficulty', methods=['GET'])
def choose_difficulty():
    return render_template('test-difficulty.html')

# Route for when test started
@app.route('/test', methods=['GET'])
def test():
    difficulty = request.args.get('difficulty')
    if difficulty not in ['Easy', 'Hard']:
        return redirect(url_for('test_difficulty'))

    questions = chemcursor.retrieve_questions(difficulty)

    def subscript_formula(text):
        return re.sub(r'(\d+)', r'<sub>\1</sub>', text)

    """
        q[0] = id
        q[1] = question text
        q[2] = category
        q[3] = difficulty
        q[4] = correct answer
        q[5] = choices w/ correct answer
        q[6] = inchi (for 2d generating 2d image)
    """
    questions_data = []
    for q in questions:
        question_text = subscript_formula(q[1])
        question_data = {
            'id': q[0],
            'question_text': question_text,
            'category': q[2],
            'difficulty': q[3],
            'correct_answer': q[4],
            'choices': q[5].split(',') if q[5] else None,
            'type': 'multiple_choice' if q[5] else 'identification',
        }

        if q[6]:
            question_data['structure_image'] = chemback.generate_2d_structure(q[6])

        questions_data.append(question_data)

    return render_template('test.html', questions=questions_data, current=0)

@app.route('/databases', methods=['GET'])
def choose_database():
    return render_template('databases.html')

@app.route('/database_select', methods=['POST'])
def database_select():
    database = request.form.get("database_selection")
    if database == 'Compounds':
        return redirect(url_for('compounds_database'))
    elif database == 'Questions':
        return redirect(url_for('questions_database'))
    else:
        return redirect(url_for('databases'))

@app.route('/compounds_database', methods=['GET'])
def compounds_database():
    per_page = request.args.get("per_page", 10, type=int)
    page = request.args.get("page", 1, type=int)
    data, total_count = chemcursor.compounds_database_retrieval(page, per_page)
    return render_template('compounds_database.html', database='Compounds', data=data, total_count=total_count, per_page=per_page, page=page)

@app.route('/questions_database', methods=['GET'])
def questions_database():
    per_page = request.args.get("per_page", 10, type=int)
    page = request.args.get("page", 1, type=int)
    data, total_count = chemcursor.questions_database_retrieval(page, per_page)
    return render_template('questions_database.html', database='Questions', data=data, total_count=total_count, per_page=per_page, page=page)

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    entry_id = request.form.get("entry_id")
    database = request.form.get("database")
    if database == "Compounds":
        chemcursor.delete_compound(entry_id)
        return redirect(url_for('compounds_database'))
    elif database == "Questions":
        chemcursor.delete_question(entry_id)
        return redirect(url_for('questions_database'))

@app.route('/edit_entry', methods=['POST'])
def edit_entry():
    form_data = request.form.to_dict()
    database = form_data.pop("database")
    if database == "Compounds":
        chemcursor.edit_compound(form_data)
        return redirect(url_for('compounds_database'))
    elif database == "Questions":
        chemcursor.edit_question(form_data)
        return redirect(url_for('questions_database'))

@app.route('/add_entry', methods=['POST'])
def add_entry():
    form_data = request.form.to_dict()
    database = form_data.pop("database")
    if database == "Compounds":
        chemcursor.add_compound(form_data)
        return redirect(url_for('compounds_database'))
    elif database == "Questions":
        chemcursor.add_question(form_data)
        return redirect(url_for('questions_database'))

# self explanatory :)
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
