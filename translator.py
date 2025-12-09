import getopt
import sys
import os
import time
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
import traceback

client = None

@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
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
        return str(response.choices[0].message.content).replace("\n"," ")
    except Exception as e:
        print('Exception occurred. Retrying in 10s...', file=sys.stderr)
        print('Details:', file=sys.stderr)
        traceback.print_exc()
        raise e

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
        print(err,file=sys.stderr)
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
    tqdm.write('Loading data...')
    # 读取数据
    df = pd.read_csv(inp)
    rows = len(df)
    tqdm.write(f'There are {rows} rows in total.')
    titles_out = []
    if os.path.exists(output):
        df_out = pd.read_csv(output)
        for index, row in df_out.iterrows():
            titles_out.append(row['title'])
    else:
        with open(output, "w", encoding="utf-8") as f:
            f.write('title,authors,abstract,date,paper_url,score,title_cn,abstract_cn\n')
    # 遍历每一行，翻译摘要
    with open(output, "a", encoding="utf-8") as f:
        try:
            for index, row in tqdm(df.iterrows(),total=rows, position=0, file=sys.stdout, desc="Translation Process"):
                title = row['title']
                if title in titles_out:
                    tqdm.write(f'Skipping existing paper #{index+1} (Title:\"{title}\")')
                    continue
                abstract = row['abstract']
                tqdm.write(f"Translating paper #{index+1}...")
                cn_title = translate_text(model_name, title)
                cn_abstract = translate_text(model_name,abstract)
                # 将结果写入新文件
                f.write(f"\"{str(title).replace("\"","\"\"")}\","
                        f"\"{str(row['authors']).replace("\"","\"\"")}\","
                        f"\"{str(abstract).replace("\"","\"\"")}\","
                        f"\"{str(row['date']).replace("\"","\"\"")}\","
                        f"\"{str(row['paper_url']).replace("\"","\"\"")}\","
                        f"\"{str(row['score']).replace("\"","\"\"")}\","
                        f"\"{str(cn_title).replace("\"","\"\"")}\","
                        f"\"{str(cn_abstract).replace("\"","\"\"")}\"\n")
                f.flush() # 及时更新文件内容
                time.sleep(1)  # 避免请求过于频繁
            tqdm.write('Translation completed.')
        except RetryError:
            print('Retried 5 times. Translation failed.',file=sys.stderr)
            exit(-1) # 直接退出程序，反正有断点续传

if __name__ == "__main__":
    main()
