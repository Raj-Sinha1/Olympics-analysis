import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('Olympic_logo.png')

user_menu=st.sidebar.radio(
    label='Select an Option',options=('Medal Tally','Overall Analysis','Country-wise Analysis',
    'Athlete wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Country wise overall tally")
    elif(selected_year!='Overall' and selected_country=='Overall'):
        st.title(f'Medal tally in the {selected_year}\'s summer olympics.')
    elif(selected_year=='Overall' and selected_country!='Overall'):
        st.title(f'{selected_country}\'s medal tally over the years.')
    else:
        st.title(f'{selected_country}\'s medal tally in the {selected_year}\'s summer olympics.')
        
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1

    cities=df['City'].unique().shape[0]

    sports=df['Sport'].unique().shape[0]

    events=df['Event'].unique().shape[0]

    athletes=df['Name'].unique().shape[0]

    nations=df['region'].unique().shape[0]

    st.title("Top statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time=helper.data_over_time(df,'region')
    nations_over_time.rename(columns={'Year':'Edition','count':'No. of participating countries'},inplace=True)
    fig=px.line(nations_over_time,x='Edition',y='No. of participating countries',markers='o')
    fig.update_traces(line_color='#0000ff')

    st.title('Participating nations over the years')
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    events_over_time.rename(columns={'Year':'Edition','count':'No. of Events held'},inplace=True)
    fig=px.line(events_over_time,x='Edition',y='No. of Events held',markers='o')
    fig.update_traces(line_color='#0000ff')

    st.title('No. of events held over the years')
    st.plotly_chart(fig)

    athelets_over_time=helper.data_over_time(df,'Name')
    athelets_over_time.rename(columns={'Year':'Edition','count':'No. of participants'},inplace=True)
    fig=px.line(athelets_over_time,x='Edition',y='No. of participants',markers='o')
    fig.update_traces(line_color='#0000ff')

    st.title('No. of participants over the years')
    st.plotly_chart(fig)

    st.title("No. of events held in a sport over time")

    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc="count").fillna('0').astype('int'),annot=True)

    st.pyplot(fig)


    st.title('Most Successfull Athletes')

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selcted_sport=st.selectbox(label='Select a Sport', options=sport_list)
    most_successfull=helper.most_successfull(df,selcted_sport)

    st.table(most_successfull)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal",markers='o')
    st.title(selected_country + "\'s Medal Tally over the years")
    st.plotly_chart(fig)


    st.title(f'{selected_country}\'s Performace Heatmap')
    performance_df=helper.country_event_heatmap(df,selected_country)

    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(performance_df,annot=True)

    st.pyplot(fig)

    st.title(f'{selected_country}\'s Best Athletes')
    country_wise_top=helper.most_successfull_country_wise(df,selected_country)

    st.table(country_wise_top)

if user_menu=='Athlete wise Analysis':
    st.title('Age Distribution')

    age,gold,silver,bronze=helper.athlete_age_analysis(df)

    figure=ff.create_distplot([age,gold,silver,bronze],
                          ['Overall Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,
                          show_rug=False)
    
    figure.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(figure)

    st.title('Age Distribution With Respect To Sports')

    selcted_medal=st.selectbox(label='Select a Medal', options=['Gold','Silver','Bronze'])

    sports=df['Sport'].unique().tolist()

    age_df,sports_name_list=helper.age_medal_distribution(df,selcted_medal)

    figure=ff.create_distplot(age_df, sports_name_list, show_hist=False, show_rug=False)
    figure.update_layout(autosize=False,width=1000,height=600)

    st.plotly_chart(figure)


    st.title('Weight V/S Height Analysis')

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox(label='Select a sport',options=sport_list )
    athlete_df=helper.athlete_wt_vs_ht(df,selected_sport)

    # fig,ax=plt.subplots()
    # ax=sns.scatterplot(x=athlete_df['Weight'],y=athlete_df['Height'],hue=athlete_df['Medal'],style=athlete_df['Sex'],s=60)
    # st.pyplot (fig)

    fig=px.scatter(athlete_df,x = "Weight",y = "Height",color = "Medal",symbol='Sex',opacity=0.7)
    fig.update_layout(autosize=False,width=1000,height=600)
    fig.update_traces(marker={'size': 8})
    st.plotly_chart(fig)

    st.title('Men v/s Women Participation Comparison')

    men_v_women_df=helper.men_vs_women(df)

    fig=px.line(men_v_women_df,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)