# 入门项目：Project HF-Translator (Buggy Paper Translator)

## 背景故事：

> “在科研过程中，我们需要快速浏览海量的英文文献。为了加快扫描文献的速度，我们通常会使用一些大模型来帮我们把扫下来的文献翻译成中文。要在没有本地 GPU 显存的情况下实现这一目标，我们需要利用云端的大模型推理服务。你的任务是：利用 **Hugging Face Inference Providers** 的免费层级（Free Tier），编写一个 Python 脚本，自动将一批英文论文的标题和摘要翻译成中文。
>
> 这是我们组之前一位实习生写的代码 Demo，目标是调用 Hugging Face 的 Inference API 来翻译论文。他虽然把基本的代码逻辑写通了，但他离职前把环境搞乱了，代码也跑不通，还有一堆拼写错误。
>
> 你的任务是：接手这个烂摊子，修复环境依赖，重构代码逻辑，并让它成功跑完 iccv2025.csv 的翻译任务并给出优秀的文献翻译。”

------

## 任务书

**任务目标：**

修复并重构 translator_legacy.py，使其能够稳定、高效地调用 Hugging Face 免费 API 完成翻译任务，将文件夹下的iccv2025.csv翻译为中文。

****

**具体要求**：

0. **准备**：
-[x] 了解一下Hugging Face平台和大模型做翻译的基本原理，注册Hugging Face并获得access_token。
1. =**环境修复**：
   - [x] (To be improved) `requirements.txt` 中包含无法安装或错误的包。请修复它，生成一个新的 `requirements_fixed.txt`。
   - [x] **考核点**：你需要识别出哪些包是必须的，哪些是错误的，哪些是多余的。
2. **代码重构**：
   - [x] **API 升级**：弃用过时的接口，改用 `huggingface_hub.InferenceClient` 或 **最新的** `OpenAI` 兼容接口（推荐查阅最新文档https://huggingface.co/docs/inference-providers/en/index），任意一个即可。
   - [x] **模型修正**：修正错误的模型名称，并显式指定 Provider 策略为 `:fastest`。你可以使用任何一个你觉得好用的大模型，推荐使用``openai/gpt-oss-120b:fastest``。除此以外，模型的参数也有若干错误，请了解这些参数都代表着什么，并选择合适的参数。
   - [x] **Prompt 优化**：当前的 Prompt 效果很差，请设计一个更合理的、更适合学术论文的System Prompt。
   - [ ] **异常处理**：增加 `try-except` 和 `tenacity`（或手动）重试机制，防止因网络波动或 Rate Limit (429) 导致程序崩溃。
   - [x] **Token 安全**：**严禁**在代码中硬编码 Token，请改为从环境变量读取。
3. **工程优化 (Bonus)**：
   - [x] **进度显示**：引入 `tqdm` 显示进度。
   - [ ] **断点续传**：如果程序在第 3 条中断，下次运行能否从第 4 条开始？（而不是从头跑）。

**提交物**：

1. 修复后的代码仓库链接（包含 commit 记录）。
2. 运行成功的 `result.csv`。输出格式参考本文件夹下的``example_result.py``。
3. 一份简短的 `FIX_LOG.md`，列出你发现了哪些坑，以及是如何解决的。
4. 一个简单的README，描述这个项目是干什么的，如何配置环境，如何运行。

**注意事项**：
1. 你可以自由地使用任何搜索引擎、AI工具，但我们在面试的时候可能会考核你对代码逻辑（以及其正确性）的理解；
2. 推荐使用git全程管理你的代码。代码完成后提交到一个GitHub仓库并将url发送到randy.bh.li@foxmail.com。邮件标题为【2025科研实习考核-姓名】。