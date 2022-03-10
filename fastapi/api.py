from fastapi import FastAPI
import string
import re
import os
import joblib
from transformers import DistilBertTokenizer, TFDistilBertModel
from pydantic import BaseModel

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

class Query(BaseModel):
    text: str

app = FastAPI()

# Set models path
path_to_model = 'models/BERT_MLP_model.joblib'

# load mlp model, bert tokenizer and bert model
mlp_model = joblib.load(open(path_to_model, 'rb'))
bert_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert_model = TFDistilBertModel.from_pretrained("distilbert-base-uncased")

def processor(sentence):
    """
    input: string
    Takes in a sentence & cleans the sentence
    output: string """   
    # Remove white spaces
    sentence = re.sub(' +', ' ',sentence).strip()
        
    return sentence

def bert_vectorizer(text):
    """
    input: array
    Takes in an array with sentences 
    and outputs a vectorized array
    output: array """
    
    encoded_input = bert_tokenizer(text, return_tensors='tf')
    output = bert_model(encoded_input)[0]
    output = output.numpy()[0][0]

    return [output]


def sklearn_classification_model(text, clean_text, 
                                vectorized_text, model):
    """
    input: user input, cleaned user input, vectorized array & ml model object
    The vectorized array is passed into the model object for prediction.
    The user inputs and prediction information are passed into a dictionary.
    output: dictionary """

    # Predict sentiment
    prediction = model.predict(vectorized_text)[0]
    # Get class probabilities
    prediction_proba = model.predict_proba(vectorized_text)[0]
    # Get all classes
    prediction_classes = model.classes_
    # Create class ranking
    class_ranking = {}
    # Get confidence per class
    for classes, conf in zip(prediction_classes, prediction_proba):
        class_ranking[classes] = conf
    
    # Sort class ranking
    class_ranking = dict(sorted(class_ranking.items(), key=lambda x: x[1], reverse=True))

    # Dictionary with empty values
    result = {"user input": "", "processed input": "", 
              "predicted sentiment": "", "confidence": "", 
              "class ranking": ""}

    # Fill dictionary
    result["user input"] = text
    result["processed input"] = clean_text
    result["predicted sentiment"] = prediction
    result["confidence"] = class_ranking[prediction]
    result["class ranking"] = class_ranking

    return result

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
def predict_sentiment(text: Query):
    # Text cleaner
    clean_text = processor(text.text)    
    # Feature_extraction
    vectorized_text = bert_vectorizer(clean_text)
    # Classification model
    result = sklearn_classification_model(text, clean_text, 
                                          vectorized_text, mlp_model)
    # Render result
    return result
