# App For Fact Check NLP

How to run:

1. Install docker
2. Navigate to FactCheckNLP/app
3. run `docker build --tag nlp_app .`
4. run `docker run -d -p 8080:8080 nlp_app`
5. The app should be deployed at http://localhost:8080