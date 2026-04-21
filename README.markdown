# LLM-VDetector

Based on Large Language Model (LLM), smart contract source code and Control Flow Graph (CFG) were combined to realize automatic vulnerability detection.

## Environment Dependencies

- python 3.12
- Windows
- pygments 2.19

## Project dataset 

GitHub: DAppScan

## Run

### Extract the vulnerability source information of the data set

Before performing vulnerability detection, it is necessary to extract the source code, and CFG (control flow graph) information of the vulnerability source in the dataset, and generate the formatted data for Prompt.

#### Parameter Configuration

Before executing the data extraction script, modify the following path configuration according to your environment (config/settings.py)：

| Parameter  | Comments | 
|------------------|---------------|
| `VUL_INFO` | Vulnerability source data (source code) output directory | 
| `VUL_CFG_INFO` | Vulnerability Source Data (CFG) output directory |
| `SOURCE_CODE_INFO` | Prompt Data (source + CFG) output directory | 
| `VUL_SOURCE_BASE` | Vulnerability source database path | 
| `VUL_SOURCE_BYTECODE_BASE` | Vulnerability bytecode database path | 
| `VUL_CFG_BASE` | CFG source vulnerability detection data |


##### Extract source code vulnerability information

/data_preparation/

Run the 'python prepare_data.py' script to extract the source code vulnerability information from the dataset and compare the LLM detection results.

Run the 'python prepare_data_CFG.py' script. First, extract CFG vulnerability information from the data set to compare the LLM detection results. Instead, the source code and the corresponding CFG information are extracted and used to generate the prompt.

Run the 'python fileter_source_code.py' script, and according to the results of the 'prepare_data.py' script, extract the source code files corresponding to the vulnerability information from the data set to generate the prompt.

### Vulnerability Detection

#### Modify the detection configuration information 

Once the data is ready, modify the configuration information (config/settings.py)

 | Parameter | Comments | 
 |--------|------|
 |DETECT_MODES  | Detection mode| 
 |DETECT_VUL_TYPE | Type of vulnerability |
 |SOURCE_DETECT_OUTPUT_DIR | Source code only detects save paths |
 |CFG_DETECT_OUTPUT_DIR | Only CFG detects save paths |
 |SOURCE_CFG_DETECT_OUTPUT_DIR| Source and CFG save paths |

#### Start vulnerability detection

/llm_detect/

Executing the main program `python main.py`
