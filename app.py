import streamlit as st
import preprocessor, help
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # num_messages = help.fetch_stats(selected_user, df)
        # Stats Area
        num_messages, words, num_media_messages, links = help.fetch_stats(selected_user, df)
        # st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)


        # Finding busiest user in a grp
        if selected_user == 'Overall':
            st.title('Most busy People')
            x,new_df = help.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st. columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation ='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

         # wordcloud
        df_wc = help.create_wordcloud(selected_user,df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)



