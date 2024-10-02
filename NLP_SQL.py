from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
key_path =""
credentials = Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
if credentials.expired:
    credentials.refresh(Request())
PROJECT_ID = 'hari-practice'
REGION = 'us-central1'

import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]
import mysql.connector
import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting


# Function to connect to MySQL and get table information
def get_table_and_column_info(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION;
        """
        database_name = connection.database
        cursor.execute(query, (database_name,))
        columns_info = cursor.fetchall()
        table_column_info = {}
        for table_name, column_name, data_type in columns_info:
            if table_name not in table_column_info:
                table_column_info[table_name] = {}
            table_column_info[table_name][column_name] = data_type
        return table_column_info
    except mysql.connector.Error as e:
        print(f"Error fetching table and column information: {e}")
        return {}
    finally:
        cursor.close()


# Function to initialize Google Vertex AI and generate SQL query
def generate(prompt):
    vertexai.init(project=PROJECT_ID, location=REGION, credentials=credentials)
    model = GenerativeModel("gemini-1.5-pro-002")
    responses = model.generate_content(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    res = ""
    for response in responses:
        res += response.text
    return res


# Function to convert NLP question to SQL
def nlp_sql(question: str) -> str:
    # MySQL connection parameters
    connection = mysql.connector.connect(
        host='127.0.0.1',  # Replace with your host (e.g., 'localhost')
        database='Hari',  # Replace with your database name
        user='root',  # Replace with your MySQL username
        password='Hari@1811229'  # Replace with your MySQL password
    )

    if connection.is_connected():
        table_info = get_table_and_column_info(connection)

    prompt = f"""
        You are an expert in converting the given English questions directly into SQL code.
        Question: {question}

        Use the following MySQL Database information to craft the query:
        {table_info}

        Only return the SQL query in JSON format where the key is "sql" and the value is the SQL code. Do not include any explanations, comments, or extra text.

        Example:
        Question: Which customers have placed orders with an amount greater than $3000?
        Output: {{
            "sql": "SELECT c.customer_name, o.order_date, o.amount FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.amount > 3000;"
        }}

        Provide the SQL query in JSON format for the question below:
    """

    sql = generate(prompt)
    sql = sql.replace("```json", "").replace("```", "").strip()
    sql_data = json.loads(sql)
    sql_code = sql_data["sql"]

    if connection.is_connected():
        connection.close()

    return sql_code
#
#
# # Example usage
# question = "Which department has the highest average salary?"
# sql_query = nlp_sql(question)
# print(sql_query)
