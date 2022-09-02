# Natural Language Processing API - FastAPI, spaCy, SKLearn
api that does sentiment analysis and analyzes text for tokens index, text, tag, POS, Dependency, Lemma, Shape, Alpha, and stop words


## model. 
```PYTHON3
class Input(BaseModel):
    sentence: str
```


## endpoints.  

POST.  
### /get_svm_sentiment **(EXPERIMENTAL)**.  
gets sentiment using a support vector machine, highly experimental.    
request will be:
```JSON
{
"sentence" : "I hate this book. It's not good."
}
```

POST. 
### /analyze_text  
gets input text and breaks it down by part of speech, lemma, shape, alpha, and stop word.  
request will be:
```JSON
{
"sentence" : "I am going to play basketball"
}
```


POST. 
### /entity_recognition  
gets input text and displays named entities. where they begin, end, what the entity is, and the label.   
request will be:   
```JSON
{
"sentence" : "Bill Gates is an awesome guy. Microsoft is a billion dollar company"
}
```


POST.  
### /sentiment_analysis
displays a positive or negative score based on polarity and displays all positive and negative words. handled by spaCy.   
request will be:   
```JSON
{
"sentence" : "I love this place. the food is so good and the service is awesome!"
}
```


## RUN. 
```
pip install -r requirements.txt
uvicorn main:app --reload
```
