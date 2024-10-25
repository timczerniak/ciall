installreqs:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest -v

dockertestbase:
	docker image rm -f ciall_testbase
	docker build --target ciall_testbase -f Dockerfile -t ciall_testbase .

dockertest: dockertestbase
	docker run --rm -i ciall_testbase make test

dockershell: dockertestbase
	docker run --rm -it ciall_testbase bash