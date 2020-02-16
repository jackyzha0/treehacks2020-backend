FROM tensorflow/tensorflow:2.1.0-py3

# Copy requirements file
COPY requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# Copy files
COPY server.py server.py
COPY BERT_pred.py BERT_pred.py
COPY WordNet_Lookup.py WordNet_Lookup.py
COPY BERT_semcor.pickle BERT_semcor.pickle
COPY NounChunk.py NounChunk.py

RUN python3 -m nltk.downloader wordnet
RUN python3 -m spacy download en_core_web_md
RUN python3 -m nltk.downloader stopwords

# Expose port and run server
EXPOSE 5000
CMD ["python3", "-u", "server.py"]