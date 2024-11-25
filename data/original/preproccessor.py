import os
import json

def transform_laws_ch_to_articles(input_file, output_file):
    # 讀取原始 JSON 文件
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
        return
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    
    # 初始化結果列表
    articles = []

    # 遍歷 Laws，提取條文
    for law in data.get("Laws", []):
        law_level = law.get("LawLevel", "")
        law_name = law.get("LawName", "")
        law_category = law.get("LawCategory", "")
        
        for article in law.get("LawArticles", []):
            articles.append({
                "LawLevel": law_level,
                "LawName": law_name,
                "LawCategory": law_category,
                "ArticleType": article.get("ArticleType", ""),
                "ArticleNo": article.get("ArticleNo", ""),
                "ArticleContent": article.get("ArticleContent", "")
            })

    # # 將結果寫入新的 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

def transform_laws_en_to_articles(input_file, output_file):
    # 讀取原始 JSON 文件
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(type(data))
            print(len(data.get("Laws")))
    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
        return
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    
    # 初始化結果列表
    articles = []

    # 遍歷 Laws，提取條文
    for law in data.get("Laws", []):
        law_level = law.get("LawLevel", "")
        law_name = law.get("EngLawName", "")
        for article in law.get("EngLawArticles", []):
            articles.append({
                "LawLevel": law_level,
                "EngLawName": law_name,
                "EngArticleType": article.get("EngArticleType", ""),
                "EngArticleNo": article.get("EngArticleNo", ""),
                "EngArticleContent": article.get("EngArticleContent", "")
            })

    # # 將結果寫入新的 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    input_file = "data/original/laws_en.json"
    output_file = "data/laws_en.json"
    transform_laws_en_to_articles(input_file, output_file)