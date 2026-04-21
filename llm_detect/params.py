from config import settings


class DetectParams:
    """融合不同模式的参数配置"""

    def __init__(self, mode=None):
        self.mode = mode
        # 根据mode值初始化其他参数
        if mode == 'SOURCE_ONLY':
            self._init_source_mode()
        elif mode == 'CFG_ONLY':
            self._init_cfg_mode()
        elif mode == 'SOURCE_AND_CFG':
            self._init_cfg_source_mode()
        else:
            self._init_default()

    def _init_source_mode(self):
        """初始化源码检测模式参数"""
        self.source_code_path = settings.SOURCE_CODE_INFO
        self.vul_type = settings.DETECT_VUL_TYPE
        self.output = settings.SOURCE_DETECT_OUTPUT_DIR

    def _init_cfg_mode(self):
        """初始化CFG检测模式参数"""
        self.source_code_path = settings.SOURCE_CODE_INFO
        self.vul_type = settings.DETECT_VUL_TYPE
        self.output = settings.CFG_DETECT_OUTPUT_DIR

    def _init_cfg_source_mode(self):
        """初始化CFG+源码融合检测模式参数"""
        self.source_code_path = settings.SOURCE_CODE_INFO
        self.vul_type = settings.DETECT_VUL_TYPE
        self.output = settings.SOURCE_CFG_DETECT_OUTPUT_DIR

    def _init_default(self):
        """初始化默认参数"""
        self.source_code_path = settings.SOURCE_CODE_INFO
        self.vul_type = settings.DETECT_VUL_TYPE
        self.output = settings.SOURCE_DETECT_OUTPUT_DIR

    # 添加 getter 方法

    def get_mode(self):
        """获取检测模式"""
        return self.mode

    def get_source_code_path(self):
        """获取prompt 信息"""
        return self.source_code_path

    def get_vul_type(self):
        """获取漏洞类型"""
        return self.vul_type

    def get_output_dir(self):
        """获取输出目录"""
        return self.output
