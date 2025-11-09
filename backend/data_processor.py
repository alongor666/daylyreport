"""
数据处理模块 - 负责Excel清洗、CSV合并和数据查询
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import glob


class DataProcessor:
    """数据处理器"""

    def __init__(self, data_dir='data', staff_mapping_file='业务员机构团队归属.json'):
        # 获取项目根目录(backend的上一级)
        project_root = Path(__file__).parent.parent

        self.data_dir = project_root / data_dir
        self.staff_mapping_file = project_root / staff_mapping_file
        self.merged_csv = project_root / '车险清单_2025年10-11月_合并.csv'
        self.staff_mapping = self._load_staff_mapping()

    def _build_name_to_info(self):
        """
        构建姓名到机构/团队信息的映射

        说明：
        - 原始映射文件的键为“工号+姓名”的拼接，例如“200049147向轩颉”。
        - 这里通过正则提取中文姓名部分作为键，值为映射中的机构、团队信息。
        - 若同名出现多条且信息不同，将保留最后一条并记录冲突用于校验。

        Returns:
            tuple(dict, list):
                - name_to_info: { 姓名: { '三级机构': str, '四级机构': str, '团队简称': Optional[str] } }
                - conflicts: [ 姓名 ] 存在多条且信息不一致的姓名列表
        """
        import re
        name_to_info = {}
        conflicts = []
        for staff_key, staff_info in (self.staff_mapping or {}).items():
            match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
            if not match:
                continue
            name = match.group()
            existing = name_to_info.get(name)
            if existing and (
                existing.get('三级机构') != staff_info.get('三级机构') or
                existing.get('团队简称') != staff_info.get('团队简称') or
                existing.get('四级机构') != staff_info.get('四级机构')
            ):
                conflicts.append(name)
            name_to_info[name] = {
                '三级机构': staff_info.get('三级机构'),
                '四级机构': staff_info.get('四级机构'),
                '团队简称': staff_info.get('团队简称')
            }
        return name_to_info, sorted(list(set(conflicts)))

    def get_policy_mapping(self):
        """
        获取保单号→业务员→团队/机构映射信息

        说明：
        - 保单号作为唯一标识，从合并清单中提取其对应的业务员姓名。
        - 业务员姓名再通过映射文件获取其团队简称与三级机构信息。
        - 同时返回可能存在的姓名冲突列表，供前端提示与诊断。

        Returns:
            dict: {
              'policy_to_staff': { 保单号: 业务员姓名 },
              'staff_to_info': { 姓名: { '三级机构': str, '四级机构': str, '团队简称': Optional[str] } },
              'conflicts': [ 姓名 ]
            }
        """
        if not self.merged_csv.exists():
            return {'policy_to_staff': {}, 'staff_to_info': {}, 'conflicts': []}

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        # 仅保留有效列
        cols = df.columns
        if '保单号' not in cols or '业务员' not in cols:
            return {'policy_to_staff': {}, 'staff_to_info': {}, 'conflicts': []}

        # 构建保单号→业务员映射
        tmp = df[['保单号', '业务员']].dropna()
        # 若同一保单号出现多条，优先保留第一条（改为 duplicated 更安全）
        # 函数级中文注释：
        # - 背景：部分环境中混合类型（字符串/数字）保单号在 drop_duplicates 过程中可能产生类型不一致警告；
        # - 修复：改用 duplicated 生成布尔掩码，再反选保留首条，避免潜在的 dtype 问题。
        dup_mask = tmp.duplicated(subset=['保单号'], keep='first')
        tmp = tmp[~dup_mask]
        policy_to_staff = {str(r['保单号']): str(r['业务员']) for _, r in tmp.iterrows()}

        # 姓名→机构团队信息
        name_to_info, conflicts = self._build_name_to_info()

        return {
            'policy_to_staff': policy_to_staff,
            'staff_to_info': name_to_info,
            'conflicts': conflicts
        }

    def _load_staff_mapping(self):
        """加载业务员机构团队映射"""
        if self.staff_mapping_file.exists():
            with open(self.staff_mapping_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def process_new_excel(self, excel_path):
        """
        处理新的Excel文件,转换为CSV格式

        Args:
            excel_path: Excel文件路径

        Returns:
            处理后的DataFrame
        """
        print(f"正在处理Excel文件: {excel_path}")

        # 读取Excel文件
        df = pd.read_excel(excel_path)

        print(f"  读取成功: {len(df)} 行, {len(df.columns)} 列")

        # 数据清洗
        df = self._clean_data(df)

        return df

    def _clean_data(self, df):
        """
        数据清洗 - 确保格式符合标准CSV
        """
        # 1. 删除完全为空的行
        df = df.dropna(how='all')

        # 2. 确保日期格式正确
        date_columns = ['刷新时间', '投保确认时间', '保险起期']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # 3. 数值类型转换
        numeric_columns = ['签单/批改保费', '签单数量', '手续费', '手续费含税', '增值税']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 4. 填充缺失值
        df = df.fillna('')

        print(f"  数据清洗完成")

        return df

    def merge_with_existing(self, new_df):
        """
        将新数据与现有CSV合并

        Args:
            new_df: 新的DataFrame

        Returns:
            合并后的DataFrame
        """
        if self.merged_csv.exists():
            print(f"读取现有数据: {self.merged_csv}")
            existing_df = pd.read_csv(self.merged_csv, encoding='utf-8-sig')

            # 合并数据
            merged_df = pd.concat([existing_df, new_df], ignore_index=True)

            # 去重 - 根据保单号和投保确认时间（改用 duplicated 保留最后一条）
            # 函数级中文注释：
            # - 修复点：使用 duplicated 生成掩码并反选，保证对混合类型的兼容性；
            # - 同时尝试统一日期列为 datetime，避免字符串/对象导致的等值对比异常。
            if '保单号' in merged_df.columns and '投保确认时间' in merged_df.columns:
                try:
                    merged_df['投保确认时间'] = pd.to_datetime(merged_df['投保确认时间'], errors='coerce')
                except Exception:
                    pass
                dup_mask = merged_df.duplicated(subset=['保单号', '投保确认时间'], keep='last')
                merged_df = merged_df[~dup_mask]

            print(f"  合并完成: {len(existing_df)} + {len(new_df)} = {len(merged_df)} 行")
        else:
            print(f"  未找到现有数据,创建新文件")
            merged_df = new_df

        return merged_df

    def save_merged_data(self, df):
        """保存合并后的数据"""
        df.to_csv(self.merged_csv, index=False, encoding='utf-8-sig')
        print(f"  数据已保存: {self.merged_csv}")

    def scan_and_process_new_files(self):
        """
        扫描data目录,处理所有新的Excel文件
        """
        if not self.data_dir.exists():
            print(f"警告: 数据目录不存在: {self.data_dir}")
            return

        # 查找所有Excel文件
        excel_files = list(self.data_dir.glob('*.xlsx')) + list(self.data_dir.glob('*.xls'))

        if not excel_files:
            print(f"未找到新的Excel文件")
            return

        print(f"找到 {len(excel_files)} 个Excel文件")

        all_new_data = []

        for excel_file in excel_files:
            try:
                # 处理单个文件
                df = self.process_new_excel(excel_file)
                all_new_data.append(df)

                # 处理完成后移动到已处理目录
                processed_dir = self.data_dir / 'processed'
                processed_dir.mkdir(exist_ok=True)

                new_path = processed_dir / f"{excel_file.stem}_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}{excel_file.suffix}"
                excel_file.rename(new_path)
                print(f"  文件已移动: {new_path}")

            except Exception as e:
                print(f"  处理失败: {e}")

        if all_new_data:
            # 合并所有新数据
            combined_new = pd.concat(all_new_data, ignore_index=True)

            # 与现有数据合并
            final_df = self.merge_with_existing(combined_new)

            # 保存
            self.save_merged_data(final_df)

            print(f"数据更新完成!")

    def get_daily_report(self, date=None):
        """
        获取日报数据

        Args:
            date: 日期(默认为最新日期)

        Returns:
            {
                'date': '2025-11-05',
                'premium': 125000.50,
                'policy_count': 234,
                'commission': 5000.00,
                'target_gap': -15000.00  # 负数表示未完成
            }
        """
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig')

        # 确保日期格式
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 如果未指定日期,使用最新日期
        if date is None:
            date = df['投保确认时间'].max()
        else:
            date = pd.to_datetime(date)

        # 筛选指定日期的数据（使用规范化日期避免类型不一致）
        # 函数级中文注释：
        # - 修复点：用 .dt.normalize() 与锚定日期的 normalize() 比较，避免 .dt.date 产生的 Python 对象类型与 NaT 混合导致的隐性错误。
        anchor = pd.to_datetime(date)
        date_col = df['投保确认时间'].dt.normalize()
        daily_data = df[date_col == anchor.normalize()]

        # 计算KPI
        report = {
            'date': date.strftime('%Y-%m-%d'),
            'premium': float(daily_data['签单/批改保费'].sum()),
            'policy_count': int(daily_data['签单数量'].sum()),
            'commission': float(daily_data['手续费含税'].sum()),
            'target_gap': 0  # TODO: 需要设置目标值
        }

        # 计算目标差距(假设日目标为20万保费)
        daily_target = 200000
        report['target_gap'] = report['premium'] - daily_target

        return report

    def get_week_trend(self, end_date=None, weeks=1):
        """
        获取连续N周的趋势数据

        Args:
            end_date: 结束日期(默认为最新日期)
            weeks: 周数(1=7天, 3=21天)

        Returns:
            [
                {'date': '2025-10-30', 'weekday': '周三', 'premium': 125000},
                ...
            ]
        """
        if not self.merged_csv.exists():
            return []

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig')
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 如果未指定日期,使用最新日期
        if end_date is None:
            end_date = df['投保确认时间'].max()
        else:
            end_date = pd.to_datetime(end_date)

        # 计算开始日期(连续N周)
        days = weeks * 7 - 1
        start_date = end_date - timedelta(days=days)

        # 筛选时间范围（规范化到日，避免 .dt.date 的dtype差异）
        # 函数级中文注释：
        # - 修复点：用 .dt.normalize() 进行日期区间筛选与分组，提升稳定性与向量化性能。
        date_col = df['投保确认时间'].dt.normalize()
        start_norm = start_date.normalize()
        end_norm = end_date.normalize()
        mask = (date_col >= start_norm) & (date_col <= end_norm)
        period_data = df[mask]

        # 按规范化日期分组统计
        daily_stats = period_data.groupby(period_data['投保确认时间'].dt.normalize()).agg({
            '签单/批改保费': 'sum',
            '签单数量': 'sum'
        }).reset_index()

        # 转换为API格式
        trend_data = []
        weekday_map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

        for _, row in daily_stats.iterrows():
            date_obj = pd.to_datetime(row['投保确认时间'])
            trend_data.append({
                'date': date_obj.strftime('%Y-%m-%d'),
                'weekday': weekday_map[date_obj.dayofweek],
                'premium': float(row['签单/批改保费']),
                'policy_count': int(row['签单数量'])
            })

        return trend_data

    def get_latest_date(self):
        """获取数据中的最新日期"""
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
        latest = df['投保确认时间'].max()

        return latest.strftime('%Y-%m-%d') if pd.notna(latest) else None

    def get_filter_options(self):
        """
        获取所有筛选器的可选值

        Returns:
            {
                '三级机构': ['达州', '德阳', ...],
                '团队': ['达州业务一部', '德阳业务三部', ...],
                '是否续保': ['是', '否', ...],
                '是否新能源': ['是', '否', ...],
                '机构团队映射': { '达州': ['业务一部', ...], ... }
            }
        """
        if not self.merged_csv.exists():
            return {}

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)

        # 从映射文件中提取三级机构和团队
        institutions = set()
        teams = set()
        inst_team_map = {}
        for staff_key, staff_info in self.staff_mapping.items():
            inst = staff_info.get('三级机构')
            team = staff_info.get('团队简称')
            if inst:
                institutions.add(inst)
                if inst not in inst_team_map:
                    inst_team_map[inst] = set()
                # 仅记录有效团队名称，剔除'null'
                if team and team != 'null':
                    inst_team_map[inst].add(team)
            if team and team != 'null':
                teams.add(team)

        # 转换映射中的集合为排序列表
        inst_team_map_sorted = {k: sorted(list(v)) for k, v in inst_team_map.items()}

        # 保单号选项（作为唯一标识）
        policy_numbers = sorted(df['保单号'].dropna().astype(str).unique().tolist()) if '保单号' in df.columns else []

        return {
            '三级机构': sorted(list(institutions)),
            '团队': sorted(list(teams)),
            '是否续保': sorted(df['是否续保'].dropna().unique().tolist()) if '是否续保' in df.columns else [],
            '是否新能源': sorted(df['是否新能源'].dropna().unique().tolist()) if '是否新能源' in df.columns else [],
            '是否过户车': sorted(df['是否过户车'].dropna().unique().tolist()),
            '是否异地车': sorted(df['是否异地车'].dropna().unique().tolist()) if '是否异地车' in df.columns else [],
            '险种大类': sorted(df['险种大类'].dropna().unique().tolist()),
            '吨位': sorted(df['吨位分段'].dropna().unique().tolist()),
            '是否电销': ['全部', '是', '否'],
            # ========== 新增：业务类型（客户类别3） ==========
            '客户类别3': sorted(df['客户类别3'].dropna().unique().tolist()) if '客户类别3' in df.columns else [],
            '机构团队映射': inst_team_map_sorted,
            '保单号': policy_numbers,
            '业务员': sorted(df['业务员'].dropna().unique().tolist()) if '业务员' in df.columns else []
        }

    def get_week_comparison(self, metric='premium', filters=None, anchor_date=None, data_scope='exclude_correction'):
        """
        获取3个7天周期对比数据

        Args:
            metric: 'premium'(签单保费) 或 'count'(保单件数)
            filters: 筛选条件字典 {
                '三级机构': 'xxx',
                '团队': 'xxx',
                '新转续': 'xxx',
                '能源类型': 'xxx',
                '是否过户车': 'xxx',
                '险种大类': 'xxx',
                '吨位': 'xxx',
                'is_dianxiao': 'xxx'
            }
            data_scope: 数据口径 ('exclude_correction' 或 'include_correction')

        Returns:
            {
                'latest_date': '2025-11-05',
                'x_axis': ['周三', '周四', '周五', '周六', '周日', '周一', '周二'],
                'series': [
                    {
                        'name': 'D-14 (10-22): 781万',
                        'data': [...],
                        'dates': [...],
                        'code': 'D-14',
                        'total_value': 7814320.5,
                        'period_index': 2
                    },
                    {
                        'name': 'D-7 (10-29): 657万',
                        'data': [...],
                        'dates': [...],
                        'code': 'D-7',
                        'total_value': 6571028.3,
                        'period_index': 1
                    },
                    {
                        'name': 'D (11-05): 791万',
                        'data': [...],
                        'dates': [...],
                        'code': 'D',
                        'total_value': 7906812.0,
                        'period_index': 0
                    }
                ]
            }
        """
        if not self.merged_csv.exists():
            return None

        # 读取数据
        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 应用数据口径过滤
        df = self._apply_data_scope_filter(df, data_scope)

        # 应用筛选条件
        df = self._apply_filters(df, filters)

        # 获取锚定日期(默认使用最新日期)
        latest_date = df['投保确认时间'].max() if anchor_date is None else pd.to_datetime(anchor_date)
        if pd.isna(latest_date):
            return None

        # 计算3个周期的日期范围
        periods = []
        for i in range(3):
            end_date = latest_date - timedelta(days=i*7)
            start_date = end_date - timedelta(days=6)
            periods.append({
                'name': '',  # 暂时留空，后面根据数据填充
                'start': start_date,
                'end': end_date
            })

        # 构建X轴(从最近7天的第一天开始的星期序列)
        weekday_map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        # 使用 pandas 的 dayofweek 保持与向量化索引一致
        first_weekday = periods[0]['start'].dayofweek  # 最近7天的第一天是星期几(由anchor_date决定)
        x_axis = []
        for i in range(7):
            x_axis.append(weekday_map[(first_weekday + i) % 7])

        # 统计每个周期的数据
        series = []
        for idx, period in enumerate(periods):
            # 筛选时间范围（规范化到日）
            date_col = df['投保确认时间'].dt.normalize()
            start_norm = period['start'].normalize()
            end_norm = period['end'].normalize()
            mask = (date_col >= start_norm) & (date_col <= end_norm)
            period_data = df[mask].copy()

            # 按日期分组统计 - 使用向量化计算 weekday_index
            period_data['weekday_index'] = (period_data['投保确认时间'].dt.normalize() - start_norm).dt.days
            # 仅保留当前周期的7天索引范围
            period_data = period_data[(period_data['weekday_index'] >= 0) & (period_data['weekday_index'] < 7)]

            # 根据指标选择聚合列
            if metric == 'count':
                # 保单件数: 保费>=50的记录数
                period_data = period_data[period_data['签单/批改保费'] >= 50]
                daily_stats = period_data.groupby('weekday_index').size()
            else:  # premium
                # 签单保费
                daily_stats = period_data.groupby('weekday_index')['签单/批改保费'].sum()

            # 构造完整7天数据(缺失的填0)
            data = []
            dates = []
            for i in range(7):
                data.append(float(daily_stats.get(i, 0)))
                dates.append((period['start'] + timedelta(days=i)).strftime('%Y-%m-%d'))

            # 计算该周期的总值（用于标签显示）
            total_value = sum(data)

            # 格式化总值：保费取整万，件数取整数
            if metric == 'count':
                value_str = f"{int(total_value)}"
            else:
                value_str = f"{int(total_value / 10000)}万"  # 取整

            # 生成标签：D-X (日期): 数值
            # idx=0 → D, idx=1 → D-7, idx=2 → D-14
            period_label = 'D' if idx == 0 else f'D-{(idx) * 7}'
            date_str = period['end'].strftime('%m-%d')  # 简化日期格式
            label = f"{period_label} ({date_str}): {value_str}"

            series.append({
                'name': label,
                'data': data,
                'dates': dates,
                'code': period_label,
                'total_value': total_value,  # 保存原始总值用于前端计算趋势
                'period_index': idx  # 保存周期索引
            })

        # 验证业务员映射
        validation_result = self._validate_staff_mapping(df)

        # 反转series顺序：从 [D, D-7, D-14] 改为 [D-14, D-7, D]
        # 图表展示时从旧到新更符合时间线认知
        series.reverse()

        return {
            'latest_date': latest_date.strftime('%Y-%m-%d'),
            'x_axis': x_axis,
            'series': series,
            'validation': validation_result
        }

    def get_kpi_windows(self, date=None, filters=None, data_scope='exclude_correction'):
        """
        获取KPI三口径数据：当日(指定日期)、近7天(截至指定日期)、近30天(截至指定日期)

        Args:
            date: 指定日期，默认为最新日期
            filters: 筛选条件字典
            data_scope: 数据口径 ('exclude_correction' 或 'include_correction')

        Returns:
            {
                'anchor_date': 'YYYY-MM-DD',
                'premium': {'day': float, 'last7d': float, 'last30d': float},
                'policy_count': {'day': int, 'last7d': int, 'last30d': int},
                'commission': {'day': float, 'last7d': float, 'last30d': float},
                'target_gap_day': float
            }
        """
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 应用数据口径过滤（中文注释：根据是否包含批改决定样本范围）
        df = self._apply_data_scope_filter(df, data_scope)

        # 应用筛选条件
        df = self._apply_filters(df, filters)

        # 锚定日期：默认最新日期
        anchor = df['投保确认时间'].max() if date is None else pd.to_datetime(date)
        if pd.isna(anchor):
            return None

        # 时间范围
        start_7d = anchor - timedelta(days=6)
        start_30d = anchor - timedelta(days=29)

        # 统一日期比较到“天”的规范化形式，避免 .dt.date 的Python对象比较
        # 函数级中文注释：
        # - 修复点：用 .dt.normalize() 对齐区间边界，保证类型一致与性能优化。
        date_col = df['投保确认时间'].dt.normalize()
        anchor_norm = anchor.normalize()
        start_7d_norm = start_7d.normalize()
        start_30d_norm = start_30d.normalize()

        day_mask = (date_col == anchor_norm)
        seven_mask = (date_col >= start_7d_norm) & (date_col <= anchor_norm)
        thirty_mask = (date_col >= start_30d_norm) & (date_col <= anchor_norm)

        day_df = df[day_mask]
        seven_df = df[seven_mask]
        thirty_df = df[thirty_mask]

        def sum_float(series):
            try:
                return float(series.sum())
            except Exception:
                return 0.0

        def sum_int(series):
            try:
                return int(series.sum())
            except Exception:
                return 0

        # 计算
        premium_day = sum_float(day_df['签单/批改保费'])
        premium_7d = sum_float(seven_df['签单/批改保费'])
        premium_30d = sum_float(thirty_df['签单/批改保费'])

        count_day = sum_int(day_df['签单数量'])
        count_7d = sum_int(seven_df['签单数量'])
        count_30d = sum_int(thirty_df['签单数量'])

        commission_day = sum_float(day_df['手续费含税'])
        commission_7d = sum_float(seven_df['手续费含税'])
        commission_30d = sum_float(thirty_df['手续费含税'])

        # 目标差距(沿用日目标)
        daily_target = 200000
        target_gap_day = premium_day - daily_target

        # ===== 占比计算辅助函数 =====
        def _safe_ratio(numerator: float, denominator: float) -> float:
            """
            函数级中文注释：
            计算占比（numerator/denominator），并进行鲁棒性处理：
            - 当分母<=0或缺失时，返回0.0；
            - 结果范围裁剪至 [0, 1]，避免异常值污染前端展示；
            - 输入参数类型为 float，输出为 float。
            """
            try:
                denom = float(denominator or 0.0)
                num = float(numerator or 0.0)
            except Exception:
                return 0.0
            if denom <= 0:
                return 0.0
            r = num / denom
            if r < 0:
                return 0.0
            if r > 1:
                return 1.0
            return float(r)

        def _mask_telesales(df_):
            """
            函数级中文注释：
            电销判定口径：终端来源为 '0110融合销售' 视作电销。
            若列缺失，返回全 False，避免异常。
            """
            if '终端来源' in df_.columns:
                return df_['终端来源'].astype(str) == '0110融合销售'
            return pd.Series([False] * len(df_), index=df_.index)

        def _mask_new_energy(df_):
            """
            函数级中文注释：
            新能源判定口径：'是否新能源' 列为 '是'。
            缺失时返回全 False。
            """
            if '是否新能源' in df_.columns:
                return df_['是否新能源'].astype(str) == '是'
            return pd.Series([False] * len(df_), index=df_.index)

        def _mask_transfer(df_):
            """
            函数级中文注释：
            过户车判定口径：'是否过户车' 列为 '是'。
            缺失时返回全 False。
            """
            if '是否过户车' in df_.columns:
                return df_['是否过户车'].astype(str) == '是'
            return pd.Series([False] * len(df_), index=df_.index)

        def _mask_mandatory(df_):
            """
            函数级中文注释：
            交强险判定口径：
            - 优先使用 '险种代码' 以 '0301' 开头；
            - 若无，则回退到 '险种名称' 包含 '交强'。
            两列均缺失时返回全 False。
            """
            if '险种代码' in df_.columns:
                code_mask = df_['险种代码'].astype(str).str.startswith('0301')
            else:
                code_mask = pd.Series([False] * len(df_), index=df_.index)
            if '险种名称' in df_.columns:
                name_mask = df_['险种名称'].astype(str).str.contains('交强', na=False)
            else:
                name_mask = pd.Series([False] * len(df_), index=df_.index)
            return code_mask | name_mask

        def _mask_commercial(df_):
            """
            函数级中文注释：
            商业险判定口径：
            - 优先使用 '险种代码' 以 '0312'、'0313'、'0317' 等商业险代码开头；
            - 若无，则回退到 '险种名称' 包含 '商业保险'。
            两列均缺失时返回全 False。
            """
            if '险种代码' in df_.columns:
                code_series = df_['险种代码'].astype(str)
                code_mask = code_series.str.startswith(('0312', '0313', '0317'))
            else:
                code_mask = pd.Series([False] * len(df_), index=df_.index)
            if '险种名称' in df_.columns:
                name_mask = df_['险种名称'].astype(str).str.contains('商业保险', na=False)
            else:
                name_mask = pd.Series([False] * len(df_), index=df_.index)
            return code_mask | name_mask

        def _mask_non_local(df_):
            """
            函数级中文注释：
            异地车判定口径：'是否异地车' 列为 '是'。
            缺失时返回全 False。
            """
            if '是否异地车' in df_.columns:
                return df_['是否异地车'].astype(str) == '是'
            return pd.Series([False] * len(df_), index=df_.index)

        def _mask_single_mandatory(df_):
            """
            函数级中文注释：
            单交判定口径（严格）：'险别组合' 列值严格等于 '单交'。
            说明：不做任何后备或模糊匹配；缺失列时返回全 False。
            """
            if '险别组合' in df_.columns:
                return df_['险别组合'].astype(str).str.strip() == '单交'
            return pd.Series([False] * len(df_), index=df_.index)

        def _mask_new_policy(df_):
            """
            函数级中文注释：
            新保判定口径（严格）：'是否续保' 列值严格等于 '新保'。
            说明：仅做去空格标准化，不进行同义词映射；缺失列时返回全 False。
            """
            if '是否续保' in df_.columns:
                return df_['是否续保'].astype(str).str.strip() == '新保'
            return pd.Series([False] * len(df_), index=df_.index)

        def _mask_loss_business(df_):
            """
            函数级中文注释：
            清亏业务判定口径（严格）：'车险新业务分类' 列值严格等于 '清亏业务'。
            说明：仅做去空格标准化；当列缺失时返回全 False，确保安全。
            """
            if '车险新业务分类' in df_.columns:
                return df_['车险新业务分类'].astype(str).str.strip() == '清亏业务'
            return pd.Series([False] * len(df_), index=df_.index)

        def _ratio_premium(window_df, cond_mask):
            """
            函数级中文注释：
            计算金额占比（保费）：给定时间窗口 DataFrame 和条件掩码，
            - 分子：window_df[cond_mask] 的 '签单/批改保费' 求和；
            - 分母：window_df 的 '签单/批改保费' 求和；
            返回安全比例 [0,1]。
            """
            num = sum_float(window_df.loc[cond_mask, '签单/批改保费'])
            denom = sum_float(window_df['签单/批改保费'])
            return _safe_ratio(num, denom)

        def _ratio_count(window_df, cond_mask):
            """
            函数级中文注释：
            计算件数占比：给定时间窗口 DataFrame 和条件掩码，
            - 分子：window_df[cond_mask] 的 '签单数量' 求和；
            - 分母：window_df 的 '签单数量' 求和；
            返回安全比例 [0,1]。
            """
            num = sum_int(window_df.loc[cond_mask, '签单数量'])
            denom = sum_int(window_df['签单数量'])
            return _safe_ratio(float(num), float(denom))

        # 计算各项占比（按三口径返回，双口径：保费/件数）
        telesales_day_p = _ratio_premium(day_df, _mask_telesales(day_df))
        telesales_7d_p = _ratio_premium(seven_df, _mask_telesales(seven_df))
        telesales_30d_p = _ratio_premium(thirty_df, _mask_telesales(thirty_df))

        telesales_day_c = _ratio_count(day_df, _mask_telesales(day_df))
        telesales_7d_c = _ratio_count(seven_df, _mask_telesales(seven_df))
        telesales_30d_c = _ratio_count(thirty_df, _mask_telesales(thirty_df))

        new_energy_day_c = _ratio_count(day_df, _mask_new_energy(day_df))
        new_energy_7d_c = _ratio_count(seven_df, _mask_new_energy(seven_df))
        new_energy_30d_c = _ratio_count(thirty_df, _mask_new_energy(thirty_df))
        new_energy_day_p = _ratio_premium(day_df, _mask_new_energy(day_df))
        new_energy_7d_p = _ratio_premium(seven_df, _mask_new_energy(seven_df))
        new_energy_30d_p = _ratio_premium(thirty_df, _mask_new_energy(thirty_df))

        transfer_day_c = _ratio_count(day_df, _mask_transfer(day_df))
        transfer_7d_c = _ratio_count(seven_df, _mask_transfer(seven_df))
        transfer_30d_c = _ratio_count(thirty_df, _mask_transfer(thirty_df))
        transfer_day_p = _ratio_premium(day_df, _mask_transfer(day_df))
        transfer_7d_p = _ratio_premium(seven_df, _mask_transfer(seven_df))
        transfer_30d_p = _ratio_premium(thirty_df, _mask_transfer(thirty_df))

        mandatory_day_p = _ratio_premium(day_df, _mask_mandatory(day_df))
        mandatory_7d_p = _ratio_premium(seven_df, _mask_mandatory(seven_df))
        mandatory_30d_p = _ratio_premium(thirty_df, _mask_mandatory(thirty_df))
        mandatory_day_c = _ratio_count(day_df, _mask_mandatory(day_df))
        mandatory_7d_c = _ratio_count(seven_df, _mask_mandatory(seven_df))
        mandatory_30d_c = _ratio_count(thirty_df, _mask_mandatory(thirty_df))

        # 商业险占比：保费/件数双口径
        commercial_day_p = _ratio_premium(day_df, _mask_commercial(day_df))
        commercial_7d_p = _ratio_premium(seven_df, _mask_commercial(seven_df))
        commercial_30d_p = _ratio_premium(thirty_df, _mask_commercial(thirty_df))
        commercial_day_c = _ratio_count(day_df, _mask_commercial(day_df))
        commercial_7d_c = _ratio_count(seven_df, _mask_commercial(seven_df))
        commercial_30d_c = _ratio_count(thirty_df, _mask_commercial(thirty_df))

        # 异地车占比：按件数与保费双口径
        non_local_day_c = _ratio_count(day_df, _mask_non_local(day_df))
        non_local_7d_c = _ratio_count(seven_df, _mask_non_local(seven_df))
        non_local_30d_c = _ratio_count(thirty_df, _mask_non_local(thirty_df))

        non_local_day_p = _ratio_premium(day_df, _mask_non_local(day_df))
        non_local_7d_p = _ratio_premium(seven_df, _mask_non_local(seven_df))
        non_local_30d_p = _ratio_premium(thirty_df, _mask_non_local(thirty_df))

        # 单交占比：严格以 '险别组合=单交' 判定，双口径
        single_mandatory_day_c = _ratio_count(day_df, _mask_single_mandatory(day_df))
        single_mandatory_7d_c = _ratio_count(seven_df, _mask_single_mandatory(seven_df))
        single_mandatory_30d_c = _ratio_count(thirty_df, _mask_single_mandatory(thirty_df))

        single_mandatory_day_p = _ratio_premium(day_df, _mask_single_mandatory(day_df))
        single_mandatory_7d_p = _ratio_premium(seven_df, _mask_single_mandatory(seven_df))
        single_mandatory_30d_p = _ratio_premium(thirty_df, _mask_single_mandatory(thirty_df))

        # 新保占比：严格以 '是否续保=新保' 判定，双口径
        new_policy_day_c = _ratio_count(day_df, _mask_new_policy(day_df))
        new_policy_7d_c = _ratio_count(seven_df, _mask_new_policy(seven_df))
        new_policy_30d_c = _ratio_count(thirty_df, _mask_new_policy(thirty_df))

        new_policy_day_p = _ratio_premium(day_df, _mask_new_policy(day_df))
        new_policy_7d_p = _ratio_premium(seven_df, _mask_new_policy(seven_df))
        new_policy_30d_p = _ratio_premium(thirty_df, _mask_new_policy(thirty_df))

        # 清亏业务占比：严格以 '车险新业务分类=清亏业务' 判定，双口径
        loss_business_day_c = _ratio_count(day_df, _mask_loss_business(day_df))
        loss_business_7d_c = _ratio_count(seven_df, _mask_loss_business(seven_df))
        loss_business_30d_c = _ratio_count(thirty_df, _mask_loss_business(thirty_df))

        loss_business_day_p = _ratio_premium(day_df, _mask_loss_business(day_df))
        loss_business_7d_p = _ratio_premium(seven_df, _mask_loss_business(seven_df))
        loss_business_30d_p = _ratio_premium(thirty_df, _mask_loss_business(thirty_df))

        # 验证业务员映射与保单号一致性
        validation_staff = self._validate_staff_mapping(df)
        validation_policy = self._validate_policy_consistency(df)
        validation_result = {
            **(validation_staff or {'unmatched_staff': [], 'unmatched_count': 0}),
            'policy_consistency': validation_policy
        }

        return {
            'anchor_date': anchor.strftime('%Y-%m-%d'),
            'premium': {
                'day': premium_day,
                'last7d': premium_7d,
                'last30d': premium_30d
            },
            'policy_count': {
                'day': count_day,
                'last7d': count_7d,
                'last30d': count_30d
            },
            'commission': {
                'day': commission_day,
                'last7d': commission_7d,
                'last30d': commission_30d
            },
            'target_gap_day': target_gap_day,
            'ratios': {
                # 电销占比：同时返回保费占比与件数占比
                'telesales': {
                    'premium': {
                        'day': telesales_day_p,
                        'last7d': telesales_7d_p,
                        'last30d': telesales_30d_p
                    },
                    'count': {
                        'day': telesales_day_c,
                        'last7d': telesales_7d_c,
                        'last30d': telesales_30d_c
                    }
                },
                # 新能源占比：同时返回保费与件数口径
                'new_energy': {
                    'premium': {
                        'day': new_energy_day_p,
                        'last7d': new_energy_7d_p,
                        'last30d': new_energy_30d_p
                    },
                    'count': {
                        'day': new_energy_day_c,
                        'last7d': new_energy_7d_c,
                        'last30d': new_energy_30d_c
                    }
                },
                # 过户车占比：同时返回保费与件数口径
                'transfer': {
                    'premium': {
                        'day': transfer_day_p,
                        'last7d': transfer_7d_p,
                        'last30d': transfer_30d_p
                    },
                    'count': {
                        'day': transfer_day_c,
                        'last7d': transfer_7d_c,
                        'last30d': transfer_30d_c
                    }
                },
                # 交强险占比：同时返回保费与件数口径
                'mandatory': {
                    'premium': {
                        'day': mandatory_day_p,
                        'last7d': mandatory_7d_p,
                        'last30d': mandatory_30d_p
                    },
                    'count': {
                        'day': mandatory_day_c,
                        'last7d': mandatory_7d_c,
                        'last30d': mandatory_30d_c
                    }
                },
                # 商业险占比：同时返回保费与件数口径
                'commercial': {
                    'premium': {
                        'day': commercial_day_p,
                        'last7d': commercial_7d_p,
                        'last30d': commercial_30d_p
                    },
                    'count': {
                        'day': commercial_day_c,
                        'last7d': commercial_7d_c,
                        'last30d': commercial_30d_c
                    }
                },
                # 异地车占比：同时返回保费与件数口径
                'non_local': {
                    'premium': {
                        'day': non_local_day_p,
                        'last7d': non_local_7d_p,
                        'last30d': non_local_30d_p
                    },
                    'count': {
                        'day': non_local_day_c,
                        'last7d': non_local_7d_c,
                        'last30d': non_local_30d_c
                    }
                },
                # 单交占比：严格以险别组合=单交识别
                'single_mandatory': {
                    'premium': {
                        'day': single_mandatory_day_p,
                        'last7d': single_mandatory_7d_p,
                        'last30d': single_mandatory_30d_p
                    },
                    'count': {
                        'day': single_mandatory_day_c,
                        'last7d': single_mandatory_7d_c,
                        'last30d': single_mandatory_30d_c
                    }
                },
                # 新保占比：严格以是否续保=新保识别
                'new_policy': {
                    'premium': {
                        'day': new_policy_day_p,
                        'last7d': new_policy_7d_p,
                        'last30d': new_policy_30d_p
                    },
                    'count': {
                        'day': new_policy_day_c,
                        'last7d': new_policy_7d_c,
                        'last30d': new_policy_30d_c
                    }
                },
                # 清亏业务占比：严格以车险新业务分类=清亏业务识别
                'loss_business': {
                    'premium': {
                        'day': loss_business_day_p,
                        'last7d': loss_business_7d_p,
                        'last30d': loss_business_30d_p
                    },
                    'count': {
                        'day': loss_business_day_c,
                        'last7d': loss_business_7d_c,
                        'last30d': loss_business_30d_c
                    }
                }
            },
            'validation': validation_result
        }

    def _apply_data_scope_filter(self, df, data_scope='exclude_correction'):
        """
        应用数据口径过滤 - 根据批改状态过滤数据
        
        Args:
            df: DataFrame
            data_scope: 数据口径 ('exclude_correction' 或 'include_correction')
            
        Returns:
            过滤后的DataFrame
        """
        if data_scope == 'exclude_correction':
            # 不含批改：批单类型为空或缺失
            return df[df['批单类型'].isna() | (df['批单类型'] == '')]
        elif data_scope == 'include_correction':
            # 包含批改：全部数据
            return df
        return df

    def _apply_filters(self, df, filters):
        """
        应用筛选条件

        Args:
            df: DataFrame
            filters: 筛选条件字典

        Returns:
            过滤后的DataFrame

        Note:
            会验证业务员匹配情况，如果有业务员在数据中但不在映射文件中，
            会记录警告信息。

        函数级中文注释：
        - 修复点：业务员筛选兼容“仅姓名”与“工号+姓名”两种格式。
        - 背景：前端 GlobalFilterPanel 使用 policy-mapping 提供的姓名键，
                后端数据列通常为“工号+姓名”。若直接用姓名做等值过滤会导致无匹配。
        - 改进：当传入过滤值为中文姓名时，先从映射文件中反查对应“工号+姓名”集合，
                若存在则按集合过滤；若不存在，则回退为对数据列中文姓名提取后进行匹配。
        """
        import re

        if not filters:
            return df

        # 复制一份避免修改原数据
        filtered_df = df.copy()

        # 验证业务员匹配情况
        self._validate_staff_mapping(filtered_df)

        # 保单号筛选（唯一标识）
        if filters.get('保单号'):
            filtered_df = filtered_df[filtered_df['保单号'].astype(str) == str(filters['保单号'])]
            # 若选择了保单号，强制依据保单对应的业务员进行后续机构/团队的一致性判断
            name_to_info, _ = self._build_name_to_info()
            if '业务员' in filtered_df.columns and not filtered_df.empty:
                staff_name = filtered_df.iloc[0]['业务员']
                staff_info = name_to_info.get(staff_name)
                # 若前端同时传入机构或团队，与映射不一致则忽略前端传值，以映射为准
                if staff_info:
                    if filters.get('三级机构') and filters['三级机构'] != staff_info.get('三级机构'):
                        # 直接覆盖为映射值，保持一致性
                        filters['三级机构'] = staff_info.get('三级机构')
                    if filters.get('团队') and filters['团队'] != staff_info.get('团队简称'):
                        filters['团队'] = staff_info.get('团队简称')

        # 业务员筛选（兼容：中文姓名 或 工号+姓名）
        if filters.get('业务员'):
            import re
            requested = str(filters['业务员']).strip()

            # 判断是否为“工号+姓名”格式：包含数字且长度较长
            is_staff_key_format = bool(re.search(r"\d", requested))

            if is_staff_key_format:
                # 传入为完整 staff_key：直接等值过滤
                filtered_df = filtered_df[filtered_df['业务员'] == requested]
            else:
                # 传入为中文姓名：尝试通过映射文件反查对应的 staff_key 集合
                staff_keys = []
                for staff_key in (self.staff_mapping or {}).keys():
                    match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
                    if match and match.group() == requested:
                        staff_keys.append(staff_key)

                if staff_keys:
                    # 映射命中：按 staff_key 集合过滤
                    filtered_df = filtered_df[filtered_df['业务员'].isin(staff_keys)]
                else:
                    # 映射未命中：回退为对数据列提取中文姓名后匹配
                    def extract_name(value):
                        m = re.search(r'[\u4e00-\u9fa5]+', str(value))
                        return m.group() if m else ''

                    filtered_df = filtered_df[filtered_df['业务员'].apply(lambda v: extract_name(v) == requested)]

        # 三级机构筛选(通过业务员映射)
        if filters.get('三级机构') and filters['三级机构'] != '全部':
            # 构建业务员列表（使用完整的工号+姓名）
            staff_list = []
            for staff_key, staff_info in self.staff_mapping.items():
                if staff_info.get('三级机构') == filters['三级机构']:
                    # 直接使用完整的staff_key（工号+姓名）
                    staff_list.append(staff_key)

            if staff_list:
                filtered_df = filtered_df[filtered_df['业务员'].isin(staff_list)]
            else:
                # 如果没有匹配的业务员，返回空DataFrame
                filtered_df = filtered_df[filtered_df['业务员'].isin([])]

        # 团队筛选(通过业务员映射)
        if filters.get('团队') and filters['团队'] != '全部':
            # 构建业务员列表（使用完整的工号+姓名）
            staff_list = []
            for staff_key, staff_info in self.staff_mapping.items():
                if staff_info.get('团队简称') == filters['团队']:
                    # 直接使用完整的staff_key（工号+姓名）
                    staff_list.append(staff_key)

            if staff_list:
                filtered_df = filtered_df[filtered_df['业务员'].isin(staff_list)]
            else:
                # 如果没有匹配的业务员，返回空DataFrame
                filtered_df = filtered_df[filtered_df['业务员'].isin([])]

        # 是否续保筛选
        if filters.get('是否续保') and filters['是否续保'] != '全部':
            # 如果存在“是否续保”列，按此列过滤；否则回退到“车险新业务分类”
            if '是否续保' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['是否续保'] == filters['是否续保']]
            elif '车险新业务分类' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['车险新业务分类'] == filters['是否续保']]

        # 是否新能源筛选
        if filters.get('是否新能源') and filters['是否新能源'] != '全部':
            filtered_df = filtered_df[filtered_df['是否新能源'] == filters['是否新能源']]

        # 过户车筛选
        if filters.get('是否过户车') and filters['是否过户车'] != '全部':
            filtered_df = filtered_df[filtered_df['是否过户车'] == filters['是否过户车']]

        # 险种大类筛选
        if filters.get('险种大类') and filters['险种大类'] != '全部':
            filtered_df = filtered_df[filtered_df['险种大类'] == filters['险种大类']]

        # 吨位筛选
        if filters.get('吨位') and filters['吨位'] != '全部':
            filtered_df = filtered_df[filtered_df['吨位分段'] == filters['吨位']]

        # 电销筛选
        if filters.get('is_dianxiao') and filters['is_dianxiao'] != '全部':
            is_dianxiao = filters['is_dianxiao'] == '是'
            if is_dianxiao:
                filtered_df = filtered_df[filtered_df['终端来源'] == '0110融合销售']
            else:
                filtered_df = filtered_df[filtered_df['终端来源'] != '0110融合销售']

        # 异地车筛选
        if filters.get('是否异地车') and filters['是否异地车'] != '全部':
            filtered_df = filtered_df[filtered_df['是否异地车'] == filters['是否异地车']]

        # ========== 新增：业务类型筛选（客户类别3） ==========
        if filters.get('business_type') and filters['business_type'] != '全部':
            if '客户类别3' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['客户类别3'] == filters['business_type']]
            else:
                # 如果数据中不存在该字段，记录警告但不中断
                print(f"警告: 数据中不存在'客户类别3'字段，忽略业务类型筛选")

        return filtered_df

    def _validate_policy_consistency(self, df):
        """
        校验保单号→业务员→团队/三级机构的一致性

        说明：
        - 遍历数据中的“保单号、业务员、团队、三级机构”字段，与映射文件的姓名→信息进行比对。
        - 若数据中的团队或三级机构与映射不一致，则记录为不一致的保单号集合。

        Args:
            df (DataFrame): 已应用筛选的数据集

        Returns:
            dict: {
              'mismatch_policies': [保单号...],
              'mismatch_count': int
            }
        """
        if df.empty:
            return {'mismatch_policies': [], 'mismatch_count': 0}

        cols = df.columns
        required = {'保单号', '业务员'}
        if not required.issubset(set(cols)):
            return {'mismatch_policies': [], 'mismatch_count': 0}

        name_to_info, _ = self._build_name_to_info()
        mismatches = []
        for _, r in df.iterrows():
            policy = str(r['保单号'])
            staff_name = str(r['业务员'])
            staff_info = name_to_info.get(staff_name)
            if not staff_info:
                # 若映射中不存在该业务员，交由 unmatched_staff 处理，这里不重复记录
                continue
            # 比对团队与三级机构（若存在这些列）
            if '团队' in cols:
                if pd.notna(r['团队']) and str(r['团队']) != str(staff_info.get('团队简称')):
                    mismatches.append(policy)
                    continue
            if '三级机构' in cols:
                if pd.notna(r['三级机构']) and str(r['三级机构']) != str(staff_info.get('三级机构')):
                    mismatches.append(policy)
                    continue

        mismatches = sorted(list(set(mismatches)))
        return {
            'mismatch_policies': mismatches,
            'mismatch_count': len(mismatches)
        }

    def get_staff_performance_distribution(self, period='day', date=None, filters=None, data_scope='exclude_correction'):
        """
        获取各机构业务员业绩区间分布

        业绩区间划分:
        - <0 (负保费)
        - 0-0.5万
        - 0.5-1.5万
        - 1.5-2万
        - 2-3万
        - >=3万

        Args:
            period: 时间段 (day=当日, last7d=近7天, last30d=近30天)
            date: 指定日期 (默认为最新日期)
            filters: 筛选条件
            data_scope: 数据口径 (exclude_correction=不含批改, include_correction=含批改)

        Returns:
            dict: {
                'period': 'day',
                'period_label': '当日',
                'date_range': '2025-11-08',
                'distribution': [
                    {'range': '<0', 'count': 2, 'percentage': 5.0},
                    {'range': '0-0.5万', 'count': 15, 'percentage': 37.5},
                    ...
                ],
                'total_staff': 40,
                'total_premium': 1580000.50
            }
        """
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 应用筛选条件
        df = self._apply_filters(df, filters)

        # 应用数据口径筛选（是否包含批改单）
        if data_scope == 'exclude_correction' and '签单/批改标识' in df.columns:
            df = df[df['签单/批改标识'] != '批改']

        # 获取锚定日期
        anchor_date = df['投保确认时间'].max() if date is None else pd.to_datetime(date)
        if pd.isna(anchor_date):
            return None

        # 时间范围映射
        if period == 'day':
            start_date = anchor_date
            period_label = '当日'
            date_range = anchor_date.strftime('%Y-%m-%d')
        elif period == 'last7d':
            start_date = anchor_date - timedelta(days=6)
            period_label = '近7天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        elif period == 'last30d':
            start_date = anchor_date - timedelta(days=29)
            period_label = '近30天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        else:
            return None

        # 筛选时间范围（规范化到日，避免 .dt.date 的dtype差异）
        date_col = df['投保确认时间'].dt.normalize()
        if period == 'day':
            mask = date_col == anchor_date.normalize()
        else:
            mask = (date_col >= start_date.normalize()) & (date_col <= anchor_date.normalize())

        period_data = df[mask].copy()

        if period_data.empty:
            return {
                'period': period,
                'period_label': period_label,
                'date_range': date_range,
                'distribution': [
                    {'range': '<0', 'count': 0, 'percentage': 0.0},
                    {'range': '0-0.5万', 'count': 0, 'percentage': 0.0},
                    {'range': '0.5-1.5万', 'count': 0, 'percentage': 0.0},
                    {'range': '1.5-2万', 'count': 0, 'percentage': 0.0},
                    {'range': '2-3万', 'count': 0, 'percentage': 0.0},
                    {'range': '>=3万', 'count': 0, 'percentage': 0.0}
                ],
                'total_staff': 0,
                'total_premium': 0.0
            }

        # 按业务员分组统计保费
        staff_stats = period_data.groupby('业务员').agg({
            '签单/批改保费': 'sum',
            '签单数量': 'sum'
        }).reset_index()

        # 根据时间周期确定天数, 区间阈值按“当日阈值 * 天数”自适应
        period_days = {
            'day': 1,
            'last7d': 7,
            'last30d': 30
        }.get(period, 1)

        def _scale_bound(value):
            if value in (float('-inf'), float('inf')):
                return value
            return value * period_days

        def _format_wan(value):
            wan_value = value / 10000
            if wan_value.is_integer():
                return str(int(wan_value))
            return f"{wan_value:.1f}".rstrip('0').rstrip('.')

        def _format_range_label(min_value, max_value):
            if min_value == float('-inf') and max_value == 0:
                return '<0'
            if max_value == float('inf'):
                return f">={_format_wan(min_value)}万"
            return f"{_format_wan(min_value)}-{_format_wan(max_value)}万"

        base_ranges = [
            {'min': float('-inf'), 'max': 0},
            {'min': 0, 'max': 5000},
            {'min': 5000, 'max': 15000},
            {'min': 15000, 'max': 20000},
            {'min': 20000, 'max': 30000},
            {'min': 30000, 'max': float('inf')}
        ]

        ranges = []
        for r in base_ranges:
            scaled_min = _scale_bound(r['min'])
            scaled_max = _scale_bound(r['max'])
            ranges.append({
                'name': _format_range_label(scaled_min, scaled_max),
                'min': scaled_min,
                'max': scaled_max
            })

        # 统计每个区间的业务员数量
        distribution = []
        total_staff = len(staff_stats)
        total_premium = float(staff_stats['签单/批改保费'].sum())

        for r in ranges:
            if r['max'] == float('inf'):
                count = len(staff_stats[staff_stats['签单/批改保费'] >= r['min']])
            elif r['min'] == float('-inf'):
                count = len(staff_stats[staff_stats['签单/批改保费'] < r['max']])
            else:
                count = len(staff_stats[
                    (staff_stats['签单/批改保费'] >= r['min']) &
                    (staff_stats['签单/批改保费'] < r['max'])
                ])

            percentage = (count / total_staff * 100) if total_staff > 0 else 0

            distribution.append({
                'range': r['name'],
                'count': int(count),
                'percentage': round(percentage, 1)
            })

        return {
            'period': period,
            'period_label': period_label,
            'date_range': date_range,
            'distribution': distribution,
            'total_staff': int(total_staff),
            'total_premium': total_premium
        }

    def _validate_staff_mapping(self, df):
        """
        验证业务员映射匹配情况

        Args:
            df: DataFrame

        Returns:
            dict: 包含未匹配业务员信息的字典
        """
        if df.empty or not self.staff_mapping:
            return {'unmatched_staff': [], 'unmatched_count': 0}

        # 获取数据中的所有业务员
        if '业务员' not in df.columns:
            return {'unmatched_staff': [], 'unmatched_count': 0}

        data_staff = set(df['业务员'].dropna().unique())
        mapping_staff = set()

        # 从映射文件中提取业务员姓名
        for staff_key in self.staff_mapping.keys():
            import re
            match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
            if match:
                mapping_staff.add(match.group())

        # 找出未匹配的业务员
        unmatched_staff = data_staff - mapping_staff

        if unmatched_staff:
            print(f"警告: 以下 {len(unmatched_staff)} 名业务员在数据中存在但在映射文件中未找到:")
            for staff in sorted(unmatched_staff)[:10]:  # 只显示前10个
                print(f"  - {staff}")
            if len(unmatched_staff) > 10:
                print(f"  ... 还有 {len(unmatched_staff) - 10} 个")

        return {
            'unmatched_staff': list(unmatched_staff),
            'unmatched_count': len(unmatched_staff)
        }

    def get_insurance_type_distribution(self, period='day', date=None, filters=None, data_scope='exclude_correction'):
        """
        获取险别组合占比分析

        Args:
            period: 时间段 (day=当日, last7d=近7天, last30d=近30天)
            date: 指定日期 (默认为最新日期)
            filters: 筛选条件
            data_scope: 数据口径 (exclude_correction=不含批改, include_correction=含批改)

        Returns:
            dict: {
                'period': 'day',
                'period_label': '当日',
                'date_range': '2025-11-08',
                'distribution': [
                    {'type': '单交', 'count': 156, 'percentage': 43.8, 'premium': 1250000.50},
                    {'type': '同保主全', 'count': 102, 'percentage': 28.7, 'premium': 980000.00},
                    ...
                ],
                'total_count': 356,
                'total_premium': 5600000.00
            }
        """
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 应用数据口径过滤（必须在筛选条件之前）
        df = self._apply_data_scope_filter(df, data_scope)

        # 应用筛选条件
        df = self._apply_filters(df, filters)

        # 获取锚定日期
        anchor_date = df['投保确认时间'].max() if date is None else pd.to_datetime(date)
        if pd.isna(anchor_date):
            return None

        # 时间范围映射
        if period == 'day':
            start_date = anchor_date
            period_label = '当日'
            date_range = anchor_date.strftime('%Y-%m-%d')
        elif period == 'last7d':
            start_date = anchor_date - timedelta(days=6)
            period_label = '近7天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        elif period == 'last30d':
            start_date = anchor_date - timedelta(days=29)
            period_label = '近30天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        else:
            return None

        # 筛选时间范围（规范化到日，避免 .dt.date 的dtype差异）
        date_col = df['投保确认时间'].dt.normalize()
        if period == 'day':
            mask = date_col == anchor_date.normalize()
        else:
            mask = (date_col >= start_date.normalize()) & (date_col <= anchor_date.normalize())

        period_data = df[mask].copy()

        # 检查字段存在性
        if '单套-险别' not in period_data.columns:
            return {
                'period': period,
                'period_label': period_label,
                'date_range': date_range,
                'distribution': [],
                'total_count': 0,
                'total_premium': 0.0,
                'error': '数据中缺少"单套-险别"字段'
            }

        if period_data.empty:
            return {
                'period': period,
                'period_label': period_label,
                'date_range': date_range,
                'distribution': [],
                'total_count': 0,
                'total_premium': 0.0
            }

        # 按险别组合分组统计
        insurance_stats = period_data.groupby('单套-险别').agg({
            '签单数量': 'sum',
            '签单/批改保费': 'sum'
        }).reset_index()

        total_count = int(insurance_stats['签单数量'].sum())
        total_premium = float(insurance_stats['签单/批改保费'].sum())

        # 构建分布数据（按保费降序排列）
        distribution = []
        for _, row in insurance_stats.iterrows():
            count = int(row['签单数量'])
            premium = float(row['签单/批改保费'])
            percentage = (count / total_count * 100) if total_count > 0 else 0

            distribution.append({
                'type': row['单套-险别'],
                'count': count,
                'premium': premium,
                'percentage': round(percentage, 1)
            })

        # 按保费降序排序
        distribution.sort(key=lambda x: x['premium'], reverse=True)

        return {
            'period': period,
            'period_label': period_label,
            'date_range': date_range,
            'distribution': distribution,
            'total_count': total_count,
            'total_premium': total_premium
        }

    def get_premium_range_distribution(self, period='day', date=None, filters=None, data_scope='exclude_correction'):
        """
        获取业务员保费区间占比分析

        业绩区间划分（按业务员聚合后的保费）:
        - <0 (负保费)
        - 0-0.5万
        - 0.5-1.5万
        - 1.5-2万
        - 2-3万
        - >=3万

        Args:
            period: 时间段 (day=当日, last7d=近7天, last30d=近30天)
            date: 指定日期 (默认为最新日期)
            filters: 筛选条件
            data_scope: 数据口径 (exclude_correction=不含批改, include_correction=含批改)

        Returns:
            dict: {
                'period': 'day',
                'period_label': '当日',
                'date_range': '2025-11-08',
                'distribution': [
                    {'range': '<0', 'staff_count': 2, 'percentage': 4.2, 'total_premium': -5000.00},
                    {'range': '0-0.5万', 'staff_count': 17, 'percentage': 35.4, 'total_premium': 42000.50},
                    ...
                ],
                'total_staff': 48,
                'total_premium': 650000.00
            }
        """
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 应用数据口径过滤（必须在筛选条件之前）
        df = self._apply_data_scope_filter(df, data_scope)

        # 应用筛选条件
        df = self._apply_filters(df, filters)

        # 获取锚定日期
        anchor_date = df['投保确认时间'].max() if date is None else pd.to_datetime(date)
        if pd.isna(anchor_date):
            return None

        # 时间范围映射
        if period == 'day':
            start_date = anchor_date
            period_label = '当日'
            date_range = anchor_date.strftime('%Y-%m-%d')
        elif period == 'last7d':
            start_date = anchor_date - timedelta(days=6)
            period_label = '近7天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        elif period == 'last30d':
            start_date = anchor_date - timedelta(days=29)
            period_label = '近30天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        else:
            return None

        # 筛选时间范围（规范化到日，避免 .dt.date 的dtype差异）
        date_col = df['投保确认时间'].dt.normalize()
        if period == 'day':
            mask = date_col == anchor_date.normalize()
        else:
            mask = (date_col >= start_date.normalize()) & (date_col <= anchor_date.normalize())

        period_data = df[mask].copy()

        if period_data.empty or '业务员' not in period_data.columns:
            return {
                'period': period,
                'period_label': period_label,
                'date_range': date_range,
                'distribution': [],
                'total_staff': 0,
                'total_premium': 0.0
            }

        # 按业务员分组统计保费
        staff_stats = period_data.groupby('业务员').agg({
            '签单/批改保费': 'sum'
        }).reset_index()

        # 定义业绩区间（新增负保费区间，调整其他区间）
        ranges = [
            {'name': '<0', 'min': float('-inf'), 'max': 0},
            {'name': '0-0.5万', 'min': 0, 'max': 5000},
            {'name': '0.5-1.5万', 'min': 5000, 'max': 15000},
            {'name': '1.5-2万', 'min': 15000, 'max': 20000},
            {'name': '2-3万', 'min': 20000, 'max': 30000},
            {'name': '>=3万', 'min': 30000, 'max': float('inf')}
        ]

        total_staff = len(staff_stats)
        total_premium = float(staff_stats['签单/批改保费'].sum())

        # 统计每个区间的业务员数量和保费
        distribution = []
        for r in ranges:
            if r['max'] == float('inf'):
                range_staff = staff_stats[staff_stats['签单/批改保费'] >= r['min']]
            elif r['min'] == float('-inf'):
                range_staff = staff_stats[staff_stats['签单/批改保费'] < r['max']]
            else:
                range_staff = staff_stats[
                    (staff_stats['签单/批改保费'] >= r['min']) &
                    (staff_stats['签单/批改保费'] < r['max'])
                ]

            staff_count = len(range_staff)
            range_premium = float(range_staff['签单/批改保费'].sum())
            percentage = (staff_count / total_staff * 100) if total_staff > 0 else 0

            distribution.append({
                'range': r['name'],
                'staff_count': int(staff_count),
                'total_premium': range_premium,
                'percentage': round(percentage, 1)
            })

        return {
            'period': period,
            'period_label': period_label,
            'date_range': date_range,
            'distribution': distribution,
            'total_staff': int(total_staff),
            'total_premium': total_premium
        }

    def get_renewal_type_distribution(self, period='day', date=None, filters=None, data_scope='exclude_correction'):
        """
        获取新转续占比分析

        Args:
            period: 时间段 (day=当日, last7d=近7天, last30d=近30天)
            date: 指定日期 (默认为最新日期)
            filters: 筛选条件
            data_scope: 数据口径 (exclude_correction=不含批改, include_correction=含批改)

        Returns:
            dict: {
                'period': 'day',
                'period_label': '当日',
                'date_range': '2025-11-08',
                'distribution': [
                    {'type': '续保', 'count': 220, 'percentage': 61.8, 'premium': 3450000.00},
                    {'type': '新保', 'count': 108, 'percentage': 30.3, 'premium': 1680000.00},
                    {'type': '转保', 'count': 28, 'percentage': 7.9, 'premium': 470000.00}
                ],
                'total_count': 356,
                'total_premium': 5600000.00
            }
        """
        if not self.merged_csv.exists():
            return None

        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

        # 应用数据口径过滤（必须在筛选条件之前）
        df = self._apply_data_scope_filter(df, data_scope)

        # 应用筛选条件
        df = self._apply_filters(df, filters)

        # 获取锚定日期
        anchor_date = df['投保确认时间'].max() if date is None else pd.to_datetime(date)
        if pd.isna(anchor_date):
            return None

        # 时间范围映射
        if period == 'day':
            start_date = anchor_date
            period_label = '当日'
            date_range = anchor_date.strftime('%Y-%m-%d')
        elif period == 'last7d':
            start_date = anchor_date - timedelta(days=6)
            period_label = '近7天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        elif period == 'last30d':
            start_date = anchor_date - timedelta(days=29)
            period_label = '近30天'
            date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {anchor_date.strftime('%Y-%m-%d')}"
        else:
            return None

        # 筛选时间范围（规范化到日，避免 .dt.date 的dtype差异）
        date_col = df['投保确认时间'].dt.normalize()
        if period == 'day':
            mask = date_col == anchor_date.normalize()
        else:
            mask = (date_col >= start_date.normalize()) & (date_col <= anchor_date.normalize())

        period_data = df[mask].copy()

        # 检查字段存在性（优先使用"是否续保"，回退到"车险新业务分类"）
        renewal_field = None
        if '是否续保' in period_data.columns:
            renewal_field = '是否续保'
        elif '车险新业务分类' in period_data.columns:
            renewal_field = '车险新业务分类'
        else:
            return {
                'period': period,
                'period_label': period_label,
                'date_range': date_range,
                'distribution': [],
                'total_count': 0,
                'total_premium': 0.0,
                'error': '数据中缺少"是否续保"或"车险新业务分类"字段'
            }

        if period_data.empty:
            return {
                'period': period,
                'period_label': period_label,
                'date_range': date_range,
                'distribution': [],
                'total_count': 0,
                'total_premium': 0.0
            }

        # 按新转续分组统计
        renewal_stats = period_data.groupby(renewal_field).agg({
            '签单数量': 'sum',
            '签单/批改保费': 'sum'
        }).reset_index()

        total_count = int(renewal_stats['签单数量'].sum())
        total_premium = float(renewal_stats['签单/批改保费'].sum())

        # 构建分布数据（按保费降序排列）
        distribution = []
        for _, row in renewal_stats.iterrows():
            count = int(row['签单数量'])
            premium = float(row['签单/批改保费'])
            percentage = (count / total_count * 100) if total_count > 0 else 0

            distribution.append({
                'type': row[renewal_field],
                'count': count,
                'premium': premium,
                'percentage': round(percentage, 1)
            })

        # 按保费降序排序
        distribution.sort(key=lambda x: x['premium'], reverse=True)

        return {
            'period': period,
            'period_label': period_label,
            'date_range': date_range,
            'distribution': distribution,
            'total_count': total_count,
            'total_premium': total_premium,
            'field_used': renewal_field  # 记录使用的字段名
        }


if __name__ == '__main__':
    import sys
    import io

    # 设置输出编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 测试
    processor = DataProcessor()

    print("=" * 60)
    print("开始扫描并处理新文件...")
    print("=" * 60)
    processor.scan_and_process_new_files()

    print("\n" + "=" * 60)
    print("生成日报数据...")
    print("=" * 60)
    report = processor.get_daily_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("生成7天趋势数据...")
    print("=" * 60)
    trend = processor.get_week_trend(weeks=1)
    print(json.dumps(trend[:3], ensure_ascii=False, indent=2))
