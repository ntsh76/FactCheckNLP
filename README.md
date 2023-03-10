# FactCheckNLP

This repository is intended to be used to NLP project development for creating a fact checking model. 

# Data

We use the PUBHEALTH dataset (https://github.com/neemakot/Health-Fact-Checking repo)

# Pre-processing 

Currently it only contains pre-processing code and a dummy model to verify dependencies.

# Starting with code

Download data from google drive link if you have access. Then start working with the notebook src/NLPNotebook
The training code is scattered in different notebooks.

1. Pre-processing code and some initial experiments are in the notebook - NLPInitialNotebookPreprocessingT5SmallModel.ipynb 
2. NLPInitialNotebookPreprocessingT5SmallModel.ipynb - Contain pre-processing and t5-small training for explanation generation 
3. ClaimClassification.ipynb - Claim classification using DistillBert 
4. ExplanationGeneration.ipynb - Explanation Text generation
5. InferenceNotebook.ipynb - Contains an example of using the saved model to predict

# Saved model

Available on google drive.

