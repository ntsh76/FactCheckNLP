from utils.fact_check_nlp.predict import ExplanationModel, ClaimClassificationModel


CLAIM_MODEL_PATH = '/tmp/claim_classification_true_false_distillbert'
EXPLANATION_MODEL_PATH = '/tmp/explanation-generation-peagusus-256-64'

claim_model = ClaimClassificationModel(CLAIM_MODEL_PATH)
explanation_model = ExplanationModel(EXPLANATION_MODEL_PATH)


def model(claim, source):
    confidence, result = claim_model.predict(claim_text=claim, evidence_text=source[:512])
    explanation = explanation_model.predict(source[:512])
    return result == 'true', confidence, explanation


if __name__ == "__main__":
    claim_text = "Claim is true"
    evidence_text = "Claim is false. Claim is incorrect. Claim is wrong. Claim is bad. Claim is unproven"
    prediction = claim_model.predict(claim_text=claim_text, evidence_text=evidence_text)
    print(prediction)
