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

            # 去重 - 根据保单号和投保确认时间
            if '保单号' in merged_df.columns and '投保确认时间' in merged_df.columns:
                merged_df = merged_df.drop_duplicates(
                    subset=['保单号', '投保确认时间'],
                    keep='last'
                )

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

        # 筛选指定日期的数据
        daily_data = df[df['投保确认时间'].dt.date == date.date()]

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

        # 筛选时间范围
        mask = (df['投保确认时间'].dt.date >= start_date.date()) & \
               (df['投保确认时间'].dt.date <= end_date.date())
        period_data = df[mask]

        # 按日期分组统计
        daily_stats = period_data.groupby(period_data['投保确认时间'].dt.date).agg({
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
                'weekday': weekday_map[date_obj.weekday()],
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

        return {
            '三级机构': sorted(list(institutions)),
            '团队': sorted(list(teams)),
            '是否续保': sorted(df['是否续保'].dropna().unique().tolist()) if '是否续保' in df.columns else [],
            '是否新能源': sorted(df['是否新能源'].dropna().unique().tolist()) if '是否新能源' in df.columns else [],
            '是否过户车': sorted(df['是否过户车'].dropna().unique().tolist()),
            '险种大类': sorted(df['险种大类'].dropna().unique().tolist()),
            '吨位': sorted(df['吨位分段'].dropna().unique().tolist()),
            '是否电销': ['全部', '是', '否'],
            '机构团队映射': inst_team_map_sorted
        }

    def get_week_comparison(self, metric='premium', filters=None, anchor_date=None):
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

        Returns:
            {
                'latest_date': '2025-11-05',
                'x_axis': ['周三', '周四', '周五', '周六', '周日', '周一', '周二'],
                'series': [
                    {'name': '最近7天(10/30-11/05)', 'data': [...]},
                    {'name': '上个7天(10/23-10/29)', 'data': [...]},
                    {'name': '前个7天(10/16-10/22)', 'data': [...]}
                ]
            }
        """
        if not self.merged_csv.exists():
            return None

        # 读取数据
        df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

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
                'name': f'{"最近" if i==0 else "上个" if i==1 else "前个"}7天({start_date.strftime("%m/%d")}-{end_date.strftime("%m/%d")})',
                'start': start_date,
                'end': end_date
            })

        # 构建X轴(从最近7天的第一天开始的星期序列)
        weekday_map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        first_weekday = periods[0]['start'].weekday()  # 最近7天的第一天是星期几(由anchor_date决定)
        x_axis = []
        for i in range(7):
            x_axis.append(weekday_map[(first_weekday + i) % 7])

        # 统计每个周期的数据
        series = []
        for idx, period in enumerate(periods):
            # 筛选时间范围
            mask = (df['投保确认时间'].dt.date >= period['start'].date()) & \
                   (df['投保确认时间'].dt.date <= period['end'].date())
            period_data = df[mask].copy()

            # 按日期分组统计 - 修复日期计算
            period_data['weekday_index'] = period_data['投保确认时间'].apply(
                lambda x: (x.date() - period['start'].date()).days if pd.notna(x) else -1
            )
            # 过滤掉无效的weekday_index
            period_data = period_data[period_data['weekday_index'] >= 0]

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

            series.append({
                'name': period['name'],
                'data': data,
                'dates': dates,
                'code': 'W' if idx == 0 else f'W-{idx}'
            })

        return {
            'latest_date': latest_date.strftime('%Y-%m-%d'),
            'x_axis': x_axis,
            'series': series
        }

    def get_kpi_windows(self, date=None):
        """
        获取KPI三口径数据：当日(指定日期)、近7天(截至指定日期)、近30天(截至指定日期)

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

        # 锚定日期：默认最新日期
        anchor = df['投保确认时间'].max() if date is None else pd.to_datetime(date)
        if pd.isna(anchor):
            return None

        # 时间范围
        start_7d = anchor - timedelta(days=6)
        start_30d = anchor - timedelta(days=29)

        day_mask = (df['投保确认时间'].dt.date == anchor.date())
        seven_mask = (df['投保确认时间'].dt.date >= start_7d.date()) & (df['投保确认时间'].dt.date <= anchor.date())
        thirty_mask = (df['投保确认时间'].dt.date >= start_30d.date()) & (df['投保确认时间'].dt.date <= anchor.date())

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
            'target_gap_day': target_gap_day
        }

    def _apply_filters(self, df, filters):
        """
        应用筛选条件

        Args:
            df: DataFrame
            filters: 筛选条件字典

        Returns:
            过滤后的DataFrame
        """
        if not filters:
            return df

        # 复制一份避免修改原数据
        filtered_df = df.copy()

        # 三级机构筛选(通过业务员映射)
        if filters.get('三级机构') and filters['三级机构'] != '全部':
            # 构建业务员列表
            staff_list = []
            for staff_key, staff_info in self.staff_mapping.items():
                if staff_info.get('三级机构') == filters['三级机构']:
                    # 提取姓名部分(去掉工号)
                    import re
                    match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
                    if match:
                        staff_list.append(match.group())

            if staff_list:
                filtered_df = filtered_df[filtered_df['业务员'].isin(staff_list)]

        # 团队筛选(通过业务员映射)
        if filters.get('团队') and filters['团队'] != '全部':
            staff_list = []
            for staff_key, staff_info in self.staff_mapping.items():
                if staff_info.get('团队简称') == filters['团队']:
                    import re
                    match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
                    if match:
                        staff_list.append(match.group())

            if staff_list:
                filtered_df = filtered_df[filtered_df['业务员'].isin(staff_list)]

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

        return filtered_df


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
