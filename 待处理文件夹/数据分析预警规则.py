#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
车险业务数据分析预警规则
基于业务规则与数据洞察文档的预警监控脚本
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class InsuranceDataMonitor:
    """车险数据监控预警类"""
    
    def __init__(self):
        # 业务规则常量定义
        self.VOLATILITY_THRESHOLD = 0.10  # 10%波动率阈值
        self.WEEKEND_GROWTH_THRESHOLD = 10  # 周末增长10倍阈值
        self.INSTITUTION_CONCENTRATION_THRESHOLD = 0.40  # 机构集中度40%阈值
        
        # 客户类别优先级
        self.HIGH_VALUE_CUSTOMER_TYPES = ['非营业个人客车']
        self.FOCUS_CUSTOMER_TYPES = ['摩托车', '非营业货车']
        
        # 险别价值评估
        self.HIGH_VALUE_INSURANCE_TYPES = ['同保主全']
        self.LOW_VALUE_INSURANCE_TYPES = ['同保交三']
        
    def check_daily_volatility(self, daily_data):
        """
        检查日保费波动率预警
        :param daily_data: 按日汇总的保费数据
        :return: 预警信息列表
        """
        alerts = []
        
        # 计算日环比波动率
        daily_data['premium_change'] = daily_data['总保费'].pct_change()
        daily_data['volatility_rate'] = abs(daily_data['premium_change'])
        
        # 筛选超过阈值的异常波动
        abnormal_days = daily_data[daily_data['volatility_rate'] > self.VOLATILITY_THRESHOLD]
        
        for _, row in abnormal_days.iterrows():
            alerts.append({
                'type': '日保费波动异常',
                'date': row['日期'],
                'premium': row['总保费'],
                'change_rate': row['premium_change'],
                'volatility_rate': row['volatility_rate'],
                'severity': '高' if row['volatility_rate'] > 0.20 else '中',
                'description': f"{row['日期']}日保费波动率{row['volatility_rate']:.1%}，超过{self.VOLATILITY_THRESHOLD:.0%}阈值"
            })
        
        return alerts
    
    def check_weekday_comparison(self, weekday_data):
        """
        检查同星期对比异常
        :param weekday_data: 按星期汇总的保费数据
        :return: 预警信息列表
        """
        alerts = []
        
        # 按星期分组计算平均值
        weekday_avg = weekday_data.groupby('星期')['总保费'].mean()
        
        # 检查每个星期的波动
        for weekday in weekday_avg.index:
            weekday_values = weekday_data[weekday_data['星期'] == weekday]['总保费']
            
            if len(weekday_values) >= 3:  # 至少3个数据点
                mean_val = weekday_avg[weekday]
                max_val = weekday_values.max()
                min_val = weekday_values.min()
                
                # 计算极值偏离率
                max_deviation = abs(max_val - mean_val) / mean_val if mean_val > 0 else 0
                min_deviation = abs(min_val - mean_val) / mean_val if mean_val > 0 else 0
                
                if max_deviation > self.VOLATILITY_THRESHOLD:
                    alerts.append({
                        'type': '同星期波动异常',
                        'weekday': weekday,
                        'extreme_value': max_val,
                        'mean_value': mean_val,
                        'deviation_rate': max_deviation,
                        'severity': '高',
                        'description': f"{weekday}出现极值{max_val:.0f}万，偏离平均值{max_deviation:.1%}"
                    })
        
        return alerts
    
    def check_weekend_anomaly(self, daily_data):
        """
        检查周末业务激增异常
        :param daily_data: 按日汇分的保费数据
        :return: 预警信息列表
        """
        alerts = []
        
        # 添加星期信息
        daily_data['星期'] = pd.to_datetime(daily_data['日期']).dt.day_name()
        
        # 计算工作日平均值（排除周末）
        weekday_avg = daily_data[~daily_data['星期'].isin(['Saturday', 'Sunday'])]['总保费'].mean()
        
        # 检查周末数据
        weekend_data = daily_data[daily_data['星期'].isin(['Saturday', 'Sunday'])]
        
        for _, row in weekend_data.iterrows():
            weekend_premium = row['总保费']
            growth_multiple = weekend_premium / weekday_avg if weekday_avg > 0 else 0
            
            if growth_multiple > self.WEEKEND_GROWTH_THRESHOLD:
                alerts.append({
                    'type': '周末业务激增异常',
                    'date': row['日期'],
                    'weekday': row['星期'],
                    'weekend_premium': weekend_premium,
                    'weekday_avg': weekday_avg,
                    'growth_multiple': growth_multiple,
                    'severity': '高',
                    'description': f"{row['日期']}({row['星期']})保费{weekend_premium:.0f}万，是工作日平均的{growth_multiple:.1f}倍"
                })
        
        return alerts
    
    def check_institution_concentration(self, institution_data):
        """
        检查机构集中度风险
        :param institution_data: 按机构汇总的保费数据
        :return: 预警信息列表
        """
        alerts = []
        
        # 计算各机构占比
        total_premium = institution_data['总保费'].sum()
        institution_data['占比'] = institution_data['总保费'] / total_premium
        
        # 检查最大机构占比
        max_institution = institution_data.loc[institution_data['占比'].idxmax()]
        max_ratio = max_institution['占比']
        
        if max_ratio > self.INSTITUTION_CONCENTRATION_THRESHOLD:
            alerts.append({
                'type': '机构集中度过高风险',
                'institution': max_institution['机构名称'],
                'concentration_ratio': max_ratio,
                'premium_amount': max_institution['总保费'],
                'severity': '高' if max_ratio > 0.50 else '中',
                'description': f"{max_institution['机构名称']}占比{max_ratio:.1%}，超过{self.INSTITUTION_CONCENTRATION_THRESHOLD:.0%}阈值"
            })
        
        return alerts
    
    def check_customer_structure(self, customer_data):
        """
        检查客户结构合理性
        :param customer_data: 按客户类别汇总的数据
        :return: 预警信息列表
        """
        alerts = []
        
        # 计算各类别占比
        total_count = customer_data['笔数'].sum()
        customer_data['占比'] = customer_data['笔数'] / total_count
        
        # 检查高价值客户占比
        high_value_customers = customer_data[customer_data['客户类别'].isin(self.HIGH_VALUE_CUSTOMER_TYPES)]
        high_value_ratio = high_value_customers['占比'].sum()
        
        # 检查关注客户占比
        focus_customers = customer_data[customer_data['客户类别'].isin(self.FOCUS_CUSTOMER_TYPES)]
        focus_customers_ratio = focus_customers['占比'].sum()
        
        # 生成客户结构分析报告
        alerts.append({
            'type': '客户结构分析',
            'high_value_ratio': high_value_ratio,
            'focus_customers_ratio': focus_customers_ratio,
            'severity': '信息',
            'description': f"高价值客户占比{high_value_ratio:.1%}，关注客户占比{focus_customers_ratio:.1%}"
        })
        
        return alerts
    
    def check_insurance_combination(self, insurance_data):
        """
        检查险别组合结构
        :param insurance_data: 按险别组合汇总的数据
        :return: 预警信息列表
        """
        alerts = []
        
        # 计算各险别占比
        total_count = insurance_data['笔数'].sum()
        insurance_data['占比'] = insurance_data['笔数'] / total_count
        
        # 检查单交业务占比
        single_insurance = insurance_data[insurance_data['险别组合'] == '单交']
        single_ratio = single_insurance['占比'].iloc[0] if not single_insurance.empty else 0
        
        # 检查高价值险别占比
        high_value_insurance = insurance_data[insurance_data['险别组合'].isin(self.HIGH_VALUE_INSURANCE_TYPES)]
        high_value_ratio = high_value_insurance['占比'].sum()
        
        if single_ratio > 0.45:  # 单交业务占比过高
            alerts.append({
                'type': '商业险渗透率低',
                'single_insurance_ratio': single_ratio,
                'high_value_ratio': high_value_ratio,
                'severity': '中',
                'description': f"单交业务占比{single_ratio:.1%}，商业险渗透率有待提升"
            })
        
        return alerts
    
    def generate_monitoring_report(self, data_dict):
        """
        生成完整的监控报告
        :param data_dict: 包含各类数据的数据字典
        :return: 完整监控报告
        """
        report = {
            '监控时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '预警规则版本': '1.0',
            '预警结果': {}
        }
        
        # 执行各项检查
        all_alerts = []
        
        if 'daily_data' in data_dict:
            all_alerts.extend(self.check_daily_volatility(data_dict['daily_data']))
            all_alerts.extend(self.check_weekend_anomaly(data_dict['daily_data']))
        
        if 'weekday_data' in data_dict:
            all_alerts.extend(self.check_weekday_comparison(data_dict['weekday_data']))
        
        if 'institution_data' in data_dict:
            all_alerts.extend(self.check_institution_concentration(data_dict['institution_data']))
        
        if 'customer_data' in data_dict:
            all_alerts.extend(self.check_customer_structure(data_dict['customer_data']))
        
        if 'insurance_data' in data_dict:
            all_alerts.extend(self.check_insurance_combination(data_dict['insurance_data']))
        
        # 按严重程度分类
        high_alerts = [alert for alert in all_alerts if alert.get('severity') == '高']
        medium_alerts = [alert for alert in all_alerts if alert.get('severity') == '中']
        info_alerts = [alert for alert in all_alerts if alert.get('severity') == '信息']
        
        report['预警结果'] = {
            '总计预警数量': len(all_alerts),
            '高优先级预警': len(high_alerts),
            '中优先级预警': len(medium_alerts),
            '信息类预警': len(info_alerts),
            '详细预警列表': all_alerts
        }
        
        return report

def main():
    """主函数：演示监控功能"""
    monitor = InsuranceDataMonitor()
    
    # 这里可以加载实际数据并运行监控
    print("车险业务数据监控预警系统已初始化")
    print("支持的监控功能：")
    print("1. 日保费波动异常监控")
    print("2. 同星期对比异常监控") 
    print("3. 周末业务激增异常监控")
    print("4. 机构集中度过高风险监控")
    print("5. 客户结构分析")
    print("6. 商业险渗透率监控")

if __name__ == "__main__":
    main()