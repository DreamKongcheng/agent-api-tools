# 1. 构建和运行 Docker 容器
## 1. 构建 Docker 镜像：
```bash
docker build -t google_search .
```

## 2. 运行 Docker 容器：
```bash
docker run -d -p 8000:8000 google_search
```

## 3. 访问应用
在Postman中访问`http://localhost:8000/search`，并发送一个POST请求，请求体为：
```json
{
    "query": "杭州今天天气"
}
```
可以看到返回的搜索结果。
