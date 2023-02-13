import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruity_vice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_list():
    cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    with cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()
 
def insert_fruit_row(fruit_name):
    cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    with cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + fruit_name + "');")
        return 'Thanks for adding ' + fruit_name
        
    
   
streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        fruityvice_response = get_fruity_vice_data(fruit_choice)
        streamlit.dataframe(fruityvice_response)
except URLError as e:
    streamlit.error()
        
if streamlit.button('Get Fruit Load List'): 
    my_fruit_list = get_fruit_list()
    streamlit.dataframe(my_fruit_list)

# allow end user to add a fruit to the list 
add_my_fruit = streamlit.text_input('What fruit you would like to add?')
if streamlit.button('Add a fruit'): 
    fruit_added = insert_fruit_row(add_my_fruit)
    streamlit.write(fruit_added)

streamlit.stop()

