
.PHONY: build
build:
	docker-compose build

.PHONY: stop
stop:
	docker-compose down

.PHONY: run
run:
	docker-compose up -d

.PHONY: test
test:
	docker-compose -f tests/docker_env/docker-compose.test.yml up --build --exit-code-from backend-test --abort-on-container-exit backend-test
	docker-compose -f tests/docker_env/docker-compose.test.yml down -v
