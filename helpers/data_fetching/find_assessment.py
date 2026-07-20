def find_assessment(cursor, user_id):
    query = "SELECT * FROM assessments WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    return row