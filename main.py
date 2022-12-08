import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title='Mathias Rostagno\'s Board Game Analysis')
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://srsdubai.ae/wp-content/uploads/2022/04/Board-Games.jpg");
             background-attachment: fixed;
             background-size: cover;
             background-color: rgba(255,255,255,0.6);
             background-blend-mode: lighten;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

df = pd.read_csv('Data/bgg_dataset.csv', sep=';', decimal=',')

st.markdown("<h1 style='text-align: center; color: Black;'>Board Game Analysis</h1>", unsafe_allow_html=True)

with st.expander('Introduction', expanded = True):
    st.markdown("<h2 style='text-align: center; color: black'>Introduction</h2>", unsafe_allow_html=True)
    st.markdown('##### BoardGameGeek (BGG) is an online forum for board gaming hobbyists and a game database '
                'that holds reviews, images and videos for over 125,600 different tabletop games, including '
                'European-style board games, wargames, and card games. In addition to the game database, '
                'the site allows users to rate games on a 1–10 scale and publishes a ranked list of board games.')
    st.markdown('##### In this project i will perform an exploratory data analysis with a sample of the first 20K ranked games')

    col1, col2 = st.columns(2)
    col1.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/BoardGameGeek_Logo.svg/440px-BoardGameGeek_Logo.svg.png")
    col2.markdown("![Alt Text](https://i.gifer.com/HNaD.gif)")

with st.expander('Modules Loading & Importing Data'):
    st.markdown("<h2 style='text-align: center; color: black'>Modules Loading & Importing Data</h2>", unsafe_allow_html=True)
    if st.checkbox('1. Modules Loading', label_visibility = 'Visible'):
        code1 = '''import streamlit as st \nimport pandas as pd \nimport io'''
        st.code(code1, language='python')
    if st.checkbox('2. Importing Data'):
        code2 = '''df = pd.read_csv('Data/bgg_dataset.csv', sep=';', decimal=',')'''
        st.code(code2, language='python')
    if st.checkbox('3. Show Data'):
        st.dataframe(df)

with st.expander('Basic Exploration'):
    st.markdown("<h2 style='text-align: center; color: black'>Basic Exploration</h2>", unsafe_allow_html=True)
    st.write('Total number of games :', len(df))
    if st.checkbox("1. Head"):
        st.dataframe(df.head())
    if st.checkbox("2. Info"):
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        st.markdown('**From the above informations, we can see that :**')
        st.markdown('- There are some missing values in several columns (ID, Year Published, Owned Users)')
        st.markdown('- The two columns "Mechanics" and "Domains" have missing values but we can keep it')
        st.markdown("- Year Published is not a Datetime Object, but we can work with that")
        st.markdown('- In order to gain a little bit of memory usage we can modify some columns types')
    if st.checkbox('3. Describe'):
        st.write(df.describe())
        st.markdown('**From the above informations, we can see that :**')
        st.markdown("- Some games have 'Max Players' equal to 0 and others equal to 999")
        st.markdown("- Some games have a 'Play Time' equal to 60.000 seconds")
        st.markdown("- Some games have a 'Year Published' equal to 0, not because they were released at Year 0, but because Year is not reported")
        st.markdown("- The range of 'Year Published' is between -3500 BC and 2022 !")
    if st.checkbox('4. Explore Oldest Games'):
        df_year_sorted = df.sort_values(by=['Year Published'], ascending=False)
        st.dataframe(df_year_sorted.tail(10))
        st.markdown("- As we can see, there are some pretty popular games here !")
        st.markdown("- The game of Go is still very popular, has a very good rating, is owned by a lot of people although it has been released more than 4200 year ago !")

df = df[df['Year Published'].notna()]
df = df.loc[~(df['Year Published'] == 0)]
df = df[df['Owned Users'].notna()]
df = df[df['ID'].notna()]
df['Age'] = 2022 - df['Year Published']
df = df.astype({'ID': 'int64', 'Year Published': 'int64', 'Owned Users': 'int64'})
df['Mechanics'] = df['Mechanics'].fillna('Unknown')
df['Domains'] = df['Domains'].fillna('Not Communicated')
Sample = (df[(df.Mechanics == 'Unknown') & (df.Domains == 'Not Communicated')]).sample(10)
df['Mechanics'] = df['Mechanics'].str.replace('/', ',')
df['Mechanics'] = df['Mechanics'].str.replace(':', ',')
df['Domains'] = df['Domains'].str.replace('/', ',')
df['Domains'] = df['Domains'].str.replace(':', ',')

with st.expander('Data Cleaning'):
    st.markdown("<h2 style='text-align: center; color: black'>Data Cleaning</h2>", unsafe_allow_html=True)
    if st.checkbox('1. Drop NA / 0 Values'):
        st.markdown("Let's drop 0 and NA values from the 'Year Published' column and drop NA values from 'Owned Users' and 'ID' columns")
        code3 = '''df = df[df['Year Published'].notna()] \ndf = df.loc[~(df['Year Published'] == 0)] \ndf = df[df['Owned Users'].notna()] \ndf = df[df['ID'].notna()]'''
        st.code(code3, language='python')
    if st.checkbox('2. Converting columns type'):
        st.markdown('We convert ID, Year Published and Owned Users columns into int64')
        code5 = '''df.astype({'ID': 'int64', 'Year Published': 'int64', 'Owned Users': 'int64'})'''
        st.code(code5, language='python')
    if st.checkbox('3. Replace NA Values'):
        st.markdown("Replacing NA Values in Mechanics's column by 'Unknown' and Domains's columns by 'Not Communicated'")
        code6 = '''Mechanics_NA = df[df['Mechanics'].isna()] \nDomains_NA = df[df['Domains'].isna()] \ndf['Mechanics'] = df['Mechanics'].fillna('Unknown') \ndf['Domains'] = df['Domains'].fillna('Not Communicated')'''
        st.code(code6, language='python')
        st.markdown("Here is a random sample where the two columns contains both 'Unknown' and 'Not communicated' mention :")
        st.dataframe(Sample)
    if st.checkbox("4. Cleaning 'Mechanics' and 'Domains'"):
        st.markdown("Both Mechanics and Domains columns defines the game type, and have often multiple values separated by comas, but sometimes other characters.")
        st.markdown("Let's clean this by replacing '/' and ':' with comas ','")
        code7 = '''df['Mechanics'] = df['Mechanics'].str.replace('/', ',') \ndf['Mechanics'] = df['Mechanics'].str.replace(':', ',') \ndf['Domains'] = df['Domains'].str.replace('/', ',') \ndf['Domains'] = df['Domains'].str.replace(':', ',')'''
        st.code(code7, language='python')
    if st.checkbox('4. Creating Age column'):
        st.markdown("Year published is not a very convenient for future analysis, so let's create a new column 'Age'")
        code4 = '''df['Age'] = 2022 - df['Year Published']'''
        st.code(code4, language='python')
    if st.checkbox('5. Cleaned Dataframe'):
        st.dataframe(df)

with st.expander('Data Exploration'):
    st.markdown("<h2 style='text-align: center; color: black'>Data Exploration</h2>", unsafe_allow_html=True)