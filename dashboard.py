import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("""
### This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦 about US Airlines.
""")
st.sidebar.markdown("""
This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦""")

# Load data

DATA_URL= "https://raw.githubusercontent.com/cysorianoc/STREAMLIT_DASHBOARD_AIRLINES/refs/heads/main/Tweets.csv"
# we need to add the cache to load the data only once
# so it will run only once per session
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data= load_data()

# Display the data
# st.write(data)

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
#st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])
st.sidebar.markdown(data[data['airline_sentiment'] == random_tweet]['text'].sample(n=1).iloc[0])

st.sidebar.markdown(" #### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='1')
# key is used to assign a unique identifier to the widget
sentiment_count = data['airline_sentiment'].value_counts()

# we can ru the code below to show the dataframe
#st.write(sentiment_count)

sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

        
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == 'Histogram':
        # Fix column names for the bar chart
        bar_data = data['airline_sentiment'].value_counts().reset_index()
        bar_data.columns = ['Sentiment', 'Tweets']  # Rename columns for clarity
        fig = px.bar(bar_data, x='Sentiment', y='Tweets', color='Tweets',
                     labels={'Sentiment': 'Sentiment', 'Tweets': 'Number of Tweets'},
                     height=500)
        st.plotly_chart(fig)
    else:
        # Fix column names for the pie chart
        pie_data = data['airline_sentiment'].value_counts().reset_index()
        pie_data.columns = ['Sentiment', 'Tweets']  # Rename columns for clarity
        fig = px.pie(pie_data, names='Sentiment', values='Tweets',
                     labels={'Sentiment': 'Sentiment', 'Tweets': 'Number of Tweets'})
        st.plotly_chart(fig)



st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", min_value=1, max_value=24)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close", True, key='2'):
    st.markdown("### Tweets location based on the hour of the day")
    tweet_count = len(modified_data)  # Number of tweets in the filtered data
    start_hour = hour  # Starting hour
    end_hour = (hour + 1) % 24  # Ending hour (wraps around at 24)
    st.markdown(f"{tweet_count} tweets between {start_hour}:00 and {end_hour}:00")

    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='3')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count',
                              color='airline_sentiment', facet_col='airline_sentiment',
                              labels={'airline': 'Airlines', 'airline_sentiment': 'Number of Tweets'},
                              height=600, width=800)
    st.plotly_chart(fig_choice)
    
    
st.sidebar.subheader("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))   
if not st.sidebar.checkbox("Close", True, key='4'):
    st.markdown(f"### Word cloud for {word_sentiment} sentiment")
    
    # Filter data for the selected sentiment
    sentiment_data = data[data['airline_sentiment'] == word_sentiment]
    
    # Combine all text into a single string
    all_words = ' '.join(sentiment_data['text'])
    
    # Remove unwanted words and links
    cleaned_words = ' '.join(word for word in all_words.split() 
                              if not word.startswith(('http', '@')) and word != 'RT')
    
    # Generate the word cloud
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', 
                          height=640, width=800).generate(cleaned_words)
    
    # Display the word cloud
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Hide axes
    st.pyplot(fig)
    
    