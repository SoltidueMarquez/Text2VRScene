from ChatGPT_coder import ChatGPT_coder
from experience_generator import experience_generator
import argparse

def Text2VR(opt, hist_messages, is_test):

    # Input text as ChatGPT prompt, return the filtered aframe html code

    hist_messages, code, literature = ChatGPT_coder(hist_messages, opt, is_test)

    if code != None:
        # generate VR experience
        experience_generator(code, literature, is_test)

    return hist_messages, code

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        nargs="?",
        default="generate the scene of a spaceship traveling in space (no one appears in the scene)",
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
        default="sk-5FRioxbHWVzdnEhlA4Bb41De975e490f9a8dB47c36262886",
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
        default="D:/PROGRAMME/Anaconda/envs/text2vr", # 这边不对，要在conda里配置shape-e
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

    hist_messages = []
    is_test = False
    Text2VR(opt, hist_messages, is_test)



