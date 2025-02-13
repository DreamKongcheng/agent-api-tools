from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import List

from bs4 import BeautifulSoup

# 创建 FastAPI 实例
app = FastAPI()

# 定义搜索请求的数据模型
class SearchRequest(BaseModel):
    query: str

# Google Custom Search API 密钥和搜索引擎 ID
API_KEY = "AIzaSyBh3_au-TtJ7N-QM7XW7TSIt-K2BSGbJh8"
CX = "d168e359efbc54711"

# 用于从网页中提取主要内容的函数
def extract_page_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding  # 自动检测并设置编码
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取网页中的所有文本内容，可以根据需要调整提取策略
            # 这里简单获取正文区域的文本
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])  # 你可以根据需要调整
            content = '\n'.join([para.get_text() for para in paragraphs if para.get_text()])
            return content
        else:
            return None
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return None

# 搜索的函数
def search_with_google_api(query: str):
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}'
    
    # 发送请求到 Google Custom Search API
    response = requests.get(url)
    
    if response.status_code == 200:
        # 解析返回的 JSON 数据
        results = response.json()
        
        # 提取搜索结果并返回
        search_results = []
        for item in results.get('items', []):
            page_content = extract_page_content(item['link'])  # 获取文章内容
            search_results.append({
                'title': item['title'],
                'link': item['link'],
                'content': page_content  # 将文章内容添加到结果中
            })
        
        return search_results
    else:
        # 返回错误信息
        raise HTTPException(status_code=response.status_code, detail="Error fetching results from Google API")

# # 转换成大模型友好的格式
# def format_for_large_model(results):
#     formatted_results = []
    
#     for result in results:
#         formatted_result = {
#             "source": result['link'],
#             "title": result['title'],
#             "content": result['content'],
#             "summary": result['content'][:300]  # 简要摘要，可以根据需要调整长度
#         }
#         formatted_results.append(formatted_result)
    
#     return formatted_results

# 创建搜索接口
@app.post("/search/", response_model=List[dict])
async def search(search_request: SearchRequest):
    query = search_request.query
    raw_results = search_with_google_api(query)
    # formatted_results = format_for_large_model(raw_results) 
    return raw_results



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)