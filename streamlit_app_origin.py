## Import list
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

## Function
def get_fruityvice_data(this_fruit_choice):
  streamlit.write('The user entered ', fruit_choice)
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # Normalized json file
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
  return fruityvice_normalized

streamlit.title('My first snowflake API')
streamlit.header("🥣 🥗 🍞 What's next 🐔 🥑")
streamlit.text("First of all i'll have my snowflake certification as a breakfast")
streamlit.text("After that why not dbt certification for lunch")
streamlit.text("And at the end of this year one more azure certification as a diner")
streamlit.text("This is my certification roadmap for 2023")

streamlit.title("🍌🥭 With those meals, i'll of course build these fruits smoothies below 🥝🍇")

# reading our CSV file from the S3 bucket and pull the data into a dataframe we'll call my_fruit_list. 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# setting dataframe index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page. 
streamlit.dataframe(fruits_to_show)

# Calling the Fruityvice API from Our Streamlit App!
streamlit.header("🥣 🥗 🍞 Fruityvice Fruit Advice 🐔 🥑")
try :
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

# Don't run anything past here while we troubleshoot 
streamlit.stop()

# Let's Query Our Trial Account Metadata 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# Let's the fruit_load_list table 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")

# Fetch one record
my_data_row = my_cur.fetchone()
streamlit.header("Retrieval of one of the fruits in the load list")
streamlit.dataframe(my_data_row)

#Fetch all records
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_row)

# Adding a fruit into the list
fruit_to_add = streamlit.text_input('What is the fruit you would like to add?','')
query = "INSERT INTO FRUIT_LOAD_LIST(FRUIT_NAME) VALUES('" + fruit_to_add + "')"
my_cur.execute(query)
streamlit.write('Thanks for adding ', fruit_to_add)
