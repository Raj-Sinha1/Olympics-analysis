
import numpy as np

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport',
                          'Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver',
                         'Bronze']].sort_values('Year',
                                                ascending=True).reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver',
                         'Bronze']].sort_values('Gold',
                                                ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']
    
    return(x)

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.insert(0,'Overall')

    return years,country

def data_over_time(df,column):
    data_over_years=df.drop_duplicates(['Year',column])['Year'].value_counts().reset_index().sort_values('Year')

    return data_over_years

def most_successfull(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    
    if(sport != 'Overall'):
        temp_df=temp_df[temp_df['Sport']==sport]
    return temp_df['Name'
                  ].value_counts().reset_index().merge(df,on='Name',how='left').drop_duplicates('Name')[['Name','count','Sport','region']].rename(columns={'count':'Medals','region':'Nationality'}).reset_index().drop(columns='index').head(15)

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    new_df=df.dropna(subset=['Medal'])

    performance_df=f=new_df[new_df['region']==country]


    performance_df=performance_df.drop_duplicates(subset=['Team','Year',
                                                        'Sport','Event','Medal'])
    performance_df=performance_df.pivot_table(index='Sport',
                                          columns='Year',values='Medal',
                                          aggfunc="count").fillna(0).astype('int')
    
    return performance_df

def most_successfull_country_wise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country]
    return temp_df['Name'
                  ].value_counts().reset_index().merge(df,on='Name',how='left').drop_duplicates('Name')[['Name','count','Sport',]].rename(columns={'count':'Medals','region':'Nationality'}).reset_index().drop(columns='index').head(10)   

def athlete_age_analysis(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    age=athlete_df['Age'].dropna()
    gold=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    silver=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    bronze=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    return age,gold,silver,bronze


def age_medal_distribution(df,medal='Gold'):
    famous_sports=df['Sport'].unique().tolist()
    athlete_df=df.drop_duplicates(subset=['Name','region','Year'])
    famous_sports.sort(reverse=True)
    age_df_list=[]
    name_sports=[]

    for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            gold_ages=temp_df[temp_df['Medal'] == medal]['Age'].dropna()
            
            if gold_ages.value_counts().count()>1:  
                age_df_list.append(gold_ages)
                name_sports.append(sport)
    
    return age_df_list, name_sports


def athlete_wt_vs_ht(df,sport='Overall'):

    athlete_df=df.drop_duplicates(subset=['Name','region','Year'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':
        athlete_df=athlete_df[athlete_df['Sport']==sport]
    else:
        return athlete_df
    return athlete_df

def men_vs_women(df):

    athlete_df=df.drop_duplicates(subset=['Name','region','Year'])
    men_df=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()

    women_df=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final_df=men_df.merge(women_df,on='Year',how='left').fillna(0).astype('int')

    final_df.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)

    return final_df