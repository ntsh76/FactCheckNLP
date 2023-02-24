from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from operator import itemgetter
import pandas as pd
import numpy as np
from typing import Optional


def select_evidence_sentences_based_on_cosine_similarity(path_to_corpus, k, output_path,
                                                         samples: Optional[int] = None):
    """
    Select top k evidence sentences based on sentence transformer model.
    :param path_to_corpus:
    :param k:
    :param output_path:
    :param samples:
    :return:
    """

    print("Selects similar statement from text.")
    print(f"Reading from {path_to_corpus}")

    corpus = pd.read_csv(path_to_corpus, sep='\t')
    corpus = corpus[['label', 'subjects', 'claim', 'explanation', 'main_text']]
    corpus['label'] = corpus['label'].str.strip()
    print(f"Before filter {len(corpus)}")

    corpus.dropna(how='any', inplace=True)
    corpus['subjects'] = corpus['subjects'].str.lower()
    corpus.reset_index(inplace=True)
    print(f"After filter {len(corpus)}")

    if samples is not None:
        corpus = corpus.sample(samples, random_state=123)

    sentence_transformer_model = SentenceTransformer('bert-base-nli-mean-tokens')
    corpus['top_k'] = np.empty([len(corpus), ], dtype=str)

    count = 0
    claims = corpus['claim'].values
    texts = corpus['main_text'].values
    top_k_lst = []
    for index in range(0, len(claims)):
        claim = claims[index]
        text = texts[index]

        claim_embedding = sentence_transformer_model.encode(claim)

        sentences = [sentence for sentence in sent_tokenize(text)]
        sentence_embeddings = sentence_transformer_model.encode(sentences)

        cosine_similarity_emb = {}
        for sentence, embedding in zip(sentences, sentence_embeddings):
            cosine_similarity_emb[sentence] = np.linalg.norm(cosine_similarity(
                [claim_embedding, embedding]))

        # select top_k most similar
        top_k = dict(sorted(cosine_similarity_emb.items(),
                            key=itemgetter(1), reverse=True)[:k])
        top_k = ' '.join(key for key in top_k.keys())
        top_k_lst.append(top_k)

    df = pd.DataFrame(
        {'claim': claims,
         'top_k': top_k_lst,
         'label': corpus['label'].values,
         'explanation': corpus['explanation'].values,
         'subjects': corpus['subjects'].values
         })

    print(f"Before filter {len(df)}")
    df = df[(~(df['label'].isna()))]
    print(f"After filter {len(df)}")

    print(f'Writing to {output_path}')
    df.to_csv(output_path, index=False)


def create_claim_sentence_pair(path_to_corpus,  output_path, samples: Optional[int] = None):
    """
    :param path_to_corpus:
    :param k:
    :param output_path:
    :param samples:
    :return:
    """

    print("Selects similar statement from text.")
    print(f"Reading from {path_to_corpus}")

    corpus = pd.read_csv(path_to_corpus, sep='\t')
    corpus = corpus[['label', 'subjects', 'claim', 'explanation', 'main_text']]
    corpus['label'] = corpus['label'].str.strip()
    print(f"Before filter {len(corpus)}")

    corpus.dropna(how='any', inplace=True)
    corpus['subjects'] = corpus['subjects'].str.lower()
    corpus.reset_index(inplace=True)
    print(f"After filter {len(corpus)}")

    if samples is not None:
        corpus = corpus.sample(samples, random_state=123)

    claims = corpus['claim'].values
    texts = corpus['main_text'].values
    labels = corpus['label'].values
    explanation = corpus['explanation'].values

    claim_sentence_pair = []
    for index in range(0, len(claims)):
        claim = claims[index]
        text = texts[index]

        sentences = [sentence for sentence in sent_tokenize(text)]
        for sentence in sentences:
            claim_sentence_pair.append({
                'claim': claim,
                'evidence_sentence': sentence,
                'label': labels[index]
            })

    df = pd.DataFrame(claim_sentence_pair)
    print(f"Before filter {len(df)}")
    df = df[(~(df['label'].isna()))]
    print(f"After filter {len(df)}")

    print(f'Writing to {output_path}')
    df.to_csv(output_path, index=False)

