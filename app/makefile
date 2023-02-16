up:
	docker build --tag nlp_app .
	docker run -d -p 8080:8080 --name nlp_app nlp_app

down:
	docker stop nlp_app
	docker rm nlp_app