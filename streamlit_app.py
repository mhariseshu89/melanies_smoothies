# Import python packages
import streamlit as st
import pandas as pd_df

from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!).
    """
)



#import streamlit as st
name_on_order=st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

#title =st.text_input('Movie title', 'Life of Brian')
#st.write('The current movie title is', title)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list =st.multiselect(
	'Choose up to 5 ingredients:', my_dataframe)

if ingredients_list :
    st.write(ingredients_list)
    st.text(ingredients_list)
    
ingredients_string=''

for fruit_chosen in ingredients_list:
    ingredients_string+=fruit_chosen +' '

st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

#st.write(my_insert_stmt)
#st.stop()
time_to_insert =st.button('Submit Order')

if time_to_insert:
    
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


















