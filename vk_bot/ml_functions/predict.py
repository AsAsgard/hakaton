import pandas as pd
import numpy as np
import re
from functools import lru_cache
import pymorphy2
from ml_functions.processing import *

morph = pymorphy2.MorphAnalyzer()
w2v = load_w2v_model('./data/w2v/my_model')
annoy_model = load_annoy_model('./data/annoy')
df = load_dataset('./data/ProductsDataset.csv')

@lru_cache(maxsize=1000000)
def get_normal_form(i):
    return morph.normal_forms(i)[0]

def normalize_text(x):
    return ' '.join([get_normal_form(i) for i in re.findall('\w+', x)])

def rem_spaces(x):
    return re.sub(' +', ' ', x).strip()

def rem_punctuation(x):
    return re.sub('[^A-Za-zА-Яа-я0-9 ]+', '', x)

def get_good_text(x):
    return rem_punctuation(rem_spaces(normalize_text(x)))


df['title_proc'] = df['title'].apply(get_good_text)    
df['descrirption'] = df['descrirption'].apply(get_good_text)
df['all_desc'] = df['title_proc'] + ' ' + df['descrirption']

vec = get_tfidf_model(df)


def get_avg_vector(text):
    splitted = text.split()
    length = len(splitted)
    tmp = np.zeros((length, 300))
    idfsum = 0
    for i in range(length):
        ix = vec.vocabulary_.get(splitted[i], None)
        if not ix is None:
            idf = vec.idf_[ix]
        else:
            idf = 1
        idfsum += idf
        try:
            tmp[i] = w2v[splitted[i]] * idf
        except KeyError:
            continue
    return tmp.sum(axis=0) / idfsum


def get_index(text):
    normed = get_avg_vector(get_good_text(text))
    annoy_res = annoy_model.get_nns_by_vector(normed, 10)
    return annoy_res

def get_results(idx):
    titles = df['title'][idx].values
    product_ids = df['product_id'][idx].values
    imgs = df['image_links'][idx].values
    res = []
    for title, ix, img in zip(titles, product_ids, imgs):
        link = None if img == 'nan' else img
        tmp = {'title': title, 'product_id': ix, 'image': link}
        res.append(tmp)    
    
    return res

def process_data(input_text):
    idx = get_index(input_text)
    return get_results(idx)
