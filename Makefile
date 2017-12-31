# simple makefile for kontracto

.PHONY : ve 
ve: 
	python3 -m venv --clear VE
	@echo "run . ./VE/bin/activate  to activate virtual environment"

.PHONY : install 
install :
	python3 setup.py install 

.PHONY : clean
clean : 
	rm -r build dist kontrakto.egg-info

# end of file
