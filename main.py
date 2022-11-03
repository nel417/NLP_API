from fastapi import FastAPI
import spacy
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from transformers import pipeline, set_seed, AutoTokenizer, AutoModelForSeq2SeqLM

import model
from spacytextblob.spacytextblob import SpacyTextBlob

en_core_web = spacy.load("en_core_web_sm")
en_core_web.add_pipe('spacytextblob')

app = FastAPI(tags=['sentence'])


class Input(BaseModel):
    sentence: str


# kind of fidgety, it's my first model. feel free to work off of it.
# data set has lots of positive, but not a lot of negative so i had to chop
# it in half to get equal amounts.
@app.post('/get_svm_sentiment')
def get_svm_sentiment(sentence_input: Input):
    Train, Test = train_test_split(model.reviews, test_size=0.33, random_state=42)
    container_train = model.ReviewContainer(Train)
    container_test = model.ReviewContainer(Test)
    container_train.even()
    x_train = container_train.get_text()
    y_train = container_train.get_labels()
    container_test.even()
    x_test = container_test.get_text()
    y_test = container_test.get_labels()
    vec = TfidfVectorizer()
    train_x_vec = vec.fit_transform(x_train)
    test_x_vec = vec.transform(x_test)
    y_train.count(model.Sentiment.NEGATIVE)
    classify = svm.SVC(kernel='linear')
    classify.fit(train_x_vec, y_train)
    classify_dec = DecisionTreeClassifier()
    from sklearn.metrics import f1_score
    classify_dec.fit(train_x_vec, y_train)
    new_test = vec.transform([sentence_input.sentence])
    output = classify.predict(new_test)
    return_score = f1_score(y_test,
                            classify.predict(test_x_vec),
                            average=None,
                            labels=[model.Sentiment.POSITIVE, model.Sentiment.NEUTRAL, model.Sentiment.NEGATIVE])

    return {tuple(output), tuple(return_score)}


@app.post("/analyze_text")
def get_text_characteristics(sentence_input: Input):
    document = en_core_web(sentence_input.sentence)
    output_array = []
    for token in document:
        output = {
            "Index": token.i, "Token": token.text, "Tag": token.tag_, "POS": token.pos_,
            "Dependency": token.dep_, "Lemma": token.lemma_, "Shape": token.shape_,
            "Alpha": token.is_alpha, "Is Stop Word": token.is_stop
        }
        output_array.append(output)
    return {"output": output_array}


@app.post("/entity_recognition")
def get_entity(sentence_input: Input):
    document = en_core_web(sentence_input.sentence)
    output_array = []
    for token in document.ents:
        output = {
            "Text": token.text, "Start Char": token.start_char,
            "End Char": token.end_char, "Label": token.label_
        }
        output_array.append(output)
    return {"output": output_array}


@app.post("/sentiment_analysis")
def get_text_sentiment(sentence_input: Input):
    document = en_core_web(sentence_input.sentence)

    url_sent_score = []
    url_sent_label = []
    total_pos = []
    total_neg = []
    sentiment = document._.blob.polarity
    sentiment = round(sentiment, 2)

    if sentiment > 0:
        sent_label = "Positive"
    else:
        sent_label = "Negative"

    url_sent_label.append(sent_label)
    url_sent_score.append(sentiment)
    positive_words = []
    negative_words = []

    for x in document._.blob.sentiment_assessments.assessments:
        if x[1] > 0:
            positive_words.append(x[0][0])
        elif x[1] < 0:
            negative_words.append(x[0][0])
        else:
            pass

    total_pos.append(', '.join(set(positive_words)))
    total_neg.append(', '.join(set(negative_words)))

    output = {"Score": url_sent_score, "Label": url_sent_label,
              "Positive words": total_pos, "Negative Words": total_neg}

    return {"output": output}


@app.post("/generate_text")
def generate_text(sentence_input: Input):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    input_string = sentence_input.sentence
    output = generator(input_string, max_length=512)
    return output


@app.post("/translate_french")
def translate(sentence_input: Input):
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    input = sentence_input.sentence
    input_ids = tokenizer.encode(input, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=512)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded
