FROM tensorflow/tensorflow:2.1.0-py3

# Copy requirements file
COPY requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_md

# Copy files
COPY api.py api.py

# Expose port and run server
EXPOSE 8080
CMD ["python3", "-u", "api.py"]