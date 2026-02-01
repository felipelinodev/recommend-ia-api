from flask import Blueprint, request, make_response, jsonify, abort
import json

import core.prompts as s

from middewares.middle import call_google_fonts
from core.model_connection import send_prompt
from middewares.middle import verify_match_fonts_by_tag
from middewares.middle import call_google_fonts_by_name

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: str = os.getenv("TOKEN_RECOMMEND_API")

#system prompts
SYSTEM_PROMPT_TEXTUAL: str = s.TEXTUAL
SYSTEM_PROMPT_STRUCTURED: str = s.STRUCTURED

give_ia_response =  Blueprint("give_ia_response", __name__)

def _process_request_string(prompt: str, system_prompt: str) -> dict | Exception:
    try:
        res_string = send_prompt(prompt, system_prompt)

        if res_string != "invalid entry":
            res_string = json.loads(res_string)

        res_string = call_google_fonts(res_string)
        return res_string
    except Exception as e:
        print(f"Deu erro em(_process_request_string): {e}")


@give_ia_response.route("/structured", methods=['POST'])
def give_response():
    try:
        token = request.headers.get('Authorization')
        if token != f'Bearer {TOKEN}':
             raise Exception('Taken inválido.')

        prompt = request.json
    
        res = _process_request_string(prompt, SYSTEM_PROMPT_STRUCTURED)

        return make_response(
            jsonify(
                type="structured prompt",
                response=res
            ), 200)
    except Exception as e:
        return {"error": f"erro desconhecido: {e}"}, 500 
        

@give_ia_response.route("/textual", methods=['POST'])   
def give_response_textual():
    try:
        token = request.headers.get('Authorization')
        if token != f'Bearer {TOKEN}':
            raise Exception('Taken inválido.')

        prompt = request.json

        res = _process_request_string(prompt, SYSTEM_PROMPT_TEXTUAL)

        return make_response(
            jsonify(
                type="structured prompt",
                response=res
            ), 200)
    except Exception as e:
        return {"error": f"erro desconhecido: {e}"}, 500 
        
   
@give_ia_response.route('/categorized', methods=['GET'])
def give_response_categorized():
    try:
        token = request.headers.get('Authorization')
        if token != f'Bearer {TOKEN}':
            raise Exception('Token Inválido.')

        font_category = request.args.get('category')

        if not font_category:
             return {"error": "font missing"}, 400
        
        return jsonify(verify_match_fonts_by_tag(font_category))
    except Exception as e:
        return {"error": f"erro desconhecido: {e}"}, 500   


@give_ia_response.route('/named', methods=['GET'])
def give_ia_response_font_name():
    try:
        token = request.headers.get('Authorization')
        if token != f'Bearer {TOKEN}':
            raise Exception('Token Inválido.')

        font_name = request.args.get('font')
        font_matched = call_google_fonts_by_name(font_name)

        if not font_matched:
             return {"error": "font missing"}, 400
        
        return jsonify(font_matched)

    except Exception as e:
       return {"error": f"erro desconhecido: {e}"}, 500       
