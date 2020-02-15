python3 BERT_Model.py \
--train_corpus=data/semcor.xml \
--train_type=SEM \
--trained_pickle=BERT_semcor.pickle \
--test_corpus=data/semeval2007task7.xml \
--start_k=1 --end_k=1 --save_xml_to=SE2.xml \
--use_euclidean=0 --reduced_search=0