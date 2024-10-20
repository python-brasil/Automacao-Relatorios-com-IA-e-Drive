import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

openai_apikey = os.getenv("OPENAI_KEY")

def menager_response(system_prompt:str) -> str:
    print("Passando para a IA reformular uma resposta para a IA")
    
    client = OpenAI(api_key=openai_apikey)
   
    message = [
        {
            "role":"system",
            "content": system_prompt
        },
        {
            "role":"user",
            "content": "Me forneça um resumo breve do conteúdo entregue a você"
        }
        ]
    
    try:
        response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=message,
                max_tokens=300,
                temperature=0.3
            )
        
        resposta_ia = response.choices[0].message.content

        return resposta_ia
    except Exception as ex:
        print(ex)
    
    return ""