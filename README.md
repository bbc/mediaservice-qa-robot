# mediaservice-qa-robot
A question-answering robot for media service components.
The idea is to use a component's runbook, README and component tests to create question-answer pair data. Use Natural Language Processing(NLP) model to encode the questions and use similarity search engine to create index for questions. When people input the question, the question will be encoded by the same NLP model and use search engine to get most similar questions in the index, then fetch the answers by the questions.
The embedding model uses [SentenceTransformers](https://www.sbert.net/). The search engine uses [faiss](https://github.com/facebookresearch/faiss). The service framework uses [Flask](https://flask.palletsprojects.com/en/2.0.x/).

## requirement
```
pip install -r requirements.txt
```

## run demo
```
flask run
```
Then open browser http://127.0.0.1:5000/ 

## tools
There are some tools under /tools to extract question-answer pair from runbook, README and component tests and append the result to a csv file. 
After you get all the data in the csv file, delete data/demo.csv and demo.index, run ```python tools/add-index.py --csv_in your_csv.csv  --csv_out data/demo.csv``` to add id for the data.
