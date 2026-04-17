from typing import Dict, List, Set
import numpy as np

class FunctionSlicer:
    def __init__(self, group_data: Dict, token_data: Dict, max_token_per_slice):
        """
        初始化函数切片器

        Args:
            group_data: 分组数据 {合约: [[函数组1], [函数组2], ...]}
            token_data: token大小数据 {合约: {函数: token大小}}
            max_token_per_slice: 每个切片的最大token数
        """
        self.group_data = group_data
        self.token_data = token_data
        self.max_token_per_slice = max_token_per_slice

        # 预处理数据
        self.function_groups = self._preprocess_groups()
        self.function_tokens = self._preprocess_tokens()

    def _preprocess_groups(self) -> List[Set[str]]:
        """将分组数据预处理为函数组列表"""
        groups = []
        for contract, func_groups in self.group_data.items():
            for func_group in func_groups:
                # 为每个函数添加合约前缀，避免重名
                full_names = {f"{contract}.{func}" if func else f"{contract}._constructor_"
                              for func in func_group}
                groups.append(full_names)
        return groups

    def _preprocess_tokens(self) -> Dict[str, int]:
        """将token数据预处理为 {完整函数名: token大小}"""
        tokens = {}
        for contract, func_tokens in self.token_data.items():
            for func, token_size in func_tokens.items():
                full_name = f"{contract}.{func}" if func else f"{contract}._constructor_"
                tokens[full_name] = token_size

        return tokens

    def _build_function_to_group_mapping(self) -> Dict[str, int]:
        """建立函数到所属组索引的映射"""
        mapping = {}
        for group_idx, group in enumerate(self.function_groups):
            for func in group:  
                mapping[func] = group_idx


        return mapping

    def slice_functions(self) -> List[Set[str]]:
        """
        主要的切片算法

        返回: 切片列表，每个切片是一组函数名
        """
        # 步骤1: 计算每个组的token大小
        print(self.max_token_per_slice)
        group_sizes = []
        for group in self.function_groups:
            group_size = sum(self.function_tokens.get(func, 0) for func in group)
            group_sizes.append(group_size)
        # 步骤2: 对组按大小排序（从大到小）
        sorted_groups = sorted(
            [(size, idx) for idx, size in enumerate(group_sizes)],
            reverse=True
        )
        # 步骤3: 贪心算法进行分组
        slices = []  # 存储最终的切片
        current_slice = set()  # 当前切片中的函数
        current_size = 0  # 当前切片的token大小

        # 优先处理大组
        for size, group_idx in sorted_groups:
            group = self.function_groups[group_idx]
            group_token = size

            # 如果整个组超过最大限制，需要拆分
            if group_token > self.max_token_per_slice:
                self._split_large_group(group, slices)
                continue

            # 如果当前切片加上这个组不会超过限制，就加入当前切片
            if current_size + group_token <= self.max_token_per_slice:
                current_slice.update(group)
                current_size += group_token
            else:
                # 当前切片已满，保存并开始新切片
                if current_slice:
                    slices.append(current_slice)
                current_slice = set(group)
                current_size = group_token

        # 添加最后一个切片
        if current_slice:
            slices.append(current_slice)

        # 步骤4: 处理可能遗漏的独立函数
        self._handle_remaining_functions(slices)

        return slices

    def _split_large_group(self, group: Set[str], slices: List[Set[str]]):
        """拆分超过限制的大组"""
        # 按函数token大小排序
        sorted_funcs = sorted(
            [(self.function_tokens[func], func) for func in group],
            reverse=True
        )

        current_slice = set()
        current_size = 0

        for token_size, func in sorted_funcs:
            if current_size + token_size <= self.max_token_per_slice:
                current_slice.add(func)
                current_size += token_size
            else:
                if current_slice:
                    slices.append(current_slice)
                current_slice = {func}
                current_size = token_size

        if current_slice:
            slices.append(current_slice)

    def _handle_remaining_functions(self, slices: List[Set[str]]):
        """处理可能遗漏的独立函数"""
        all_sliced_funcs = set()
        for slice_group in slices:
            all_sliced_funcs.update(slice_group)

        # 找出所有函数中未被切片的
        all_funcs = set(self.function_tokens.keys())
        remaining_funcs = all_funcs - all_sliced_funcs

        if not remaining_funcs:
            return

        # 将剩余函数按token大小排序
        sorted_remaining = sorted(
            [(self.function_tokens[func], func) for func in remaining_funcs],
            reverse=True
        )

        # 尝试将剩余函数加入到现有切片中
        for token_size, func in sorted_remaining:
            added = False
            for slice_group in slices:
                slice_size = sum(self.function_tokens[f] for f in slice_group)
                if slice_size + token_size <= self.max_token_per_slice:
                    slice_group.add(func)
                    added = True
                    break

            if not added:
                # 创建新切片
                slices.append({func})

    def optimize_slices(self, slices: List[Set[str]]) -> List[Set[str]]:
        """优化切片分布，使其更加平衡"""
        # 计算当前切片的大小分布
        slice_sizes = [sum(self.function_tokens[f] for f in slice_group) for slice_group in slices]

        # 如果已经很平衡，直接返回
        if max(slice_sizes) <= self.max_token_per_slice and max(slice_sizes) - min(slice_sizes) < 20000:
            return slices

        # 重新平衡切片
        optimized_slices = []
        all_funcs = []

        # 收集所有函数并按相关性排序
        for slice_group in slices:
            for func in slice_group:
                all_funcs.append((self.function_tokens[func], func))

        # 按token大小排序
        all_funcs.sort(reverse=True)

        # 使用最佳适应递减算法重新分组
        current_slice = set()
        current_size = 0

        for token_size, func in all_funcs:
            # 尝试找到最适合的现有切片
            best_slice_idx = -1
            best_remaining = float('inf')

            for i, slice_group in enumerate(optimized_slices):
                slice_size = sum(self.function_tokens[f] for f in slice_group)
                if slice_size + token_size <= self.max_token_per_slice:
                    remaining = self.max_token_per_slice - (slice_size + token_size)
                    if remaining < best_remaining:
                        best_remaining = remaining
                        best_slice_idx = i

            if best_slice_idx != -1:
                optimized_slices[best_slice_idx].add(func)
            else:
                # 创建新切片
                if current_size + token_size <= self.max_token_per_slice:
                    current_slice.add(func)
                    current_size += token_size
                else:
                    if current_slice:
                        optimized_slices.append(current_slice)
                    current_slice = {func}
                    current_size = token_size

        if current_slice:
            optimized_slices.append(current_slice)

        return optimized_slices

    def print_slice_statistics(self, slices: List[Set[str]]):
        """打印切片统计信息"""
        print("切片统计信息:")
        print("=" * 50)

        total_token = sum(self.function_tokens.values())
        print(f"总函数数: {len(self.function_tokens)}")
        print(f"总token大小: {total_token}")
        print(f"切片数量: {len(slices)}")
        print(f"每个切片最大限制: {self.max_token_per_slice}")
        print()

        slice_sizes = []
        for i, slice_group in enumerate(slices, 1):
            slice_size = sum(self.function_tokens[f] for f in slice_group)
            slice_sizes.append(slice_size)
            print(f"切片 {i}: {len(slice_group)} 个函数, {slice_size} tokens")
            if slice_size > self.max_token_per_slice:
                print(f" 超过限制!")

        print()
        print(f"最大切片: {max(slice_sizes)} tokens")
        print(f"最小切片: {min(slice_sizes)} tokens")
        print(f"平均切片: {sum(slice_sizes) / len(slice_sizes):.0f} tokens")
        print(f"标准差: {np.std(slice_sizes):.0f} tokens")



