from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer


def read_data(archivo):
    """
    It reads a csv file and returns a dataframe
    
    :param archivo: the name of the file you want to read
    :return: A dataframe
    """
    df = pd.read_csv(archivo,header=0)
    return df
    
def preprocess_data(df):
    """
    The function takes a dataframe as input, and returns a dataframe with the first column as the
    student ID, the second column as the student's performance, and the remaining columns as the
    student's activity levels. The activity levels are binned into three categories: LOW, MEDIUM, and
    HIGH
    
    :param df: the dataframe
    :return: A dataframe with the columns:
    """
    df2=df.iloc[1:, 1:-1].copy()
    columns=df2.columns.values
    enc=KBinsDiscretizer(n_bins=3,encode='ordinal', strategy='uniform')
    enc.fit(df2)
    df2=enc.transform(df2)
    df2=pd.DataFrame (df2, columns = columns)
    df_merged = pd.concat([df.iloc[:,0], df2, df.iloc[:,-1]], axis=1, join='inner')
    df_merged=df_merged.replace({0:'LOW', 1:'MEDIUM', 2:'HIGH'})
    return df_merged

