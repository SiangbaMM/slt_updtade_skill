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

def get_snowflake_connection():
  return snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

def get_trial_account_metadata(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    return my_cur.fetchone()
 
def add_fruit_into_fruit_list(my_cnx, fruit_to_add):
  try:
    with my_cnx.cursor() as my_cur:
      query = "INSERT INTO FRUIT_LOAD_LIST(FRUIT_NAME) VALUES('" + fruit_to_add + "')"
      my_cur.execute(query)
      streamlit.write('Thanks for adding ', fruit_to_add)
  except as e:
    streamlit.error(e)

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

# Let's Query Our Trial Account Metadata 
streamlit.header("Let's Query Our Trial Account Metadata")
my_cnx =  get_snowflake_connection()
if streamlit.button("Get trial account metadata"):
  my_data_row = get_trial_account_metadata(my_cnx)
  streamlit.text(my_data_row)

# Don't run anything past here while we troubleshoot 
streamlit.stop()

# Let's the fruit_load_list table 
streamlit.header("The fruit load list contains")
if streamlit.button("Get trial account metadata"):
  my_data_row = get_fruit_load_list(my_cnx)
  streamlit.dataframe(my_data_row)

# Adding a fruit into the list
fruit_to_add = streamlit.text_input('What is the fruit you would like to add?','')
add_fruit_into_fruit_list(fruit_to_add)
