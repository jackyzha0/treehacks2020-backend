# readAR - backend
[DevPost](https://devpost.com/software/readar-twh41m)

This repository contains the implementation of readAR's backend. You can find an implementation of BERT to peform word sense disambiguation served through a Flask API, as well as our image processing pipeline (`/API-azure-pipeline`). 

Word Sense Disambiguation is the problem of determining which "sense" (meaning) of a word in the context of a sentence. This model is fine-tuned on the SemEval-2007 dataset and achieves 76.6% F1% score on the test dataset (`semcor.xml`). This is comparable to the current SOTA which achieves 81.2% F1% on the same dataset. The work here builds upon this paper,

> Wiedemann, G., Remus, S., Chawla, A., Biemann, C. (2019): [Does BERT Make Any Sense? Interpretable Word Sense Disambiguation with Contextualized Embeddings. Proceedings of KONVENS 2019](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2019-wiedemannetal-bert-sense.pdf), Erlangen, Germany.

### Running the example
The entire working model can be found as a Docker image. You can download it and run it as follows:

1. `docker pull jzhao2k19/bert-wsd:latest`
2. `docker run -p 5000:5000 jzhao2k19/bert-wsd:latest`

## How to train a new model
Run `chmod +x train.sh` to be able to run the script, then do `./train.sh` to begin training. It will take approximately 2 hours to retrain the embeddings. This will generate a new set of weights in a file called `BERT_semcor.pickle`. 

#### Serving the model (without Docker)
Run `python server.py` to start a Flask server on `localhost:5000`. Hit it with a POST on `/api/wsd` with a form response containing a `sentence` and target `word`. First spin-up will take ~10s and any subsequent requests will take around 500ms. Keep in mind that running this will have required you to have trained a model before hand. If you would like to run one without training, look at `Running the example` for how to do it through docker.

## Service URLs
(may not work after the hackathon)
* WSD-model: `140.238.147.73:5000/api/wsd`
* img-pipeline: `140.238.147.73:8080/api`
* quiz-generation: `140.238.147.73:8081/api?q=some+query`

## Examples
### 1 -- physics definition of work
```bash
curl --location --request POST '140.238.147.73:5000/api/wsd' \
--form 'sentence=How much work is done to lift a 3kg object 2 meters' \
--form 'word=work'
```

```json
{
    "def": "(physics) a manifestation of energy; the transfer of energy from one physical system to another expressed as the product of a force and the distance through which it moves a body in the direction of that force"
}
```

### 1 -- an occupational definition of work
```bash
curl --location --request POST '140.238.147.73:5000/api/wsd' \
--form 'sentence=What do you do for work?' \
--form 'word=work'
```

```json
{
    "def": "the occupation for which you are paid"
}
```

### 2 -- a river bank

```bash
curl --location --request POST '140.238.147.73:5000/api/wsd' \
--form 'sentence=I stand on the river bank' \
--form 'word=bank'
```

```json
{
    "def": "sloping land (especially the slope beside a body of water)"
}
```

### 2 -- a financial institution

```bash
curl --location --request POST '140.238.147.73:5000/api/wsd' \
--form 'sentence=I need to deposit money at the bank tomorrow' \
--form 'word=bank'
```

```json
{
    "def": "a financial institution that accepts deposits and channels the money into lending activities"
}
```