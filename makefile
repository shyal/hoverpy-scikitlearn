all:
		echo "done"

.PHONY:

docs: .PHONY
		cd docs; make clean; make html;

clean:
		rm -f *.pyc *.log

run:
		python hoverpy_scikitlearn.py

commit_and_push:
		git add .
		git commit -am "added"
		git push