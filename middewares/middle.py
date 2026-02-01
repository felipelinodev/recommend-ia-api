from middewares.fech_api import fetch_google_fonts
import os
import uuid



def generate_id_with_uuid() -> str:
    generate_id = uuid.uuid4()
    return generate_id

from dotenv import load_dotenv
load_dotenv()

API_KEY_GF:str = os.getenv("API_KEY_GF")
all_fonts = fetch_google_fonts(API_KEY_GF)["items"]

fonts_idx: dict = {font["family"]: font for font in all_fonts}

def verify_match_fonts(match_name: str) -> dict | bool: 
    font: dict = fonts_idx.get(match_name)
    if font:
        return { "category": font["category"], 
                 "menu": font.get("menu"),
                "files": font["files"],
                "font_variation": len(font["files"])} 
    return False

def verify_match_fonts_by_tag(tag: str) -> list[dict]: 
    matches = [font for font in all_fonts if font.get("category") == tag]
    return matches

def call_google_fonts(res_string: str) -> dict:
    split_res: dict = res_string["fonts"]

    full_dic: dict = {"fonts": []}

    for font in split_res:
        
        id: str = generate_id_with_uuid()

        name: str = font["name"]
        rank: str = font["rank"]

        curr_font_search: dict | bool = verify_match_fonts(name)

        if curr_font_search:
            merge_dick = {"name": name, "rank": rank, "font_id": id} | curr_font_search
            full_dic["fonts"].append(merge_dick)
        
    return full_dic



def call_google_fonts_by_name(name: str):
    id: str = generate_id_with_uuid()
    
    match_font: str = verify_match_fonts(name)    

    if (not match_font):
        return None

    match_font["font_id"] = id
    match_font["name"] = name

    return match_font


