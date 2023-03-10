from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch
from transformers import DistilBertModel, DistilBertTokenizer
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np
import nltk
from .train import DistillBERTClass

nltk.download('punkt')

class ExplanationModel:
    def __init__(self, model_path):
        self.tokenizer = PegasusTokenizer.from_pretrained(model_path)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_path)

    def predict(self, input_text) -> str:
        inputs = self.tokenizer(input_text, return_tensors="pt").input_ids
        outputs = self.model.generate(inputs,
                                      do_sample=True,
                                      max_length=50,
                                      top_k=50,
                                      top_p=0.95,
                                      num_return_sequences=1)

        for i, sample_output in enumerate(outputs):
            pred_text = self.tokenizer.decode(sample_output, skip_special_tokens=True)

        return pred_text


class ClaimClassificationModel:
    def __init__(self, model_path):
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = DistillBERTClass()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        self.sentence_transformer_model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.max_len = 512
        self.id_to_label = {0: "true", 1: "false", 2: "mixture", 3: "unproven"}

    def _find_top_k(self, claim_text, evidence_text, k=5):
        claim_embedding = self.sentence_transformer_model.encode(claim_text)

        sentences = [sentence for sentence in sent_tokenize(evidence_text)]
        sentence_embeddings = self.sentence_transformer_model.encode(sentences)

        cosine_similarity_emb = {}
        for sentence, embedding in zip(sentences, sentence_embeddings):
            cosine_similarity_emb[sentence] = np.linalg.norm(cosine_similarity(
                [claim_embedding, embedding]))

        # select top_k most similar
        top_k = dict(sorted(cosine_similarity_emb.items(),
                            key=itemgetter(1), reverse=True)[:k])
        top_k = ' '.join(key for key in top_k.keys())
        return top_k

    def predict(self, claim_text: str, evidence_text: str) -> str:
        top_k = self._find_top_k(claim_text.lower(), evidence_text.lower())
        input_text = str(claim_text.lower() + " " + top_k.lower())
        input_text = " ".join(input_text.split())
        inputs = self.tokenizer.encode_plus(
            input_text,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            pad_to_max_length=True,
            return_token_type_ids=True,
            truncation=True
        )
        ids = torch.tensor([inputs['input_ids']], dtype=torch.long)
        mask = torch.tensor([inputs['attention_mask']], dtype=torch.long)

        outputs = self.model(ids, mask).squeeze()
        pred_prob = torch.max(outputs.data).item()
        pred_label = torch.argmax(outputs.data).item()
        conf = torch.max(torch.softmax(outputs.data, 0)).item()


        return conf, self.id_to_label[pred_label]
