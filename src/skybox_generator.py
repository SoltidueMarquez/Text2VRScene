import argparse
import http.client
import json
import requests
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def skybox_generator(apikey, prompt, literature):
    """
    使用 OpenAI 的 API 生成天空盒图片并保存到指定路径。

    参数：
        apikey (str): API 密钥。
        prompt (str): 生成图片的提示文本。
        literature (str): 保存图片的文件名。
    """
    try:
        # 设置API连接
        conn = http.client.HTTPSConnection("api.gpt.ge")

        # 构建请求的载荷
        payload = json.dumps({
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1792x1024"
        })

        # 设置请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apikey}'
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
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            with session.get(image_url, stream=True, timeout=10) as response:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading")

                save_path = f"D://DeskTop//EndWork//Text2VRScene//src//tmp_file//resource//images//{literature}.png"

                with open(save_path, "wb") as f:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        f.write(data)
                progress_bar.close()

            print(f"图片已保存到 {literature}")
        else:
            print("未生成图片或响应中没有图片数据")

    except requests.exceptions.RequestException as e:
        print(f"下载图片时发生错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apikey",
        type=str,
        nargs="?",
        default="sk-5FRioxbHWVzdnEhlA4Bb41De975e490f9a8dB47c36262886",
        help="API key for skybox generation"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        nargs="?",
        default="a professional photograph of an astronaut riding a triceratops",
        help="The prompt to render"
    )
    opt = parser.parse_args()
    opt.prompt = "In the middle of desert with shiny sun"
    skybox_generator(opt.apikey, opt.prompt, "madmax")
