# Run the script
run:
	python forecast.py

# Clean up build files and other generated files
clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/

# Remove the virtual environment
venv:
	rm -rf venv/

# Generate a requirements file
requirements:
	pip freeze > requirements.txt

# Install project dependencies
install:
	sh install.sh
