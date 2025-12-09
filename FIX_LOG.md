# HF-Translator Fix Log
## requirements.txt
这里面实在有点杂，我做的基本上是把整个文件删了然后重新写了一遍。  
自己写的时候是直接看代码里面的有效import内容，然后IDE会自动帮我补全缺失的依赖。  
最后直接对着下载下来的库填进去就行。  
还有个办法是用pipreqs库，不过似乎不兼容我的Python版本（3.13）。  
具体修改如下（Linux diff指令结果）：
```
@@ -1,9 +1,5 @@
-# 这里面有一大堆错误、冲突、不必要的包，请修复它。
-pandas==2.0.0
-numpy
-request
-openai==0.27.0
-tensorflow==1.15.0
-tdqm
-huggingface
-python-dotenv==0.1.0
+# 修复好了
+pandas==2.3.3
+openai==2.9.0
+tqdm==4.67.1
+tenacity==9.1.2
```
完全没有一模一样的……  

## translator.py
### import相关错误
import的时候导入了很多无效依赖、甚至有拼写错误。  
直接把源码看一遍就知道要用哪些了。  
具体修改如下（Linux diff指令结果），同时为了扩展一些功能我也引入了自己找的一些依赖：  
```
@@ -1,6 +1,9 @@
+import getopt
+import sys
 import os
 import time
-import request
 import pandas as pd
 from openai import OpenAI
-import qtmd
+from tqdm import tqdm
+from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
+import traceback
```

### 模型调用相关错误
- 首先，我的代码将硬编码的token改为了从环境变量与参数中获取。  
- 其次，我根据HuggingFace的入门教程（ https://huggingface.co/inference/get-started ），将base_url更换为了最新的，同时也将模型修改正确。  
- 然后，我还参考了BabelDoc这个开源文档翻译项目，修改了提示词。  
- 最后，原代码调用模型的参数也有些问题。temperature应该是0~1中的一个数，同时仅为20的max_tokens根本不足以支撑翻译流程。  
  > Temperature: Controls the randomness of the model’s output. Higher values (closer to 1) make output more random, while lower values make the output more deterministic.（取自SiliconFlow平台说明）

  最终我选择了`temperature=0.1` `max_tokens=16384`这一组参数，足以应对绝大多数的翻译情境。

### 文件读写相关错误
文件读写也有相关错误。  
- `row['id']`根本不存在，因为原始输入的csv中并没有id这一列，如果要获取行号的话应该用迭代时的`index`变量。
- `time.sleep(1000)`的含义是休眠1000秒而不是1000毫秒，这不是Java也不是C/C++。
- 还有一些文件格式上的问题，这里就不过多赘述了。

## 总结
总的来讲，这个原始代码真的写的挺烂的。我基本上是按照自己的想法完全重写了一遍整个项目，同时也引入了很多新的东西。可能在最终的过程中有些许疏漏，敬请谅解。期间查资料问AI（而不是用AI直接生成代码）的经历也是个密集的学习过程，真的学到了很多很多……

（FIX_LOG是我自己写的，README是AI帮忙基于我自己的代码生成的，AI在处理文本真的挺强的）