import getopt
import sys
import os
import time
import pandas as pd
from openai import OpenAI
from tqdm import tqdm

client = None

def translate_text(model_name,text):  # 用来调用API翻译传入的文本
    try:
        response = client.chat.completions.create(
            model=model_name,
            #Promt based from widely-used project BabelDoc https://github.com/funstory-ai/BabelDOC/
            messages=[
                {"role": "system", "content": "You are a professional,authentic machine translation engine."},
                {"role": "user", "content": f";; Treat next line and the following lines as plain text input and translate it into Chinese (Simplified) in a single line, output translation ONLY. If translation is unnecessary (e.g. proper nouns, codes, {'{{1}}, etc. '}), return the original text. NO explanations. NO notes. Input:\n\n{text}",}
            ],
            temperature=0.1,
            max_tokens=16384,
        )
        return str(response.choices[0].message.content).replace(",","，").replace("\n"," ")
    except Exception as e:
        print(f"Error: {e}")
        return None

def usage():
    print("Usage: python translator.py [OPTION] <INPUT_FILE>")
    print("")
    print("  -h, --help: show this help message and exit")
    print("  -o, --output: set the output file, default is result.csv")
    print("  -t, --token: set the token,default is HF_TOKEN in environment variable")
    print("  -u, --url: set the base url to OpenAI API, default is HuggingFace's https://router.huggingface.co/v1")
    print("  -m, --model: set the model,default is openai/gpt-oss-120b:fastest")
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:t:u:m:", ["help","output=","token=","url=","model="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = "result.csv"
    if len(args)==0:
        usage()
        sys.exit(1)
    inp = args[0]
    hf_token = os.environ.get("HF_TOKEN")
    url = 'https://router.huggingface.co/v1'
    model_name = "openai/gpt-oss-120b:fastest"
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-t", "--token"):
            hf_token = a
        elif o in ("-u", "--url"):
            url = a
        elif o in ("-m", "--model"):
            model_name = a
        else:
            assert False, "未处理的选项"
    if hf_token is None:
        raise Exception("HF_TOKEN is not set")
    global client
    client = OpenAI(
        base_url=url,
        api_key=hf_token
    )
    # 读取数据
    df = pd.read_csv(inp)
    rows = []
    for index, row in df.iterrows():
        rows.append(row)
    tqdm.write(f'There are {len(rows)} rows in total.')
    # 遍历每一行，翻译摘要
    with open(output, "w", encoding="utf-8") as f:
        for index, row in enumerate(tqdm(rows, position=0, file=sys.stdout, desc="Translation Process:")):
            abstract = row['abstract']
            tqdm.write(f"Translating paper #{index+1}...")
            cn_abstract = translate_text(model_name,abstract)
            if cn_abstract is None:
                pass #TODO:异常处理，明天再写
            # 将结果写入新文件
            f.write(f"{index+1},{cn_abstract}\n")
            time.sleep(1)  # 避免请求过于频繁
    tqdm.write('Translation completed.')

if __name__ == "__main__":
    main()
