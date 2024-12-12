all: export-requirements up

build:
		docker-compose build
up:
		docker-compose build && docker-compose up
run:
		docker-compose build && docker-compose up
export-requirements:
		poetry export --format requirements.txt --output requirements.txt --without-hashes
