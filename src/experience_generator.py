import os
import webbrowser

# Credit to Max Shvedov at https://stackoverflow.com/questions/51189628/simple-http-server-in-python-how-to-get-files-from-dir-path
# Forgot where else I picked up code

import http.server
import socketserver
from os import path

my_host_name = 'localhost'
my_port = 8888
html_folder = 'tmp_file/myheartwillgoon'
webfile = ""

# 自定义 HTTP 请求处理器，用于处理 GET 请求
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self):  # 发送 HTTP 响应头部，表示请求成功
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', path.getsize(self.getPath()))
        self.end_headers()

    def getPath(self):  # 根据客户端请求路径 self.path，确定要加载的文件路径：
        if self.path == '/':
            content_path = path.join(
                html_folder, webfile)
        else:
            content_path = path.join(html_folder, str(self.path).split('?')[0][1:])
        return content_path

    def getContent(self, content_path): # 从指定路径读取文件内容，以二进制模式加载，返回内容。
        with open(content_path, mode='rb') as f:
            content = f.read()
        return content

    def do_GET(self):   # 处理 HTTP GET 请求
        self._set_headers()
        self.wfile.write(self.getContent(self.getPath()))

# 生成体验页面函数，用于动态生成 HTML 文件并启动服务器
def experience_generator(code, literature, is_test):

    # 去除错误
    code = code.replace("\\n", "").replace("\\", "")

    # 创建文件夹和 HTML 文件
    if not os.path.exists("tmp_file/"+str(literature)):
        os.makedirs("tmp_file/"+str(literature))

    if os.path.exists("tmp_file/"+str(literature)+"/experience.html"):
        os.remove("tmp_file/"+str(literature)+"/experience.html")
    cur_html = "tmp_file/"+str(literature)+"/experience.html"

    # 打开 cur_html 文件并写入 code（HTML 字符串）
    file = open(cur_html, 'w')
    file.write(code)
    file.close()

    # 更新全局变量 html_folder 和 webfile，指定 HTML 文件所在的目录和文件名
    global html_folder
    global webfile
    html_folder = "tmp_file/" + str(literature) + "/"
    if not is_test:
        webfile = "experience.html"
    else:
        webfile = "experience.html"

    # 启动 HTTP 服务器
    my_handler = MyHttpRequestHandler
    #if is_test == False:
    with socketserver.TCPServer(("", my_port), my_handler) as httpd:
        print("Http Server Serving at port", my_port)
        webbrowser.open("http://localhost:8888")
        httpd.serve_forever()

if __name__ == "__main__":
    webfile = "experience.html"
    html_folder = 'samples/myheartwillgoon'
    my_handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", my_port), my_handler) as httpd:
        print("Http Server Serving at port", my_port)
        webbrowser.open("http://localhost:8888")
        httpd.serve_forever()


