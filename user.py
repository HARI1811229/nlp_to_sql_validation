from nlp_sql_validation import SQLProcessor
from nlp_sql_validation import nlp_questions,sql_queries
from NLP_SQL import nlp_sql

# # Example nlp_sql function to be passed into the class
# def nlp_sql(nlp_question: str) -> str:
#     # This function should convert NLP questions to SQL queries
#     # For demonstration, return a dummy SQL query
#     return """SELECT e.first_name, e.last_name, d.department_name
#               FROM employees e
#               JOIN departments d ON e.department_id = d.department_id
#               ORDER BY d.department_name ASC, e.last_name;"""

# Initialize the SQLProcessor class with actual database credentials
processor = SQLProcessor(
    nlp_questions=nlp_questions,
    sql_queries=sql_queries,
    nlp_sql_function=nlp_sql,
    host='127.0.0.1',
    database='Hari',
    user='root',
    password='Hari@1811229'
)
# Run the queries and get comparison results
results, comparison_results = processor.run_queries_and_store_results()
for i in results:
    print(i)

print("comparison_results: ",comparison_results)
