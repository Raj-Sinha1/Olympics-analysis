import pandas as pd


def change(value):
    if value==True:
        return 1
    else:
        return 0

def preprocess(df,region_df):

    df=df[df['Season']=='Summer']
    
    # df['Year']=df['Year'].astype(object)        


    df=df.merge(region_df,on='NOC',how='left')

    df.drop_duplicates(inplace=True)

    x=pd.get_dummies(df['Medal'])

    x['Gold']=x['Gold'].apply(change)

    x['Silver']=x['Silver'].apply(change)

    x['Bronze']=x['Bronze'].apply(change)

    df=pd.concat([df,x],axis=1)

    return df

