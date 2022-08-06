import preprocessing
from sklearn.cluster import KMeans

def Clustered_final_df(df):
    df['Cluster_Id'] = None
    #Modift the n_cluster value to get the more detailed clustering
    features = df[['P_Genre','S_Genre','T_Genre']]
    kmean = KMeans(n_clusters=82)
    kmean.fit(features)
    df ['Cluster_Id'] = kmean.predict(features)
    #print(df)
    return df

def cluster_everything(input_movie):
    df = preprocessing.pre_process_all()
    #print(df)
    df = Clustered_final_df(df)
    #print(df)
    df.to_csv('Dataset_to_plot.csv')
    #Check of the movie is present or not:
    input_movie = input_movie.lower()
    try:
        movie_not_found = df.loc[~df['Movie'].str.contains(input_movie)]
        if len(movie_not_found) == 0:
            print('Movie not found')
            return 0
        get_cluster = df ['Cluster_Id'].loc[df['Movie'].str.contains(input_movie)].values[0]
        similar_movies_list = df['Movie'].loc[df['Cluster_Id'] == get_cluster].values
        return similar_movies_list
    except:
        print('Movie not found')
        return 0
#test = cluster_everything('without a paddle')