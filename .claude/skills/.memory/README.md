# 🧠 Project Memory System

## 概述

这是技能系统的**持久化记忆库**，用于存储学习模式、执行历史和系统进化轨迹。

## 架构哲学

### 传统 AI 的局限
```
每次对话 = 全新开始
无记忆 → 重复错误 → 无法进化
```

### 智能体的优势
```
每次执行 = 学习机会
持久记忆 → 模式识别 → 持续优化
```

---

## 文件结构

```
.claude/skills/.memory/
├── project_knowledge.json    # 核心记忆库
├── README.md                 # 本文档
└── backups/                  # 自动备份（未来）
    └── YYYY-MM-DD/
```

---

## Memory Schema

### 1. Metadata (元数据)
```json
{
  "created": "ISO 8601 timestamp",
  "last_updated": "ISO 8601 timestamp",
  "version": "semantic version"
}
```

### 2. Patterns (模式库)
记录识别出的问题-解决方案模式

```json
{
  "problems": [
    {
      "signature": "问题特征（用于匹配）",
      "frequency": "出现次数",
      "last_seen": "最后一次出现时间",
      "typical_context": "典型场景描述"
    }
  ],
  "solutions": [
    {
      "problem_signature": "对应的问题特征",
      "solution": "解决方案描述",
      "success_rate": "成功率 0.0-1.0",
      "total_applications": "应用次数"
    }
  ]
}
```

**核心价值**：
- 下次遇到相似问题，直接提供已验证的解决方案
- 基于成功率推荐最优方案

### 3. Evolution (演进历史)
追踪技能系统的变化轨迹

```json
{
  "skill_changes": [
    {
      "timestamp": "变更时间",
      "skill": "技能名称",
      "change_type": "变更类型 (major_upgrade/split/merge/deprecate)",
      "version": "版本变化",
      "description": "变更描述",
      "impact": "影响评估"
    }
  ],
  "refactoring_history": [
    {
      "timestamp": "重构时间",
      "action": "重构动作",
      "skill": "被重构的技能",
      "result": "结果",
      "metrics": "量化指标"
    }
  ]
}
```

**核心价值**：
- 可视化系统进化路径
- 评估重构效果
- 防止重复重构

### 4. Metrics (性能指标)
量化技能使用效果

```json
{
  "skill_usage": {
    "skill-name": {
      "total_calls": "总调用次数",
      "success_count": "成功次数",
      "avg_duration": "平均执行时间（秒）",
      "last_used": "最后使用时间"
    }
  },
  "performance": {
    "avg_task_completion_time": "平均任务完成时间",
    "total_tasks_completed": "总任务数",
    "success_rate": "整体成功率"
  }
}
```

**核心价值**：
- 识别最常用/最有效的技能
- 发现性能瓶颈
- 优化资源分配

### 5. Learning (学习记录)
从成功和失败中提取知识

```json
{
  "success_patterns": [
    {
      "pattern": "成功模式描述",
      "confidence": "置信度 0.0-1.0",
      "source": "来源"
    }
  ],
  "failure_patterns": [
    {
      "pattern": "失败模式描述",
      "root_cause": "根因分析",
      "prevention": "预防措施"
    }
  ]
}
```

**核心价值**：
- 复制成功
- 避免失败
- 建立最佳实践库

### 6. Insights (系统洞察)
主动监控和发现

```json
{
  "last_health_check": "最后健康检查时间",
  "recurring_issues": ["反复出现的问题列表"],
  "improvement_opportunities": ["改进机会列表"],
  "system_evolution_score": {
    "atomicity": "当前原子性评分",
    "target_atomicity": "目标评分",
    "composability": "可组合性评分",
    "state_awareness": "状态感知评分"
  }
}
```

**核心价值**：
- 自我诊断
- 主动优化
- 持续进化

---

## 使用场景

### Scenario 1: 记录技能执行
```python
from skill_orchestrator import learn_from_execution

# 执行某个技能后
outcome = {
    'success': True,
    'duration': 12.5,
    'error': None
}

learn_from_execution('vue-component-dev', '创建新的筛选组件', outcome)
```

**效果**：
- 更新 `skill_usage` 统计
- 记录到 `success_patterns`
- 更新平均执行时间

### Scenario 2: 查询历史模式
```python
from skill_orchestrator import load_project_memory

memory = load_project_memory()

# 查找"Pandas性能问题"的解决方案
for solution in memory['patterns']['solutions']:
    if 'pandas' in solution['problem_signature'].lower():
        print(f"Solution: {solution['solution']}")
        print(f"Success Rate: {solution['success_rate']:.1%}")
```

**效果**：
- 快速找到已验证的解决方案
- 基于成功率决策

### Scenario 3: 评估系统进化
```python
memory = load_project_memory()

evolution_score = memory['insights']['system_evolution_score']

print(f"原子性: {evolution_score['atomicity']} / {evolution_score['target_atomicity']}")
print(f"差距: {evolution_score['target_atomicity'] - evolution_score['atomicity']} points")
```

**效果**：
- 量化系统健康度
- 识别改进方向

---

## 自动维护机制

### 数据清理规则
```python
# 自动执行（未来实现）
def cleanup_old_data():
    """
    1. 删除 6个月前的失败记录
    2. 合并重复的模式
    3. 归档不再使用的技能统计
    """
```

### 备份策略
```python
# 每周自动备份
def backup_memory():
    """
    备份到 .memory/backups/YYYY-MM-DD/
    保留最近 12 周的备份
    """
```

---

## 数据隐私

**注意**：
- ✅ 本地存储，不上传云端
- ✅ 不包含敏感业务数据
- ✅ 只记录技能使用模式和元数据
- ✅ 可随时清空重置

---

## API 参考

### 读取记忆
```python
from skill_orchestrator import load_project_memory

memory = load_project_memory()
# 返回完整的记忆字典
```

### 保存记忆
```python
from skill_orchestrator import save_project_memory

memory['metrics']['performance']['total_tasks_completed'] += 1
save_project_memory(memory)
```

### 初始化记忆
```python
from skill_orchestrator import initialize_project_memory

memory = initialize_project_memory()
# 创建新的记忆库（覆盖现有数据）
```

### 记录学习
```python
from skill_orchestrator import learn_from_execution

learn_from_execution(
    skill_name='backend-data-processor',
    task_description='处理10月数据',
    outcome={
        'success': True,
        'duration': 8.2,
        'error': None
    }
)
```

---

## 进化路线图

### Phase 1: 基础记忆 ✅
- [x] JSON 存储
- [x] 基本统计
- [x] 模式记录

### Phase 2: 智能分析（计划中）
- [ ] 模式自动识别
- [ ] 异常检测
- [ ] 趋势预测

### Phase 3: 主动学习（未来）
- [ ] 从失败中自动提取规则
- [ ] 跨项目学习
- [ ] 知识迁移

---

## 原则

1. **增量学习**：每次执行都是学习机会
2. **模式识别**：自动发现重复模式
3. **持续优化**：基于数据驱动改进
4. **谦逊诚实**：记录失败，承认不足
5. **实事求是**：只存储真实发生的数据

---

**维护者**: skill-refactor (v2.0)
**创建日期**: 2025-11-09
**哲学**: "记忆是智能的基础，学习是进化的动力"
