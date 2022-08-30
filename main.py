from fastapi import FastAPI
import spacy
from pydantic import BaseModel
from spacytextblob.spacytextblob import SpacyTextBlob

en_core_web = spacy.load("en_core_web_lg")
en_core_web.add_pipe('spacytextblob')

app = FastAPI()


class Input(BaseModel):
    sentence: str


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


@app.post("/entity_recognition")
def get_entity(sentence_input: Input):
    document = en_core_web(sentence_input.sentence)

    output_array = []

    for token in document.ents:
        output = {
            "Text": token.text, "Start Char": token.start_char, "End Char": token.end_char, "Label": token.label_
        }
        output_array.append(output)
    return {"output": output_array}
