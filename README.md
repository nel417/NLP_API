# Natural Language Processing API - FastAPI, spaCy, SKLearn  
api that does sentiment analysis and analyzes text for tokens index, text, tag, POS, Dependency, Lemma, Shape, Alpha, and stop words

![example workflow](https://github.com/nel417/NLP_API/actions/workflows/nlpapi.yml/badge.svg)

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

POST.  
### /generate_text
generates random text using a gpt2 model and the transformers library. Its fairly wonky but very fun to use. perhaps if you have gpt3 access or another heavy model you will get better results, but very fun to play with:   
```JSON
{
"sentence" : "My name is Nick and I like"
}
```

POST.  
### /translate_french  
endpoint that will translate english to french.
```JSON
{
"sentence" : "Where is the bathroom and nearest cafe?"
}
```

## RUN. 
```
pip install -r requirements.txt
uvicorn main:app --reload
```