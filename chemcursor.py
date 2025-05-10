import sqlite3
import random
import chemback

def search_database(formulas, components):
    conn = sqlite3.connect('compounds.db')
    cursor = conn.cursor()

    placeholders = ', '.join(['?'] * len(formulas))

    query = f"""
        SELECT id, name, formula, inchi
        FROM compounds
        WHERE formula IN ({placeholders})
    """

    cursor.execute(query, formulas)
    results = cursor.fetchall()

    placeholders = ', '.join(['?'] * len(components))

    query = f"""
        SELECT id, name, formula, inchi
        FROM compounds
        WHERE formula IN ({placeholders})
    """

    cursor.execute(query, components)
    resultsB = cursor.fetchall()

    for i in resultsB:
        if i not in results:
            results.append(i)

    print(results)
    conn.close()
    return results

def retrieve_compound(id):
    conn = sqlite3.connect('compounds.db')
    cursor = conn.cursor()

    query = """
        SELECT id, name, formula, inchi, mol_weight, color, form, bond_type
        FROM compounds
        WHERE id = ?
    """
    
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    conn.close()

    return result

def sample_compounds():
    conn = sqlite3.connect('compounds.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT id, formula, name, inchi
        FROM compounds
        ORDER BY id ASC
        LIMIT 5;
    """

    cursor.execute(query)
    samples = []
    for row in cursor.fetchall():
        row_dict = dict(row)
        row_dict['formula'] = chemback.formulasubscript(row_dict['formula'])
        inchi_str = row_dict.get('inchi')
        row_dict['structure_image'] = chemback.generate_2d_structure(inchi_str)
        samples.append(row_dict)

    conn.close()
    return samples

def retrieve_questions(difficulty):
    conn = sqlite3.connect('questions.db')
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA temp_store = MEMORY")
    conn.execute("PRAGMA cache_size = -1000")

    if difficulty == 'Easy':
        query = "SELECT * FROM questions WHERE difficulty = 'Easy' ORDER BY RANDOM() LIMIT 10"

        questions = conn.execute(query).fetchall()
        random.shuffle(questions)
        conn.close()
        return questions
    elif difficulty == 'Hard':
        query = "SELECT * FROM questions WHERE difficulty = 'Hard' ORDER BY RANDOM() LIMIT 25"

        questions = conn.execute(query).fetchall()
        random.shuffle(questions)
        conn.close()
        return questions
    
def get_paginated_data(query, page, per_page, db_name):
    offset = (page - 1) * per_page
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    cursor.execute(query + " LIMIT ? OFFSET ?", (per_page, offset))
    data = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM (" + query + ")")
    total_count = cursor.fetchone()[0]
    
    connection.close()
    return data, total_count
    
def compounds_database_retrieval(page, per_page):
    query = "SELECT * FROM compounds"
    return get_paginated_data(query, page, per_page, "compounds.db")

def questions_database_retrieval(page, per_page):
    query = "SELECT * FROM questions"
    return get_paginated_data(query, page, per_page, "questions.db")

def delete_compound(entry_id):
    conn = sqlite3.connect('compounds.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM compounds WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def delete_question(entry_id):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def edit_compound(form_data):
    conn = sqlite3.connect('compounds.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE compounds SET name = ?, formula = ?, inchi = ?, mol_weight = ?, color = ?, form = ?, bond_type = ? WHERE id = ?", 
                   (form_data["name"], form_data["formula"], form_data["inchi"], form_data["mol_weight"], form_data["color"], form_data["form"], form_data["bond_type"], form_data["entry_id"]))
    conn.commit()
    conn.close()

def edit_question(form_data):
    if form_data['category'] == 'Multiple Choice':
        choices_string = f"{form_data['choice1']},{form_data['choice2']},{form_data['choice3']},{form_data['choice4']}"

        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE questions
            SET question_text = ?, category = ?, difficulty = ?, correct_answer = ?, choices = ?, inchi = ?
            WHERE id = ?
        """, (form_data['question_text'], form_data['category'], form_data['difficulty'], 
            form_data['correct_answer'], choices_string, form_data['inchi'], form_data['entry_id']))
    else:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE questions
            SET question_text = ?, category = ?, difficulty = ?, correct_answer = ?, choices = '', inchi = ?
            WHERE id = ?
        """, (form_data['question_text'], form_data['category'], form_data['difficulty'], 
            form_data['correct_answer'], form_data['inchi'], form_data['entry_id']))
    conn.commit()
    conn.close()

def add_compound(form_data):
    conn = sqlite3.connect('compounds.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO compounds (name, formula, inchi, mol_weight, color, form, bond_type) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (form_data["name"], form_data["formula"], form_data["inchi"], form_data["mol_weight"], form_data["color"], form_data["form"], form_data["bond_type"]))
    conn.commit()
    conn.close()

def add_question(form_data):
    if form_data['category'] == 'Multiple Choice':
        choices_string = f"{form_data['choice1']},{form_data['choice2']},{form_data['choice3']},{form_data['choice4']}"

        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions (question_text, category, difficulty, correct_answer, choices, inchi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (form_data['question_text'], form_data['category'], form_data['difficulty'], 
            form_data['correct_answer'], choices_string, form_data['inchi']))
    else:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions (question_text, category, difficulty, correct_answer, inchi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (form_data['question_text'], form_data['category'], form_data['difficulty'], 
            form_data['correct_answer'], form_data['inchi']))
    conn.commit()
    conn.close()