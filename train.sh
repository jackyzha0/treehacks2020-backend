python3 BERT_Model.py \
--train_corpus=data/senseval2_lexical_sample_train.xml \
--trained_pickle=BERT_embs.pickle \
--test_corpus=data/senseval2_lexical_sample_test.xml \
--start_k=1 --end_k=10 --save_xml_to=SE2.xml \
--use_euclidean=0 --reduced_search=0