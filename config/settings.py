from config.enums import DetectMode, VulnerabilityType
# 模型参数
MODEL_NAME = 'gpt-4o'
API_KEY = "sk-Zq367BUJF7Jx70LG77GuWOFTd6MuUsqHtWMvh8ItwSXE8wtW"
API_URL = "https://api.vectorengine.ai/v1/chat/completions"

# 检测模式
DETECT_MODES = DetectMode.SOURCE_AND_CFG
DETECT_VUL_TYPE = VulnerabilityType.Missing_Protection_against_Signature_Replay_Attacks

#线程池
MAX_WORKERS = 4

VUL_INFO = 'E:\Project\PycharmProjects\LLM-VDetector\data_base\\vul_info\\' # 漏洞源数据 源码
VUL_CFG_INFO = 'E:\Project\PycharmProjects\LLM-VDetector\data_base\\vul_cfg_info\\'  # 漏洞源数据 CFG
SOURCE_CODE_INFO = 'E:\Project\PycharmProjects\LLM-VDetector\data_base\source_code_info\\'  # prompt数据 源码+CFG
VUL_SOURCE_BASE = 'E:\Project\PycharmProjects\LLM-VDetector\DAppSCAN-source\contracts\\' #漏洞源码数据库
VUL_SOURCE_BYTECODE_BASE = 'E:\Project\PycharmProjects\LLM-VDetector\DAppSCAN-source\\bytecode' # 漏洞字节码数据库
VUL_CFG_BASE = 'E:\Project\PycharmProjects\LLM-VDetector\DAppSCAN-source\\SWCbytecode' # CFG漏洞检测数据

SOURCE_DETECT_OUTPUT_DIR = 'E:\Project\PycharmProjects\LLM-VDetector\experiments\exp_source_detection\\'
CFG_DETECT_OUTPUT_DIR = 'E:\Project\PycharmProjects\LLM-VDetector\experiments\exp_cfg_detection\\'
SOURCE_CFG_DETECT_OUTPUT_DIR = 'E:\Project\PycharmProjects\LLM-VDetector\experiments\exp_cfg_source_detection\\'