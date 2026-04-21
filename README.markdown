# LLM-VDetector

基于大语言模型（LLM），结合智能合约源码与控制流图（CFG）实现自动化漏洞检测。

## 环境依赖

- python 3.12
- Windows
- pygments 2.19

## 项目数据集 

GitHub: DAppScan

## 运行

### 提取数据集漏洞源信息

在进行漏洞检测之前，需要先提取数据集中漏洞源的源代码、和 CFG（控制流图）信息，并生成用于 Prompt 的格式化数据。

#### 参数配置

在执行数据提取脚本前，请根据实际环境修改以下路径配置（config/settings.py）：

| 参数名 | 说明 | 
|------------------|---------------|
| `VUL_INFO` | 漏洞源数据（源码）输出目录 | 
| `VUL_CFG_INFO` | 漏洞源数据（CFG）输出目录 |
| `SOURCE_CODE_INFO` | Prompt 数据（源码 + CFG）输出目录 | 
| `VUL_SOURCE_BASE` | 漏洞源码数据库路径 | 
| `VUL_SOURCE_BYTECODE_BASE` | 漏洞字节码数据库路径 | 
| `VUL_CFG_BASE` | CFG源漏洞检测数据 |


##### 提取源码漏洞信息

/data_preparation/

运行 `python prepare_data.py` 脚本，从数据集中提取源码漏洞信息，用以对比LLM检测结果

运行 `python prepare_data_CFG.py` 脚本，一是从数据集中提取CFG漏洞信息，用以对比LLM检测结果；而是提取源码以及对应的CFG信息，用于生成prompt

运行 `python fileter_source_code.py` 脚本，根据 `prepare_data.py` 脚本运行结果，从数据集中提取漏洞信息对应的源码文件，用于生成prompt

### 漏洞检测

#### 修改检测配置信息 

数据准备完成后，修改配置信息（config/settings.py）

 | 参数名 | 说明 | 
 |--------|------|
 |DETECT_MODES  | 检测模式| 
 |DETECT_VUL_TYPE | 漏洞类型 |
 |SOURCE_DETECT_OUTPUT_DIR | 仅源码检测保存路径 |
 |CFG_DETECT_OUTPUT_DIR | 仅CFG检测保存路径 |
 |SOURCE_CFG_DETECT_OUTPUT_DIR| 源码和CFG保存路径 |

#### 开始进行漏洞检测

/llm_detect/

执行主程序 `python main.py`
