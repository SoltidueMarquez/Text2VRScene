import http.client
import json
import requests  # 用于下载图片
from tqdm import tqdm  # 进度条库

# 设置API连接
conn = http.client.HTTPSConnection("api.gpt.ge")

# 构建请求的载荷
payload = json.dumps({
   "model": "dall-e-3",
   "prompt": "一张天空盒，是广阔无垠的宇宙，有星星点点的银河,务必确保图片是可以左右相连的",
   "n": 1,
   "size": "1792x1024"
})

# 设置请求头
headers = {
   'Content-Type': 'application/json',
   'Authorization': 'Bearer sk-5FRioxbHWVzdnEhlA4Bb41De975e490f9a8dB47c36262886'  # 替换为你的API密钥
}

# 发出请求
conn.request("POST", "/v1/images/generations", payload, headers)

# 获取响应
res = conn.getresponse()
data = res.read()

# 解析响应
response_json = json.loads(data.decode("utf-8"))

# 检查响应是否包含图片数据
if 'data' in response_json and len(response_json['data']) > 0:
   # 获取图片的 URL
   image_url = response_json['data'][0]['url']
   print(f"图片URL: {image_url}")

   # 下载图片并保存
   save_path = "D://DeskTop//EndWork//Text2VRScene//src//tmp_file//resource//images//generated_image.png"  # 替换为你想保存的路径

   # 使用 requests 获取图片流
   with requests.get(image_url, stream=True) as response:
      total_size = int(response.headers.get('content-length', 0))  # 获取内容总大小
      block_size = 1024  # 每次读取的块大小
      progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading")  # 设置进度条

      with open(save_path, "wb") as f:
         for data in response.iter_content(block_size):
            progress_bar.update(len(data))  # 更新进度条
            f.write(data)
      progress_bar.close()

   print(f"图片已保存到 {save_path}")
else:
   print("未生成图片或响应中没有图片数据")
