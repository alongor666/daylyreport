# API 契约

## 任务交代
本文件描述后端需要实现的所有接口、请求参数、响应结构与错误语义，帮助 AI 或工程师无需访问旧仓库即可构建接口层。字段与单位须与 `context.md`、`SCHEMA_CONTRACT.md`、`DESIGN_SYSTEM.md` 保持一致。

## 通用约定
- 基础路径：`/api`。
- 响应格式：`{"success": true|false, ...}`；错误时附 `message`、`code`，并返回适当的 HTTP 状态码。
- 时间格式：`YYYY-MM-DD`（日期）或 `YYYY-MM-DDTHH:MM:SSZ`（UTC）。
- 金额单位：默认“元”；返回给前端的 KPI 需按“万元整数”处理，字段名需注明。
- 占比字段：范围 0~1，由后端计算。

## 接口列表

### 1. POST `/api/refresh`
- **作用**：触发摄取脚本，扫描 `data/inputs/` 并导入。
- **请求**：`{ "batch_date": "2025-11-08" }`（可选，默认当天）。
- **响应**：`{ "success": true, "message": "数据刷新成功", "latest_date": "2025-11-07" }`。
- **错误**：摄取失败返回 500，`message` 包含日志文件路径。

### 2. POST `/api/kpi-windows`
- **请求体**：
```json
{
  "date": "2025-11-07",            // 可选，默认最新日期
  "filters": {                      // 可选，参见 filters 定义
    "三级机构": "乐山",
    "团队": "乐山一部",
    "业务员": "张三",
    "保单号": "6100301030120250001",
    "是否新能源": "是",
    "是否过户车": "否",
    "是否续保": "新保",
    "险种大类": "车险",
    "吨位": "二吨以下",
    "电销": "是",
    "客户类别3": "非营业个人客车"
  },
  "data_scope": "exclude_correction"   // 或 include_correction
}
```
- **响应**：
```json
{
  "success": true,
  "data": {
    "anchor_date": "2025-11-07",
    "premium_wan": {"day": 123, "last7d": 812, "last30d": 3221},
    "policy_count": {"day": 56, "last7d": 402, "last30d": 1680},
    "commission_wan": {"day": 8, "last7d": 63, "last30d": 280},
    "target_gap_wan": {"day": -5},
    "ratios": {
      "telesales": 0.32,
      "new_energy": 0.18,
      "transfer": 0.22,
      "commercial": 0.61,
      "non_local": 0.07
    },
    "validation": {
      "mismatch_count": 12,
      "missing_staff": ["李四"],
      "data_scope": "exclude_correction"
    }
  }
}
```
- **错误**：过滤器类型错误返回 400；无数据返回 404。

### 3. POST `/api/week-comparison`
- **请求体**：
```json
{
  "metric": "premium",             // premium 或 count
  "filters": { ... },
  "date": "2025-11-07",
  "data_scope": "exclude_correction"
}
```
- **响应**：
```json
{
  "success": true,
  "data": {
    "latest_date": "2025-11-07",
    "x_axis": ["周三", "周四", "周五", "周六", "周日", "周一", "周二"],
    "series": [
      {
        "code": "D-14",
        "label": "D-14 (10-24): 781万 ↑ 8.5%",
        "data": [120, 130, ...],
        "dates": ["2025-10-24", ...],
        "total_value": 781,
        "period_index": 2
      },
      { ... D-7 ... },
      { ... D ... }
    ],
    "validation": { "mismatch_count": 12 }
  }
}
```
- **错误**：`metric` 非法返回 400；无数据返回 404。

### 4. GET `/api/filter-options`
- **响应**：
```json
{
  "success": true,
  "data": {
    "三级机构": ["乐山", "天府", ...],
    "团队": ["乐山一部", ...],
    "机构团队映射": {"乐山": ["乐山一部", ...]},
    "业务员": ["张三", "李四"],
    "保单号": ["6100..."],
    "是否续保": ["新保", "续保", "转保"],
    "是否新能源": ["是", "否"],
    "是否过户车": ["是", "否"],
    "是否异地车": ["是", "否"],
    "险种大类": ["车险"],
    "吨位": ["二吨以下"],
    "是否电销": ["全部", "是", "否"],
    "客户类别3": [...]
  }
}
```

### 5. GET `/api/policy-mapping`
- **响应**：
```json
{
  "success": true,
  "data": {
    "policy_to_staff": {"6100...": "张三"},
    "staff_to_info": {"张三": {"三级机构": "乐山", "四级机构": "乐山城区", "团队简称": "乐山一部"}},
    "conflicts": ["李四"]
  }
}
```

### 6. POST `/api/insurance-type-distribution`
- **请求体**：`{"period": "day", "date": "2025-11-07", "filters": {...}, "data_scope": "exclude_correction"}`。
- **响应**：
```json
{
  "success": true,
  "data": {
    "period": "day",
    "period_label": "当日",
    "date_range": "2025-11-07",
    "distribution": [
      {"type": "交强险", "premium_wan": 120, "percentage": 40.5},
      {"type": "商业险", "premium_wan": 177, "percentage": 59.5}
    ],
    "total_premium_wan": 297
  }
}
```

### 7. POST `/api/premium-range-distribution`
- **说明**：输出业务员保费区间分布，区间固定：`<0`、`0-0.5万`、`0.5-1.5万`、`1.5-2万`、`2-3万`、`>=3万`。
- **响应**：
```json
{
  "success": true,
  "data": {
    "period": "last7d",
    "period_label": "近7天",
    "date_range": "2025-11-01 ~ 2025-11-07",
    "distribution": [
      {"range": "<0", "staff_count": 5, "total_premium_wan": -2, "percentage": 3.2},
      {...}
    ],
    "total_staff": 120,
    "total_premium_wan": 812
  }
}
```

### 8. POST `/api/renewal-type-distribution`
- **说明**：按 `是否续保` 或 `车险新业务分类` 统计。
- **响应** 同上一节，`distribution` 数组的 `type` 为 `新保/续保/转保`，附 `count`、`premium_wan`、`percentage`。

### 9. GET `/api/week-trend`
- **请求参数**：`weeks`（1 或 3），`end_date`（可选）。
- **响应**：`{"success": true, "data": [{"date": "2025-11-01", "weekday": "周六", "premium": 12345.6, "policy_count": 12}, ...]}`。

### 10. GET `/api/latest-date`
- 返回最新 `投保确认时间`。

### 11. GET `/api/health`
- 返回 `{ "status": "healthy", "message": "API 服务运行正常" }`。

## 错误码建议
| 代码 | HTTP | 说明 |
|------|------|------|
| DATA_VALIDATION_FAILED | 400 | 请求参数或筛选条件不合法 |
| NO_DATA | 404 | 无匹配数据 |
| INGESTION_ERROR | 500 | 数据摄取失败 |
| INTERNAL_ERROR | 500 | 未处理异常 |

## 契约测试
- 每个接口需提供 JSON Schema（Pydantic）供自动化测试；
- `tests/api/test_contracts.py` 应覆盖典型成功与失败场景。
