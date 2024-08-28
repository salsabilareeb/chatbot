import pandas as pd
import sqlite3
import openai

openai.api_key = "write your openai api key"
print("Share DB path:")
db_path = input()

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object
cursor = conn.cursor()

# Get the table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# Print the table names
print("Tables in the shared database:")
for i, table in enumerate(table_names):
    print(f"{i + 1}. {table[0]}")

# Ask user to select a table
selected_table = None
while selected_table is None:
    choice = input("Enter the number of the table you want to work on (or 'no' to exit): ")
    if choice.lower() == "no":
        break
    try:
        table_index = int(choice) - 1
        if 0 <= table_index < len(table_names):
            selected_table = table_names[table_index][0]
        else:
            print("Invalid table number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number or 'no'.")

if selected_table:
    print(f"You selected the table '{selected_table}'.")

    # Fetch columns of the selected table
    cursor.execute(f"PRAGMA table_info({selected_table});")
    columns_info = cursor.fetchall()

    # Extract column names and store them in a list
    column_names = [col[1] for col in columns_info]

    #print("Columns in the selected table:")
    #for column in column_names:
        #print(column)

# Close the cursor and connection
cursor.close()
conn.close()

#db_path = 'F:\\NEU\\2nd Quarter\\ALY 6070\\Assignment 3 Group\\texas.db'

# Function to execute a SQL query and return the results
def execute_sql_query(db_path, query):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            #print(results)
            return results
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return None

def chat_with_gpt(prompt):
    # Send the prompt to the GPT-3.5 Turbo model
    # Make sure to handle exceptions and manage the API key securely
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        #print(response.choices[0].message["content"])
        return response.choices[0].message["content"]
    except Exception as e:
        print("An error occurred while calling the API:", e)
        return None

def preprocess_input(user_input):
    # Define the prefix
    prefix = "Give only sql query and nothing else no comment for table 'th' with column as 'city', 'X', 'year', 'month', 'sales', 'volume', 'median', 'listings', 'inventory', 'date', 'latitude', 'longitude' also please interpret the question it could be a little different from column names. The Question is:"
    sufix = ". in dabase?"
    # Add the prefix to the user input
    manipulated_input = prefix + user_input + sufix
    # Return the manipulated input
    #print(manipulated_input)
    return manipulated_input

def generate_response(question, results):
    #print('check 1', results)
    if '*' in sql_query:
        # Mapping for column names
        columns = ['city', 'X', 'year', 'month', 'sales', 'volume', 'median', 'listings', 'inventory', 'date',
                   'latitude', 'longitude']
        # Combine the question and answer
        prompt = f"{question} The answer is: {results} corresponding values are {columns} give ans based on this info only"
        # Send the combined prompt to GPT-3.5 for refinement
        refined_response = chat_with_gpt(prompt)
        #print(refined_response)
        #print (prompt)
        return refined_response
    else:
        prompt = f"{question} The answer is: {results}"
        #print('inside generate', results)
        # Send the combined prompt to GPT-3.5 for refinement
        refined_response = chat_with_gpt(prompt)
        #print(refined_response)
        #print (question,results)
        #print (prompt)
        return refined_response


if __name__ == "__main__":
    #db_path = 'F:\\NEU\\2nd Quarter\\ALY 6070\\Assignment 3 Group\\texas.db'
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        manipulated_input = preprocess_input(user_input)
        sql_query = chat_with_gpt(manipulated_input)

        if sql_query:
            results = execute_sql_query(db_path, sql_query)
            if results:
                # Assuming the user input is the question
                question = user_input
                # Assuming the first result is the answer
                answer = results[0]
                refined_response = generate_response(question, answer)
                print("Irfan:", refined_response)
                #print(sql_query)
                #print(results)
            else:
                print("No results found or an error occurred.")
