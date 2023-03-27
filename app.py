import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

df=pd.read_csv('combinedlistings_clean (1).csv')
st.set_page_config(layout="wide")
st.title('Airbnb Chicago')


st.set_option('deprecation.showPyplotGlobalUse', False)
with st.expander('Interesting Insights on Airbnb Chicago'):
  st.write('This app lets the user visualize interesting insights in the Chicago Airbnb Market using Neighbourhood and Review score rating filters')

neighbourhood = st.sidebar.selectbox('Choose a neighbourhood',df['neighbourhood_cleansed'].unique())

rating_var = st.sidebar.slider("Review Scores Rating", float(df.review_scores_rating.min()), float(df.review_scores_rating.max()),(4.5, 5.0))

  #################

st.markdown("Use the Slider for Review Score Rating to find the Neighbourhoods that has the **Maximum supply of Listings** and more **customer Reviews**")
    
top = df.query(f"""review_scores_rating.between{rating_var}""")

groupedDF = top.groupby( "neighbourhood_cleansed", as_index=False ).agg(Average_Number_of_Reviews=('number_of_reviews', \
                                                                    np.mean),CountOfListings=('id', np.size))  
  #st.table(groupedDF)
 
test = alt.Chart(groupedDF,title=f"Neighbourhoods with Maximum Count of Listings and Customer Reviews between Review score Rating Range:{rating_var}").\
  mark_point().encode(
    x='Average_Number_of_Reviews',
    y='CountOfListings',    
    color='neighbourhood_cleansed'
  ).interactive()
st.altair_chart(test, use_container_width=True)

###########################

st.markdown("Select Neighbourhood Filter to see the Average price per Roomtype")
price=df.query(f"""neighbourhood_cleansed==@neighbourhood""")
pricedf=price.groupby(['room_type'],as_index=False).agg(AveragePrice=('price',np.mean)).sort_values('AveragePrice', ascending=False, ignore_index= True)
#st.table(pricedf)
bars = alt.Chart(pricedf,title=f"Average Price by Room Type in **{neighbourhood}**").mark_bar().encode(
      x= alt.X('room_type:N', title='Room Type', sort = '-y' ),      
      y=alt.Y('AveragePrice:Q', title='Average Price')
      )
st.altair_chart(bars, use_container_width=True)


############"#####
st.markdown("Select Neighbourhood Filter to find the **Top Rated Hosts** in the area")

top = df.query(f"""neighbourhood_cleansed==@neighbourhood""")
topdf=top.groupby(['host_name'],as_index=False).agg(NumberOfReviews=('number_of_reviews',np.size))\
    .sort_values('NumberOfReviews',ascending=False,ignore_index=True)
topdf= topdf.head(5)
bars = alt.Chart(topdf,title=f"Top Rated Hosts in **{neighbourhood}**").mark_bar().encode(
      x= alt.Y('NumberOfReviews:Q', title='Number Of Reviews'),      
      y=alt.Y('host_name:N', title='Host',sort = '-x')
      )
st.altair_chart(bars, use_container_width=True)
