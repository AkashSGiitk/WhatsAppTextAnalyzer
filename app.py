import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np


st.sidebar.title("Whatsapp Chat Analyzer")

# for uploading a file

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    # converting the bytecode to the text-file

    data = bytes_data.decode("utf-8")

    # sending the file data to the preprocess function

    df = preprocess.preprocess(data)

    # displaying the dataframe

    # st.dataframe(df)

    user_list = df['User'].unique().tolist()

    # removing group notification

    user_list.remove('Group Notification')

    user_list.sort()

    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis of", user_list)

    st.title("WhatsApp Chat Analysis for " + selected_user)
    if st.sidebar.button("Show Analysis"):

        # getting stats of the selected user from stats script

        num_messages, num_words, media_omitted, links = stats.fetch_stats(
            selected_user, df)

        # basic stats

        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total No. of Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(media_omitted)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        # finding the busiest users

        if selected_user == 'Overall':

            # dividing space into two columns
            # bar chart and dataframe

            st.title('Most Busy Users')
            busycount, newdf = stats.fetch_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.beta_columns(2)
            with col1:
                ax.bar(busycount.index, busycount.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(newdf)

        # Word Cloud

        st.title("Word Cloud")
        df_img = stats.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)

        # most common words in the chat

        most_common_df = stats.get_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)

        # Emoji Analysis

        emoji_df = stats.get_emoji_stats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']

        st.title("Emoji Analysis")

        col1, col2 = st.beta_columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emojicount = list(emoji_df['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)

        # Monthly timeline

        st.title("Monthly Timeline")
        time = stats.month_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        # Activity maps

        st.title("Activity Maps")

        col1, col2 = st.beta_columns(2)

        with col1:

            st.header("Most Busy Day")

            busy_day = stats.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.header("Most Busy Month")

            busy_month = stats.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)