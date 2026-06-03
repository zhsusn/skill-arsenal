#!/usr/bin/env python3
"""
JD Normalizer: Clean and standardize scraped job data.
Usage: python normalize.py input.json output.json
"""

import json, sys, re, hashlib
from datetime import datetime

TECH_KEYWORDS = [
    "Python", "Java", "Go", "Rust", "C++", "JavaScript", "TypeScript",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
    "Spark", "Hadoop", "Kafka", "Flink", "Airflow", "dbt",
    "TensorFlow", "PyTorch", "scikit-learn", "Pandas", "NumPy",
    "React", "Vue", "Angular", "Node.js", "Django", "Flask", "FastAPI",
    "Git", "Jenkins", "GitHub Actions", "GitLab CI", "CircleCI",
    "Linux", "Nginx", "Kafka", "RabbitMQ", "gRPC", "REST", "GraphQL"
]

def clean_html(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills(text):
    found = []
    upper_text = text.upper()
    for kw in TECH_KEYWORDS:
        if re.search(r'\b' + re.escape(kw.upper()) + r'\b', upper_text):
            found.append(kw)
    return found

def dedupe_jobs(jobs):
    seen = set()
    unique = []
    for job in jobs:
        key = hashlib.sha256(
            f"{job.get('company','')}|{job.get('title','')}|{job.get('location','')}".encode()
        ).hexdigest()
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

def normalize(job):
    return {
        "id": hashlib.sha256(
            f"{job.get('company','')}|{job.get('title','')}|{job.get('location','')}".encode()
        ).hexdigest()[:16],
        "source": job.get("source", "unknown"),
        "title": clean_html(job.get("title", "")),
        "company": clean_html(job.get("company", "")),
        "location": clean_html(job.get("location", "")),
        "salary_range": job.get("salary", job.get("salaryDesc", "")),
        "employment_type": job.get("employment_type", "Full-time"),
        "remote_policy": job.get("remote_policy", "Unknown"),
        "posting_date": job.get("posting_date", ""),
        "description_raw": clean_html(job.get("description", job.get("job_desc", ""))),
        "requirements": [],
        "responsibilities": [],
        "skills_extracted": extract_skills(job.get("description", "")),
        "apply_url": job.get("apply_url", job.get("link", "")),
        "company_size": job.get("company_size", job.get("brandScaleName", "")),
        "industry": job.get("industry", job.get("brandIndustry", "")),
        "scraped_at": datetime.utcnow().isoformat() + "Z"
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python normalize.py input.json output.json")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        raw = json.load(f)
    jobs = [normalize(j) for j in raw]
    jobs = dedupe_jobs(jobs)
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"Normalized {len(jobs)} unique jobs from {len(raw)} raw records.")

if __name__ == "__main__":
    main()
