# BERT WSD
an implementation of BERT to peform word sense disambiguation served through a Flask API.

Word Sense Disambiguation is the problem of determining which "sense" (meaning) of a word in the context of a sentence. This model is fine-tuned on the SemEval-2007 dataset and achieves 76.6% F1% score on the test dataset (`semcor.xml`). This is comparable to the current SOTA which achieves 81.2% F1% on the same dataset.

This repository builds upon this paper:
> Wiedemann, G., Remus, S., Chawla, A., Biemann, C. (2019): [Does BERT Make Any Sense? Interpretable Word Sense Disambiguation with Contextualized Embeddings. Proceedings of KONVENS 2019](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2019-wiedemannetal-bert-sense.pdf), Erlangen, Germany.

## how to use it

#### training the model
Run `chmod +x train.sh` to be able to run the script, then do `./train.sh` to begin training. It will take approximately 2 hours to retrain the embeddings.

#### serving the model
Run `python server.py` to start a Flask server on `localhost:5000`. Hit it with a POST on `/api` with a form response containing a `sentence` and target `word`. First spin-up will take ~10s and any subsequent requests will take around 500ms.

## examples

### 1
```bash
curl --location --request POST 'localhost:5000/api' \
--form 'sentence=How much work is done to lift a 3kg object 2 meters' \
--form 'word=work'
```

```json
{
    "def": "(physics) a manifestation of energy; the transfer of energy from one physical system to another expressed as the product of a force and the distance through which it moves a body in the direction of that force"
}
```

### 2

```bash
curl --location --request POST 'localhost:5000/api' \
--form 'sentence=I stand on the river bank' \
--form 'word=bank'
```

```json
{
    "def": "sloping land (especially the slope beside a body of water)"
}
```