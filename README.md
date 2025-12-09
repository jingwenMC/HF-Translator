# HF-Translator - 论文翻译工具

一个基于 Hugging Face Inference Providers 的免费API，用于批量翻译英文学术论文标题和摘要为中文的工具。

## 功能特点

- 🚀 使用 Hugging Face 免费 API 进行批量翻译
- 📄 支持 CSV 格式的论文数据文件
- 🔄 断点续传功能，支持从上次中断处继续翻译
- 📊 实时进度显示，使用 tqdm 进度条
- 🔧 灵活的配置选项（命令行参数 + 环境变量）
- 🛡️ 完善的错误处理和重试机制
- 🔒 Token 安全管理，不在代码中硬编码

## 环境要求

- Python 3.13

## 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/jingwenMC/HF-Translator
cd HF-Translator
```

### 2. 安装依赖
```bash
pip install -r requirements_fixed.txt
```

### 3. 配置 Hugging Face Token
有两种方式设置 Token：

**方式一：环境变量（推荐）**
```bash
# Linux/macOS
export HF_TOKEN="your_huggingface_token_here"

# Windows (PowerShell)
$env:HF_TOKEN="your_huggingface_token_here"

# Windows (CMD)
set HF_TOKEN=your_huggingface_token_here
```

**方式二：使用命令行参数**  

示例：
```bash
python translator.py papers.csv -t hf_xxx
```

## 使用方法

### 基本用法
```bash
python translator.py input.csv
```
这会使用默认设置翻译 `input.csv` 文件，输出结果为 `result.csv`

### 完整选项
```bash
python translator.py [OPTIONS] <输入文件>
```

#### 参数说明：
- `<输入文件>`：要翻译的CSV文件路径（必需）

#### 选项：
| 选项 | 缩写 | 说明             | 默认值 |
|------|------|----------------|--------|
| `--help` | `-h` | 显示帮助信息         | - |
| `--output` | `-o` | 指定输出文件         | `result.csv` |
| `--token` | `-t` | 手动指定 API Token | 使用环境变量 HF_TOKEN |
| `--url` | `-u` | API基础URL       | `https://router.huggingface.co/v1` |
| `--model` | `-m` | 指定模型           | `openai/gpt-oss-120b:fastest` |

### 示例

1. **基本翻译**：
```bash
python translator.py iccv2025.csv
```

2. **指定输出文件**：
```bash
python translator.py iccv2025.csv -o translated_papers.csv
```

3. **指定模型和Token**：
```bash
python translator.py iccv2025.csv -m deepseek-ai/DeepSeek-V3.2 -t hf_xxx
```

4. **获取帮助**：
```bash
python translator.py -h
```

## 输入文件格式

输入文件必须是CSV格式，包含以下列（顺序不限，但必须有这些列名）：

| 列名 | 说明 | 示例 |
|------|------|------|
| `title` | 论文标题 | "Deep Learning for Computer Vision" |
| `authors` | 作者列表 | "John Doe, Jane Smith" |
| `abstract` | 论文摘要 | "This paper presents a novel approach..." |
| `date` | 发表日期 | "2025-01-15" |
| `paper_url` | 论文链接 | "https://arxiv.org/abs/xxxx.xxxxx" |
| `score` | 评分（可选） | "8.5" |

示例输入文件： 参见iccv2025.csv

## 输出文件格式

输出文件为CSV格式，包含所有原始列，并新增两列：

| 新增列 | 说明 |
|--------|------|
| `title_cn` | 中文标题 |
| `abstract_cn` | 中文摘要 |

示例输出文件：参见result.csv

## 断点续传

工具支持断点续传功能：
- 如果程序中断，重新运行会自动跳过已翻译的记录
- 无需手动管理进度，工具会自动检测已处理的记录
- 每次翻译完成一行后立即写入文件，确保进度保存

## 模型配置

默认使用`openai/gpt-oss-120b:fastest`，不过也可以通过 `-m` 参数指定，例如：
```bash
python translator.py papers.csv -m deepseek-ai/DeepSeek-V3.2
```

## 错误处理

工具包含完善的错误处理机制：

1. **网络重试**：自动重试失败的API请求（最多5次）
2. **速率限制**：内置一定的延迟，避免触发API限制
3. **进度保存**：每次成功翻译后立即保存结果，出错时可以在修正后断点续传

## 注意事项

1. **免费额度**：Hugging Face 免费API有使用限制，请合理安排翻译量
2. **文件编码**：确保CSV文件使用UTF-8编码
3. **翻译质量**：对于专业术语，建议人工核对翻译结果
4. **API稳定性**：如遇API不稳定，建议稍后重试或更换模型

## 故障排除

### 常见问题

1. **"HF_TOKEN is not set"**
   - 解决方法：设置环境变量或使用 `-t` 参数

2. **"429 Too Many Requests"**
   - 解决方法：程序会自动重试，或停止程序，等待一段时间后继续

3. **CSV格式错误**
   - 解决方法：确保输入文件格式正确，包含必需的列

4. **API连接失败**
   - 解决方法：检查网络连接，或尝试更换模型

## 性能优化

- 默认设置已优化平衡速度和稳定性
- 可通过调整 `time.sleep()` 值控制请求频率
- 大量翻译时建议分批处理

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。