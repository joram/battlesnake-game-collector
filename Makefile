build:
	docker build . -t joram87/battlesnake-game-collector

run_docker:
	docker rm -f battlesnake-game-collector
	docker run -d --name battlesnake-game-collector -v /home/john/code/joram/battlesnake-game-collector/data:/src/data joram87/battlesnake-game-collector
