import streamlit
import pandas
import requests

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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
