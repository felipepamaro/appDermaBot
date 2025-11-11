.PHONY: install run test

ex:
	export $(cat env.dev | xargs)
run:
	flask --app appDermaBotArvore run --host=0.0.0.0 --port 8000 --reload
