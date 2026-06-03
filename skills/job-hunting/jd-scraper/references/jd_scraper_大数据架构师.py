#!/usr/bin/env python3
"""
大数据架构师 JD 快速抓取脚本
支持：BOSS直聘、拉勾、猎聘
Usage:
  1. 配置下方 COOKIE 和 API_KEY
  2. python jd_scraper_大数据架构师.py
  3. 生成的 raw_jobs.json 用 normalize.py 标准化
"""

import json, time, random, re, hashlib
from datetime import datetime

# ====================== 配置区 ======================

# BOSS直聘：登录后从浏览器开发者工具复制 Cookie（需包含 wt2 和 zp_at）
BOSS_COOKIE = "你的BOSS登录Cookie"

# 拉勾：如需反爬，可配置可选的代理或 Cookie
LAGOU_COOKIE = "你的拉勾Cookie（可选）"

# 猎聘：如需 API 方式，配置 Cookie；否则建议用 Playwright
LIEPIN_COOKIE = "你的猎聘Cookie（可选）"

# 搜索参数
KEYWORD = "大数据架构师"
CITY_CODE_BOSS = "101010100"   # 北京
CITY_CODE_LAGOU = "beijing"    # 拉勾城市码
MAX_PAGES = 3                  # 每平台抓 3 页，约 30-90 条
OUTPUT_RAW = "data/jobs_大数据架构师_raw.json"

# ===================================================

import requests

HEADERS_BOSS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": BOSS_COOKIE,
    "Referer": "https://www.zhipin.com/"
}

HEADERS_LAGOU = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": LAGOU_COOKIE,
    "Referer": "https://www.lagou.com/"
}

HEADERS_LIEPIN = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": LIEPIN_COOKIE,
    "Referer": "https://www.liepin.com/"
}

def scrape_boss():
    jobs = []
    for page in range(1, MAX_PAGES + 1):
        params = {"scene": 1, "query": KEYWORD, "city": CITY_CODE_BOSS, "page": page, "pageSize": 30}
        try:
            resp = requests.get(
                "https://www.zhipin.com/wapi/zpgeek/search/joblist.json",
                headers=HEADERS_BOSS, params=params, timeout=15
            )
            data = resp.json().get("zpData", {}).get("jobList", [])
        except Exception as e:
            print(f"[BOSS] page {page} error: {e}")
            break
        if not data:
            break
        for job in data:
            jobs.append({
                "title": job.get("jobName"),
                "company": job.get("brandName"),
                "salary": job.get("salaryDesc"),
                "location": job.get("cityName"),
                "description": job.get("jobDescribe", ""),
                "industry": job.get("brandIndustry", ""),
                "company_size": job.get("brandScaleName", ""),
                "source": "boss"
            })
        print(f"[BOSS] page {page} fetched {len(data)} jobs")
        time.sleep(random.uniform(1.5, 2.5))
    return jobs

def scrape_lagou():
    """
    拉勾需要 Cookie + 反爬验证，以下为简化版 requests 模板。
    若被拦截，建议改用 Playwright（见下方注释）。
    """
    jobs = []
    url = "https://www.lagou.com/jobs/positionAjax.json"
    for page in range(1, MAX_PAGES + 1):
        payload = {
            "first": "true" if page == 1 else "false",
            "pn": page,
            "kd": KEYWORD,
            "city": CITY_CODE_LAGOU
        }
        try:
            resp = requests.post(url, headers=HEADERS_LAGOU, data=payload, timeout=15)
            result = resp.json()
            content = result.get("content", {})
            positions = content.get("positionResult", {}).get("result", [])
        except Exception as e:
            print(f"[拉勾] page {page} error: {e}")
            break
        if not positions:
            break
        for job in positions:
            jobs.append({
                "title": job.get("positionName"),
                "company": job.get("companyFullName"),
                "salary": job.get("salary"),
                "location": job.get("city"),
                "description": job.get("positionDetail", ""),
                "industry": job.get("industryField", ""),
                "company_size": job.get("companySize", ""),
                "source": "lagou"
            })
        print(f"[拉勾] page {page} fetched {len(positions)} jobs")
        time.sleep(random.uniform(2, 3))
    return jobs

def scrape_liepin():
    """
    猎聘反爬较强，requests 版仅作参考。
    建议：Playwright 模拟浏览器，或使用手机端 API。
    """
    jobs = []
    # 猎聘搜索 URL 结构（简化，可能需根据实际页面调整）
    for page in range(1, MAX_PAGES + 1):
        url = f"https://www.liepin.com/zhaopin/?key={KEYWORD}&curPage={page}"
        try:
            resp = requests.get(url, headers=HEADERS_LIEPIN, timeout=15)
            # 猎聘返回 HTML，需用 BeautifulSoup 解析（此处略，建议使用 Playwright）
            print(f"[猎聘] page {page} HTML length {len(resp.text)}")
        except Exception as e:
            print(f"[猎聘] page {page} error: {e}")
            break
        time.sleep(random.uniform(2, 3))
    return jobs

def save_raw(jobs):
    import os
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_RAW, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"\n共抓取 {len(jobs)} 条原始 JD，保存至 {OUTPUT_RAW}")
    print("下一步：python .agents/skills/jd-scraper/scripts/normalize.py", OUTPUT_RAW, "jobs_normalized.json")

if __name__ == "__main__":
    all_jobs = []
    print("=== 开始抓取：大数据架构师 ===\n")

    # 1. BOSS直聘（数据最实时，推荐优先）
    if BOSS_COOKIE and "wt2" in BOSS_COOKIE:
        all_jobs.extend(scrape_boss())
    else:
        print("[跳过 BOSS] 未配置有效 Cookie。请登录 www.zhipin.com 后复制 Cookie 填入 BOSS_COOKIE。\n")

    # 2. 拉勾
    all_jobs.extend(scrape_lagou())

    # 3. 猎聘（反爬强，建议用 Playwright）
    print("[提示] 猎聘建议用 Playwright 抓取，当前 requests 版可能返回验证页。\n")

    save_raw(all_jobs)

"""
================ Playwright 备用方案（拉勾/猎聘）================

from playwright.sync_api import sync_playwright

def scrape_with_playwright(url_template, pages=3):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        for i in range(1, pages+1):
            page.goto(url_template.format(i))
            page.wait_for_timeout(3000)
            # 根据实际页面结构提取 .job-title, .company-name 等
            cards = page.query_selector_all(".job-list-item")
            for card in cards:
                title_el = card.query_selector(".job-name")
                title = title_el.inner_text() if title_el else ""
                jobs.append({"title": title, "source": "playwright"})
        browser.close()
    return jobs
"""
