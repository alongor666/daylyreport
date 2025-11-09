# 🚀 Skill System v2.0 Usage Examples

**智能体系统实战演示**

---

## Example 1: 主动健康检查

### 场景
系统每天早上自动运行健康检查，发现问题并提供建议。

### 代码
```python
from skill_refactor import generate_autonomous_recommendations

# 自动扫描项目状态
recommendations = generate_autonomous_recommendations()

# 打印报告
print(recommendations['report'])
```

### 预期输出
```markdown
# 🤖 Autonomous System Recommendations

**Generated**: 2025-11-09T08:00:00

---

## 📊 Current State

**Skills**: 16 active
**Codebase**: 23 files changed (7 days)
**Data**: FRESH
**Issues Detected**: 2
**Opportunities Found**: 3

---

## 🎯 Recommended Actions (Priority Order)

### 1. [P1] Run skill-refactor Layer 1 analysis and split 🤖 Auto-fixable

**Rationale**: 3 skills with atomicity < 60
**Effort**: Medium

### 2. [P2] Detected 2 project areas without dedicated skills 👤 Manual

**Rationale**: Detected 2 project areas without dedicated skills
**Effort**: Medium

### 3. [P2] 8 independent skills can execute in parallel 👤 Manual

**Rationale**: 8 independent skills can execute in parallel
**Effort**: Low

---

**Next Step**: Review and approve top-priority actions.
```

### 解读
- 系统自动发现了3个低原子性的技能
- 识别出2个缺失的技能覆盖区域
- 发现了并行执行的优化机会

---

## Example 2: 智能任务分解

### 场景
用户提出需求，系统自动分解为技能执行计划。

### 用户输入
```
"我要新增一个数据导出功能，支持导出Excel和CSV格式"
```

### 代码
```python
from skill_refactor import SkillOrchestrator

# 初始化编排器
orchestrator = SkillOrchestrator()

# 分解任务
plan = orchestrator.decompose_task("我要新增一个数据导出功能，支持导出Excel和CSV格式")

# 查看执行计划
print(f"""
📋 Execution Plan:

Task Type: {plan['task_type']}
Complexity: {plan['complexity']}
Duration: {plan['estimated_duration']}

Execution Phases:
""")

for phase in plan['phases']:
    parallel_badge = "⚡ Parallel" if phase['parallel'] else "→ Sequential"
    print(f"  Phase {phase['phase']} {parallel_badge}: {', '.join(phase['skills'])}")
```

### 预期输出
```
📋 Execution Plan:

Task Type: feature_development
Complexity: medium
Duration: 90-180 minutes

Execution Phases:
  Phase 1 ⚡ Parallel: api-endpoint-design, vue-component-dev
  Phase 2 → Sequential: backend-data-processor
  Phase 3 ⚡ Parallel: field-validation, testing-and-debugging
```

### 解读
系统自动：
1. **识别任务类型**：新功能开发
2. **判断影响层**：前端（导出按钮）+ 后端（API）+ 数据（格式转换）
3. **生成并行计划**：Phase 1 和 Phase 3 可并行，节省时间
4. **估算工作量**：1.5-3小时

---

## Example 3: 从执行中学习

### 场景
每次技能执行后，系统记录结果并更新知识库。

### 代码
```python
import time
from skill_refactor import learn_from_execution, load_project_memory

# 模拟执行一个技能
skill_name = 'backend-data-processor'
task = '处理2025年10月车险数据'

start_time = time.time()

try:
    # 执行任务（这里简化）
    result = process_data('data/车险清单_2025-10.csv')

    # 记录成功
    learn_from_execution(
        skill_name,
        task,
        {
            'success': True,
            'duration': time.time() - start_time,
            'error': None
        }
    )

except Exception as e:
    # 记录失败
    learn_from_execution(
        skill_name,
        task,
        {
            'success': False,
            'duration': time.time() - start_time,
            'error': str(e)
        }
    )

# 查看学习成果
memory = load_project_memory()
stats = memory['metrics']['skill_usage'][skill_name]

print(f"""
📈 Learning Update:

Skill: {skill_name}
Total Calls: {stats['total_calls']}
Success Rate: {stats['success_count'] / stats['total_calls']:.1%}
Avg Duration: {stats['avg_duration']:.1f}s
""")
```

### 预期输出
```
📈 Learning Update:

Skill: backend-data-processor
Total Calls: 15
Success Rate: 93.3%
Avg Duration: 8.2s
```

### 解读
- 系统记录了第15次调用
- 成功率93.3%（14次成功，1次失败）
- 平均执行时间8.2秒（持续优化）

---

## Example 4: 查询历史模式

### 场景
遇到问题时，先查询知识库看是否有已知解决方案。

### 代码
```python
from skill_refactor import load_project_memory

memory = load_project_memory()

# 查询"Pandas性能问题"的解决方案
problem_keyword = 'pandas'

print("🔍 Searching for known solutions...\n")

for solution in memory['patterns']['solutions']:
    if problem_keyword in solution['problem_signature'].lower():
        print(f"""
✅ Found Solution:

Problem: {solution['problem_signature']}
Solution: {solution['solution']}
Success Rate: {solution['success_rate']:.1%}
Applied {solution['total_applications']} times
""")
```

### 预期输出
```
🔍 Searching for known solutions...

✅ Found Solution:

Problem: Pandas MemoryError on large CSV
Solution: Use pd.read_csv with chunksize=10000
Success Rate: 91.7%
Applied 12 times
```

### 解读
- 系统已经遇到过类似问题12次
- 已验证的解决方案成功率91.7%
- 可以直接应用，无需重新探索

---

## Example 5: 系统自我评估

### 场景
定期检查系统健康度，识别改进方向。

### 代码
```python
from skill_refactor import load_project_memory

memory = load_project_memory()
scores = memory['insights']['system_evolution_score']

print("""
🧠 System Self-Assessment

Current State vs Target:
""")

dimensions = [
    ('Atomicity', scores['atomicity'], scores['target_atomicity']),
    ('State Awareness', scores['state_awareness'], scores['target_state_awareness']),
    ('Composability', scores['composability'], scores['target_composability'])
]

for dim, current, target in dimensions:
    gap = target - current
    progress = current / target
    bar = '█' * int(progress * 20) + '░' * (20 - int(progress * 20))

    print(f"{dim:20s} [{bar}] {current}/{target} (gap: {gap})")

# 计算总体成熟度
avg_current = sum(d[1] for d in dimensions) / len(dimensions)
avg_target = sum(d[2] for d in dimensions) / len(dimensions)
maturity = avg_current / avg_target

print(f"\n📊 Overall Maturity: {maturity:.1%}")

if maturity < 0.8:
    print("⚠️  Recommendation: Focus on improving low-score dimensions")
elif maturity < 0.95:
    print("✅ Good progress, fine-tuning needed")
else:
    print("🎉 Excellent! System is highly optimized")
```

### 预期输出
```
🧠 System Self-Assessment

Current State vs Target:

Atomicity            [███████████████░░░░░] 67/88 (gap: 21)
State Awareness      [█████████████░░░░░░░] 58/85 (gap: 27)
Composability        [████████████████░░░░] 72/90 (gap: 18)

📊 Overall Maturity: 74.8%

⚠️  Recommendation: Focus on improving low-score dimensions
```

### 解读
- 当前系统成熟度74.8%
- 状态感知能力最弱，需优先提升
- 明确改进方向和差距

---

## Example 6: 完整工作流

### 场景
从健康检查→任务分解→执行→学习的完整流程。

### 代码
```python
from skill_refactor import (
    generate_autonomous_recommendations,
    SkillOrchestrator,
    learn_from_execution
)
import time

# Step 1: 主动健康检查
print("=" * 60)
print("STEP 1: Proactive Health Check")
print("=" * 60)

health_report = generate_autonomous_recommendations()
print(health_report['report'])

# Step 2: 用户提出任务
print("\n" + "=" * 60)
print("STEP 2: User Task Submission")
print("=" * 60)

user_task = "优化前端数据加载性能"
print(f"User: {user_task}")

# Step 3: 任务分解
print("\n" + "=" * 60)
print("STEP 3: Task Decomposition")
print("=" * 60)

orchestrator = SkillOrchestrator()
plan = orchestrator.decompose_task(user_task)

print(f"Task Type: {plan['task_type']}")
print(f"Complexity: {plan['complexity']}")
print(f"Estimated Duration: {plan['estimated_duration']}\n")

for phase in plan['phases']:
    print(f"Phase {phase['phase']} ({'Parallel' if phase['parallel'] else 'Sequential'})")
    for skill in phase['skills']:
        print(f"  → {skill}")

# Step 4: 执行并学习
print("\n" + "=" * 60)
print("STEP 4: Execution with Learning")
print("=" * 60)

for phase in plan['phases']:
    for skill_name in phase['skills']:
        print(f"\n⚙️  Executing: {skill_name}")
        start = time.time()

        # 模拟执行（实际会调用真实技能）
        time.sleep(0.1)  # 模拟耗时
        success = True  # 模拟成功

        duration = time.time() - start

        # 记录学习
        learn_from_execution(
            skill_name,
            user_task,
            {
                'success': success,
                'duration': duration,
                'error': None
            }
        )

        print(f"   ✅ Completed in {duration:.2f}s")

# Step 5: 展示学习成果
print("\n" + "=" * 60)
print("STEP 5: Learning Summary")
print("=" * 60)

memory = load_project_memory()
total_executions = sum(s['total_calls'] for s in memory['metrics']['skill_usage'].values())
total_success = sum(s['success_count'] for s in memory['metrics']['skill_usage'].values())

print(f"""
📊 System Intelligence:

Total Skill Executions: {total_executions}
Overall Success Rate: {total_success / total_executions:.1%}
Memory Size: {len(str(memory))} bytes
Patterns Learned: {len(memory['learning']['success_patterns'])}
""")

print("\n✅ Workflow Complete! System has evolved.")
```

### 预期输出
```
============================================================
STEP 1: Proactive Health Check
============================================================

# 🤖 Autonomous System Recommendations
[健康报告...]

============================================================
STEP 2: User Task Submission
============================================================

User: 优化前端数据加载性能

============================================================
STEP 3: Task Decomposition
============================================================

Task Type: optimization
Complexity: medium
Estimated Duration: 60-120 minutes

Phase 1 (Parallel)
  → vue-component-dev
  → backend-data-processor
Phase 2 (Sequential)
  → testing-and-debugging

============================================================
STEP 4: Execution with Learning
============================================================

⚙️  Executing: vue-component-dev
   ✅ Completed in 0.11s

⚙️  Executing: backend-data-processor
   ✅ Completed in 0.10s

⚙️  Executing: testing-and-debugging
   ✅ Completed in 0.10s

============================================================
STEP 5: Learning Summary
============================================================

📊 System Intelligence:

Total Skill Executions: 42
Overall Success Rate: 95.2%
Memory Size: 8547 bytes
Patterns Learned: 15

✅ Workflow Complete! System has evolved.
```

---

## 关键洞察

### 1. **状态即真理**
每次执行都从实时状态查询，而非静态文档。

### 2. **组合即智能**
单个技能是工具，编排技能产生智慧。

### 3. **反馈即进化**
每次执行都是学习机会，系统越用越聪明。

### 4. **主动即超越**
不等用户问，自己发现问题并提供建议。

---

## 下一步

1. **运行健康检查**：`generate_autonomous_recommendations()`
2. **实际分解任务**：用你的真实需求测试编排器
3. **积累知识库**：执行10次以上任务，观察学习效果
4. **定期评估**：每周检查系统成熟度

---

**创建日期**: 2025-11-09
**维护**: skill-refactor v2.0
**哲学**: "智能不是程序写出来的，是从数据中学出来的"
