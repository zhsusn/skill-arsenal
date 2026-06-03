# 大数据架构师 JD 抓取脚本使用说明

> 对应脚本：`interview/jd_scraper_大数据架构师.py`  
> 适用平台：BOSS直聘、拉勾、猎聘（国内主流招聘网站）  
> 目标岗位：大数据架构师 / 数仓架构师 / 数据平台负责人

---

## 一、脚本功能

本脚本用于快速抓取国内主流招聘网站上"大数据架构师"相关职位的 JD（职位描述），并输出为结构化 JSON，供后续标准化分析使用。

| 平台 | 抓取方式 | 数据质量 | 反爬难度 |
|------|---------|---------|---------|
| **BOSS直聘** | `requests` + Cookie | ⭐⭐⭐⭐⭐ 最高 | 中等（需登录 Cookie） |
| **拉勾** | `requests` + Cookie | ⭐⭐⭐⭐ | 中高（需反爬验证） |
| **猎聘** | `requests` / Playwright | ⭐⭐⭐⭐ | 高（建议 Playwright） |

---

## 二、环境准备

### 1. Python 依赖

脚本仅使用标准库 + `requests`，无需额外安装：

```bash
pip install requests
```

如需使用 **Playwright** 备用方案（拉勾/猎聘被拦截时）：

```bash
pip install playwright
playwright install chromium
```

### 2. 创建输出目录

```bash
mkdir data
```

---

## 三、配置 Cookie

### BOSS直聘（推荐优先配置）

BOSS直聘的数据最实时，且大数据架构师岗位数量最多。**必须登录后才能抓取**。

**获取步骤：**
1. 用 Chrome/Edge 打开 [www.zhipin.com](https://www.zhipin.com)
2. 登录账号（建议用手机验证码登录，Cookie 有效期较长）
3. 按 `F12` → 切换到 **Network** 标签 → 刷新页面
4. 任意点击一个请求（如 `joblist.json` 或 `search/joblist.json`）
5. 在右侧 **Headers** 中找到 `Cookie:` 字段
6. 复制完整 Cookie 字符串（需包含 `wt2=` 和 `zp_at=`）
7. 粘贴到脚本第 14 行：
   ```python
   BOSS_COOKIE = "wt2=xxxxxxxx; zp_at=yyyyyyyy; ..."
   ```

> ⚠️ **隐私提醒**：Cookie 包含你的登录凭证，**不要上传到公开仓库**。

### 拉勾（可选）

拉勾的 Cookie 获取方式类似：
1. 登录 [www.lagou.com](https://www.lagou.com)
2. F12 → Network → 刷新 → 复制 Cookie
3. 填入脚本第 17 行 `LAGOU_COOKIE = "..."`

### 猎聘（可选，推荐用 Playwright）

猎聘反爬最强，`requests` 几乎必然被拦截。建议直接使用脚本底部的 **Playwright 备用方案**。

---

## 四、运行脚本

### 方式一：直接运行（BOSS + 拉勾）

```bash
python interview/jd_scraper_大数据架构师.py
```

**预期输出：**
```
=== 开始抓取：大数据架构师 ===

[BOSS] page 1 fetched 30 jobs
[BOSS] page 2 fetched 30 jobs
[BOSS] page 3 fetched 30 jobs
[拉勾] page 1 fetched 15 jobs
[拉勾] page 2 fetched 15 jobs
...

共抓取 95 条原始 JD，保存至 data/jobs_大数据架构师_raw.json
下一步：python .agents/skills/jd-scraper/scripts/normalize.py data/jobs_大数据架构师_raw.json jobs_normalized.json
```

### 方式二：仅运行 Playwright（拉勾/猎聘反爬时）

若 `requests` 被拦截，使用脚本底部注释掉的 Playwright 代码：

```python
# 取消脚本底部的注释，并修改选择器适配实际页面
from playwright.sync_api import sync_playwright

def scrape_with_playwright(url_template, pages=3):
    ...
```

运行方式相同：
```bash
python interview/jd_scraper_大数据架构师.py
```

---

## 五、标准化处理

原始 JSON 包含 HTML 标签、冗余字段，需用项目内的 `normalize.py` 清洗：

```bash
python .agents/skills/jd-scraper/scripts/normalize.py \
  data/jobs_大数据架构师_raw.json \
  data/jobs_大数据架构师_normalized.json
```

**标准化后字段：**

| 字段 | 说明 |
|------|------|
| `id` | 去重哈希（SHA256 前 16 位） |
| `source` | boss / lagou / liepin |
| `title` | 职位名称 |
| `company` | 公司名称 |
| `salary_range` | 薪资范围 |
| `location` | 工作地点 |
| `description_raw` | 清洗后的 JD 纯文本 |
| `skills_extracted` | 自动提取的技术关键词（Python、Spark、Flink 等） |
| `scraped_at` | 抓取时间 |

---

## 六、常见问题

### Q1：BOSS直聘提示 "Cookie 无效" 或返回空数据？

- **原因**：Cookie 过期（通常 24 小时）或缺少关键字段（`wt2`、`zp_at`）。
- **解决**：重新登录 BOSS直聘，按"三、配置 Cookie"步骤重新复制。

### Q2：拉勾返回 `"success": false` 或验证码页面？

- **原因**：拉勾对 IP 和请求频率有严格限制。
- **解决**：
  1. 增加延迟（修改脚本中 `time.sleep(random.uniform(3, 5))`）；
  2. 切换到 Playwright 模式；
  3. 使用住宅代理（不推荐，成本较高）。

### Q3：抓取速度太慢？

- **原因**：脚本内置了 1.5-3 秒随机延迟，避免触发反爬。
- **解决**：不要取消延迟。如需快速获取少量数据，建议直接手动浏览 BOSS直聘，复制 10-20 条 JD 到本地分析。

### Q4：如何抓取其他城市？

修改脚本中的城市代码：

```python
# BOSS直聘城市码
CITY_CODE_BOSS = "101010100"  # 北京
# 其他城市：上海=101020100, 深圳=101280600, 杭州=101210100

# 拉勾城市码
CITY_CODE_LAGOU = "beijing"   # 北京
# 其他城市：shanghai, shenzhen, hangzhou
```

### Q5：如何修改关键词？

```python
KEYWORD = "大数据架构师"
# 可改为："数据仓库架构师"、"实时计算工程师"、"数据平台负责人" 等
```

---

## 七、安全与隐私

1. **Cookie 不外泄**：`BOSS_COOKIE` 和 `LAGOU_COOKIE` 包含个人登录凭证，**切勿提交到 Git 仓库**；
2. **数据不出售**：抓取的 JD 仅用于个人求职分析，禁止转售或用于 ATS 垃圾投递；
3. **频率控制**：单 IP 单日建议抓取不超过 200 条，避免平台封禁账号。

---

## 八、下一步：分析 JD

抓取完成后，你可以：

1. **技能栈对比**：将 `skills_extracted` 与你的简历技能列表做对比，找出缺失项；
2. **薪资调研**：按 `location` + `company_size` 分组，统计薪资中位数；
3. **生成速记卡**：提取高频关键词，制作面试准备清单。

项目内已有一份基于抓取结果的分析报告：  
📄 `interview/数据治理模拟面试_NovaFinTech_Senior.md`（附录：大数据架构师 JD 知识点速报）

如需进一步分析（如词云、技能关联度），可用 Python 快速处理：

```python
import json
from collections import Counter

with open("data/jobs_大数据架构师_normalized.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# 统计技术关键词出现频率
skills = []
for job in jobs:
    skills.extend(job.get("skills_extracted", []))

print(Counter(skills).most_common(20))
```

---

> **维护提示**：本脚本基于 2026 年 6 月各平台的 API/页面结构编写。如平台改版导致解析失败，请检查浏览器开发者工具中的实际请求 URL 和响应结构，并相应调整脚本中的正则或选择器。
