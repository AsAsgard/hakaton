import pandas as pd
from annoy import AnnoyIndex


def get_index(text, annoy_model):
    normed = get_avg_vector(get_good_text(text))
    annoy_res = annoy_model.get_nns_by_vector(normed, 10)
    return annoy_res

def get_results(idx, df):
    titles = df['title'][idx].values
    product_ids = df['product_id'][idx].values
    imgs = df['image_links'][idx].values
    res = []
    for title, ix, img in zip(titles, product_ids, imgs):
        link = None in img == 'nan' else img
        tmp = {'title': title, 'product_id': ix, 'image': link}
        res.append(tmp)    
    
    return res

def process_data(input_text, annoy_model, df):
    idx = get_index(input_text, annoy_model)
    return get_results(idx, df)



