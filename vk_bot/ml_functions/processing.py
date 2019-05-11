import pandas as pd
from annoy import AnnoyIndex
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords


nltk.download("stopwords")
sw = stopwords.words("russian")


def load_w2v_model(path_to_model):
    return KeyedVectors(300).load(path_to_model)


def load_annoy_model(path_to_model):
    annoy_model = AnnoyIndex(300)
    annoy_model.load(path_to_model)
    return annoy_model


def load_dataset(path_to_data):
    df = pd.read_csv(path_to_data)
    df['title'].fillna('nan', inplace=True)
    df['descrirption'].fillna('nan', inplace=True)
    df['product_id'] = range(df.shape[0])
    return df


def get_tfidf_model(df):
    vec = TfidfVectorizer(stop_words=sw)
    vec.fit_transform(df['all_desc'])
    return vec
