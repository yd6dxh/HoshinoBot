import requests
import csv
import time
import urllib.parse

# API URL和必要的参数
url = "https://api.game.bilibili.com/game/player/tools/pcr/clan_battle_ranking"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Cookie": (
            "DedeUserID=167454779; "
            "DedeUserID__ckMd5=f28b4eff9b9f420d; "
            "SESSDATA=a182e43b%2C1761046171%2Cd8d61%2A42CjCbDD7wx_utkJaNq2B0o5dk4_rNI2vJ20qWKL6A-DWDLltySTMybUwGDByJEBEienoSVjN5ZGtVeDBqUVdJRGJ3NGNBNFhPVmZkOVM1UmRfendYR25vcjRmUDNZcGQ1UGw4RDZkX1JWT2NYWGpkXzB3VUI5SE5pck82eGFCZUNueS1ETGE2X1lBIIEC; "
            "bili_jct=627a1741d506809cea737b88992bdca8; "
            "bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDU4NTI4MjAsImlhdCI6MTc0NTU5MzU2MCwicGx0IjotMX0.AKi96vP00lhCvZBgOud93NAZ-rOU8hAVvfsUW8SuQf4;"
        )}

# 获取API数据
def fetch_clan_ranking(page=1):
    params = {
        "page": page,  # 分页
        "size": 20,    # 每页显示的公会数量
        "appkey": "你的appkey",  # 根据实际情况传入
        "sign": "你的签名",  # 根据实际情况传入
        "ts": int(time.time()),  # 当前时间戳
        "nonce": "随机数"  # 随机数，通常为某个不重复的值
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 如果返回状态码不是200，抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        print(f"响应内容: {response.text}")
        return {}

# 提取数据并保存为CSV
def save_to_csv():
    all_data = []
    for page in range(1, 21):  # 获取前20页数据
        data = fetch_clan_ranking(page)
        if data.get("code") != 200:
            print(f"Error fetching page {page}: {data.get('message')}")
            continue

        for rank in data["data"]["list"]:
            guild_name = rank.get("name")
            score = rank.get("score")
            rank_position = rank.get("rank")
            all_data.append([rank_position, guild_name, score])

    # 保存到CSV
    with open('clan_ranking.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["排名", "公会名", "分数"])  # 表头
        writer.writerows(all_data)

    print("CSV文件已保存：clan_ranking.csv")

# 执行函数
save_to_csv()
