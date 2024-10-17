TAIL = 100

build:
	docker compose -f docker-compose.yaml build
up:
	docker compose -f docker-compose.yaml up -d
down:
	docker compose -f docker-compose.yaml down
logs:
	docker logs -f --tail=${TAIL} mongodb_for_scripts 2>&1
pre-commit:
	pip install pre-commit && pre-commit run --all-files
