import streamlit
import pandas
import requests
import snowflake.connector

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
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# Normalized json file
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Displaying dataframe
streamlit.dataframe(fruityvice_normalized)
