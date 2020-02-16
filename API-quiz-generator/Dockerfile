FROM tensorflow/tensorflow:2.1.0-py3

# Copy requirements file
COPY requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# load library
RUN python3 -m spacy download en_core_web_md

# Copy files
COPY quiz.py quiz.py

# Expose port and run server
EXPOSE 8081
CMD ["python3", "-u", "quiz.py"]