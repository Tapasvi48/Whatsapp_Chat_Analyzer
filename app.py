import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')

st.sidebar.title("Whatsapp analyser")
uploaded_file=st.sidebar.file_uploader("Upload a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    #fetch unique
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notifcation')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("user_list",user_list)
    #         in analysis show number of meesage,emoji,time chat,
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_message,num_links=helper.fetch_status(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
          st.header("Total messages")
          st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(len(words))
        with col3:
            st.header("Media shared")
            st.title(num_media_message)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        if selected_user=='Overall':
            st.title("Most Active User")

            x=helper.active_users(df)
            fig,ax=plt.subplots()


            col1,col2=st.columns(2)
            with col1:
                c = ['red', 'yellow', 'purple', 'blue', 'orange']
                ax.bar(x.index, x.values,color=c)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                fig1,ax1=plt.subplots()
                ax1.pie(x.values, labels=x.index, autopct='%1.1f%%')
                st.pyplot(fig1)

#             word cloud
        st.title("Word Cloud")
        df_wc=helper.word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

#         most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most common words")
        st.pyplot(fig)


# emoji anlaysis
        st.title("Emoji Analysis")
        emoji_df=helper.emojihelp(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()

            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)























