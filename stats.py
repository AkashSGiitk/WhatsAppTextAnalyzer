from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):

    # make changes for specific user

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # counting the number of media files shared

    media_omitted = df[df['Message'] == '<Media omitted>']

    # number of links shared

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), media_omitted.shape[0], len(links)


# most busy user {group level}

def fetch_busy_user(df):

    df = df[df['User'] != 'Group Notifications']
    count = df['User'].value_counts().head()

    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, newdf


def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500,
                   min_font_size=10, background_color='white')

    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return df_wc


# get most common words (dataframe of word frequency)

def get_common_words(selected_user, df):

    # getting the stopwords

    file = open('stop_hinglish.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[(df['User'] != 'Group Notification') |
              (df['User'] != '<Media omitted>')]

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


def get_emoji_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI_ENGLISH])

    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojidf


def month_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))

    temp['Time'] = time

    return temp


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()
