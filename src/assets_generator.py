'''
Author: William Zhizhuo Yin
Data: 07/04/2023
'''

import os

def shape_models_generator(opt, filepath, description):
    print("Generating " + str(filepath))
    # 3D model generation
    local_path = "./tmp_file/"+str(filepath)
    object_name = filepath.split("/")[-1].split('.')[0]

    # 切换到 UTF-8 编码
    os.system("chcp 65001")

    # # 确保路径拼接正确
    workspace_dir = os.path.join(opt.shape_dir, "space")
    cmd0 = f'cd /d "{workspace_dir}"'
    print(cmd0)
    os.system(cmd0)

    cmd = opt.python_dir + f" {workspace_dir}\\generate_model.py --prompt \"" + str(description) + \
          "\""
    # cmd = opt.python_dir + f" {workspace_dir}\\Test2.py --prompt \"" + str(description) + \
    #       "\""
    print(cmd)
    os.system(cmd)

    # # 激活环境并执行命令
    # python_exe = r"D:\PROGRAMME\Anaconda\envs\shap-e\python.exe"
    # script_path = os.path.join(workspace_dir, "generate_model.py")
    # # 构建执行命令
    # generate_cmd = f'"{python_exe}" "{script_path}" --prompt "{description}"'
    #
    # # 执行命令
    # print(f"执行命令: {generate_cmd}")
    # os.system(generate_cmd)

    # 调用 Blender 脚本
    cmd2 = f'{opt.blender_dir} -b -P 2gltf2.py -- mesh.ply'
    print(cmd2)
    os.system(cmd2)

    # 复制生成的文件
    model_path = os.path.join("./mesh.gltf")
    cmd3 = f'copy "{model_path}" "{local_path}"'
    print(cmd3)
    os.system(cmd3)

    # 删除mesh.ply继续生成
    if os.path.exists("mesh.ply"):
        os.remove("mesh.ply")  # 删除文件
        print("File mesh.ply has been deleted.")
    else:
        print(f"File does not exist.")
    if os.path.exists("mesh.gltf"):
        os.remove("mesh.gltf")  # 删除文件
        print("File mesh.gltf has been deleted.")
    else:
        print(f"File does not exist.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        nargs="?",
        default="generate the scene of Mountains with towering peaks covered in dense forests of deep green.",
        help="the prompt to render"
    )
    parser.add_argument(
        "--openai_key",
        type=str,
        nargs="?",
        default="sk-5FRioxbHWVzdnEhlA4Bb41De975e490f9a8dB47c36262886",
        help="openai api key"
    )
    parser.add_argument(
        "--skybox_key",
        type=str,
        nargs="?",
        default="1QIF7ouzzbkRGcnXe1XAtABVy6b5c28brOLsOgY3UgUJV4hmYJy0rSkJn9ZR",
        help="skybox api key"
    )
    parser.add_argument(
        "--shape_dir",
        type=str,
        nargs="?",
        default="D:/DeskTop/EndWork/shap-e/",
        help="path of shap-e folder in remote machine"
    )
    parser.add_argument(
        "--python_dir",
        type=str,
        nargs="?",
        default="D:\PROGRAMME\Anaconda\envs\shap-e\python.exe",
        help="path of configured python environment in remote machine"
    )
    parser.add_argument(
        "--blender_dir",
        type=str,
        nargs="?",
        default="D:/TOOLS/blender-3.5.1-windows-x64/blender.exe",
        help="path of blender in remote machine"
    )
    opt = parser.parse_args()

    prompt = "Mountains with towering peaks covered in dense forests of deep green."
    # 还需要一个飞鸟和大的陆地
    filepath = "resource/models/Mountain2.gltf"
    shape_models_generator(opt, filepath, prompt)