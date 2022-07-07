from sklearn.model_selection import train_test_split

def load_data(filepath):

    df = pd.read_csv(filepath)
    target = df.columns[-1]
    features = [col for col in df.columns if col not in target]
    X = df[features].values
    y = df[target].values
    labels = df[target].unique().tolist()
    labels.sort()

    train_df, test_df = train_test_split(df, test_size = .30, random_state=42)

    X_train = train_df[features].values
    y_train = train_df[target].values
    X_test = test_df[features].values
    y_test = test_df[target].values


    return labels, features, target, X_train, X_test, y_train, y_test

def read_data(archivo):
    df = pd.read_csv(archivo,header=0)
    #print(df_moodle.columns)
    return df
    
def preprocess_data(df):
    df2=df.copy()
    df2=df2.replace({'PASS': 1, 'FAIL':0})
    df2=df2.drop(['student_id', 'course'], axis=1)    
    return df2

df_moodle=(read_data('data/MoodleSummary.csv'))
df_moodle_p=preprocess_data(read_data('data/MoodleSummary.csv'))
