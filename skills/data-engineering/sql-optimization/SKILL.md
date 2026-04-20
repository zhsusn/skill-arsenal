---
name: sql-optimization
description: 分析 SQL 查询性能瓶颈，提供索引优化建议、执行计划解读和改写方案。适用于慢查询排查、数据库性能调优和 Schema 设计评审。
metadata:
  tags: "data-engineering,sql,performance"
  platforms: "kimi,claude,cursor,codex,gemini"
---

# SQL Optimization

## 适用场景
- 慢查询日志分析与优化
- 新查询的上线前性能评审
- 数据库 Schema 设计review
- 索引策略评估与建议

## 核心职责
1. 分析 SQL 查询的潜在性能瓶颈
2. 解读执行计划（EXPLAIN / EXPLAIN ANALYZE）
3. 推荐合适的索引策略
4. 提供查询改写方案（等价但性能更优的写法）
5. 评估表结构设计的合理性

## 分析维度

### 1. 查询结构
- 是否使用了 SELECT *（不必要的列会增加 I/O）
- WHERE 条件是否命中索引
- JOIN 顺序是否合理（小表驱动大表）
- 子查询是否可改写为 JOIN 或 EXISTS
- 是否使用了隐式类型转换（导致索引失效）

### 2. 索引使用
- 现有索引是否被使用（Key 列）
- 是否存在冗余或重复索引
- 复合索引的列顺序是否符合最左前缀原则
- 是否需要覆盖索引（Covering Index）减少回表

### 3. 执行计划信号
- 全表扫描（Full Table Scan / Seq Scan）
- 文件排序（Using filesort）
- 临时表（Using temporary）
- 大偏移量分页（LIMIT 100000, 10）

## 输出格式

### 优化报告
```markdown
## SQL 性能分析

### 原始查询
```sql
...
```

### 瓶颈识别
1. **问题**：...
   - **影响**：...
   - **证据**：执行计划 ...

### 优化建议
1. **索引建议**：...
2. **查询改写**：...
3. **Schema 调整**（如需要）：...

### 预期收益
- 执行时间：从 X 降至 Y
- 扫描行数：从 A 降至 B
```

## 示例

### 示例 1：慢查询优化

**输入**：
```sql
SELECT * FROM orders
WHERE status = 'completed'
ORDER BY created_at DESC
LIMIT 100000, 10;
```

**分析输出**：

#### 瓶颈识别
1. **深度分页（Deep Paging）**
   - 影响：MySQL 需要扫描 100010 行，丢弃前 100000 行
   - 证据：EXPLAIN 显示 rows ≈ 100010

2. **SELECT ***
   - 影响：增加回表开销，无法使用覆盖索引

#### 优化建议

**方案 A：基于游标的分页（推荐）**
```sql
SELECT * FROM orders
WHERE status = 'completed'
  AND created_at < '2026-04-01 00:00:00'
ORDER BY created_at DESC
LIMIT 10;
```
- 添加索引：`INDEX idx_status_created_at (status, created_at)`

**方案 B：延迟关联**
```sql
SELECT o.* FROM orders o
JOIN (
    SELECT id FROM orders
    WHERE status = 'completed'
    ORDER BY created_at DESC
    LIMIT 100000, 10
) tmp ON o.id = tmp.id;
```

## 注意事项
- 索引不是越多越好，写操作（INSERT/UPDATE/DELETE）会维护索引，增加开销
- 优化建议需结合具体数据库版本和存储引擎（InnoDB/MyISAM/PostgreSQL 等）
- 大表加索引可能导致锁表，建议在低峰期执行或使用 ONLINE DDL

## 变更日志

- 2026-04-20: 初始版本
