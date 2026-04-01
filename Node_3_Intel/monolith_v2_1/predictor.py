import requests

def llm_predict(context):
    response=requests.post('http://localhost:11434/api/generate',json={'model':'llama3','prompt':f'State:{context}'})
    return response.json().get('response','')
