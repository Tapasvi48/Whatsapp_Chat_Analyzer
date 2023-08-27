import pandas as pd
from urlextract import URLExtract
extract=URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_status(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    words = []
    num_messages=df.shape[0]
    for message in df['message']:
        words.extend(message.split())
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    num_media_message=df[df['message']=="<Media omitted>\n"].shape[0]
    # find most active member in a group
    return num_messages,words,num_media_message,len(links)



def active_users(df):
    x=df['user'].value_counts().head()
    return x


def word_cloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']


    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    temp["message"]=temp["message"].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=""))
    return df_wc



def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emojihelp(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df["message"]:
        emojis.extend(c for c in message if c in emoji.UNICODE_EMOJI['en'])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df








