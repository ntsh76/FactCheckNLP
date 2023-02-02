from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from operator import itemgetter
import pandas as pd
import numpy as np
from typing import Optional


def select_evidence_sentences_based_on_cosine_similarity(path_to_corpus, k, output_path, samples: Optional[int] = None):
    """Select top k evidence sentences based on sentence transformer model."""
    corpus = pd.read_csv(path_to_corpus, sep='\t')
    corpus = corpus[(~(corpus['label'].isna()))]

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

        sentences = [claim] + [
            sentence for sentence in sent_tokenize(text)]

        sentence_embeddings = sentence_transformer_model.encode(sentences)
        claim_embedding = sentence_embeddings[0]
        sentence_embeddings = sentence_embeddings[1:]
        cosine_similarity_emb = {}

        for sentence, embedding in zip(sentences, sentence_embeddings):
            cosine_similarity_emb[sentence] = np.linalg.norm(cosine_similarity(
                [claim_embedding, embedding]))

        top_k = dict(sorted(cosine_similarity_emb.items(),
                            key=itemgetter(1))[:k])
        top_k = ' '.join(key for key in top_k.keys())
        top_k_lst.append(top_k)

    df = pd.DataFrame(columns=['claim', 'top_k', 'label', 'explanation'])
    df['claim'] = claims
    df['top_k'] = top_k_lst
    df['label'] = corpus['label']
    df['explanation'] = corpus['explanation']
    df['subjects'] = corpus['subjects']
    print(f'Writing to {output_path}')
    df.to_csv(output_path, index=False)

