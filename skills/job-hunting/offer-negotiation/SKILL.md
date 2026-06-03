---
name: offer-negotiation
description: 当用户拿到多个offer需要比较、或需要就单个offer进行薪资谈判时触发。提供总薪酬对比分析、加权决策矩阵、谈判策略与Counter脚本。
---

# Offer Negotiation

## When to Use This Skill

Use this skill when the user:
- Has multiple job offers to compare
- Needs to evaluate total compensation
- Wants to negotiate a job offer or salary
- Research market rates for their role
- Create a counter-offer strategy
- Mentions: "compare offers", "multiple offers", "which job", "offer comparison", "salary negotiation", "negotiate offer", "counter offer", "compensation"

## Core Capabilities

- Compare total compensation across offers
- Build negotiation strategy and scripts
- Create weighted decision frameworks
- Calculate true offer value
- Prepare counter-offer responses
- Identify negotiation leverage points
- Evaluate non-monetary factors
- Navigate difficult salary conversations

---

# Part 1: Offer Comparison

## Total Compensation Calculator

### Components to Include

**Cash Compensation:**
- Base salary
- Signing bonus (one-time)
- Annual bonus (target %)
- Commission (for sales roles)
- Relocation assistance

**Equity Compensation:**
- Stock options (value = current price - strike price)
- RSUs (value = current price × shares)
- Vesting schedule
- Refresh grant expectations

**Benefits Value:**
- Health insurance (employer contribution)
- 401(k) match
- HSA/FSA contributions
- Life/disability insurance

**Perks Value:**
- Vacation days (can assign $ value)
- Remote work (saves commute costs)
- Professional development budget
- Equipment/office stipend

### Calculation Template

```
OFFER A - TOTAL COMPENSATION

CASH
Base Salary:                    $150,000
Signing Bonus (year 1 only):     $25,000
Target Bonus (15%):              $22,500
--------------------------------
Cash Compensation:              $197,500 (year 1)
                               $172,500 (ongoing)

EQUITY
RSU Grant: $200,000 over 4 years
Annual Value:                    $50,000
--------------------------------
Equity Compensation:             $50,000/year

BENEFITS
401(k) Match (4%):               $6,000
Health Insurance:                $15,000 (employer portion)
HSA Contribution:                 $1,000
--------------------------------
Benefits Value:                  $22,000/year

PERKS
Vacation: 20 days (vs 10 standard)
  Extra 10 days × ~$575/day:      $5,750 value
Remote Work Savings:              $3,000 (commute, lunch)
Professional Dev:                 $2,000 budget
--------------------------------
Perks Value:                     $10,750/year

TOTAL YEAR 1:        $280,250
TOTAL ONGOING:       $255,250/year
```

## Side-by-Side Comparison Template

```markdown
# OFFER COMPARISON

|                          | Company A | Company B | Notes |
|--------------------------|-----------|-----------|-------|
| **CASH**                 |           |           |       |
| Base Salary              | $150,000  | $160,000  | B +$10K |
| Signing Bonus            | $25,000   | $10,000   | A +$15K |
| Target Bonus             | 15%       | 10%       | A +$6.5K |
| **Cash Total (Yr 1)**    | $197,500  | $186,000  | A +$11.5K |
|                          |           |           |       |
| **EQUITY**               |           |           |       |
| Grant Value (4yr)        | $200,000  | $300,000  | B +$100K |
| Annual Equity            | $50,000   | $75,000   | B +$25K |
|                          |           |           |       |
| **BENEFITS**             |           |           |       |
| 401(k) Match             | 4%        | 6%        | B +$3.2K |
| Health Insurance         | Good      | Premium   | B better |
| PTO                      | 20 days   | Unlimited | Varies |
|                          |           |           |       |
| **TOTAL COMP (Yr 1)**    | $280,250  | $285,000  | B +$4.7K |
| **TOTAL COMP (Ongoing)** | $255,250  | $275,000  | B +$19.7K |
```

## Non-Monetary Factor Framework

### Career Growth (Weight: High)

**Questions to Consider:**
- Which role offers more learning?
- Which company/brand helps future job search?
- Which has better promotion track?
- Which offers more scope/responsibility?
- Which manager will develop you more?

**Scoring:** Rate each factor 1-10 per company, then average.

### Work-Life Balance (Weight: Personal)

Factors: Expected hours, remote flexibility, vacation culture, on-call, commute.

### Team & Culture (Weight: High)

Factors: Manager quality (crucial), team dynamics, culture fit, company stability, values alignment.

### Risk Assessment (Weight: Medium)

**Startup vs. Established:** Funding runway, market position, trajectory, equity risk (could be worth $0).

## Weighted Decision Matrix

### Step 1: Define Your Priorities

```
Factor                  Weight
------------------------------------
Total Compensation       25%
Career Growth            25%
Work-Life Balance        20%
Team & Culture           20%
Location/Commute         10%
------------------------------------
Total:                   100%
```

### Step 2: Score Each Factor

```
                    Company A   Company B
Factor              Score (1-10)
------------------------------------
Compensation        7           8
Career Growth       7           8
Work-Life           8           6
Team & Culture      9           7
Location            8           5
```

### Step 3: Calculate Weighted Score

```
Company A:
(7 × 0.25) + (7 × 0.25) + (8 × 0.20) + (9 × 0.20) + (8 × 0.10)
= 1.75 + 1.75 + 1.60 + 1.80 + 0.80
= 7.70

Company B:
(8 × 0.25) + (8 × 0.25) + (6 × 0.20) + (7 × 0.20) + (5 × 0.10)
= 2.00 + 2.00 + 1.20 + 1.40 + 0.50
= 7.10

Result: Company A scores higher (7.70 vs 7.10)
```

---

# Part 2: Salary Negotiation

## The Negotiation Mindset

**Key Principles:**
1. Negotiation is expected - companies budget for it
2. 84% of employers expect candidates to negotiate
3. Not negotiating leaves $500K-$1M on the table over a career
4. The goal is win-win, not adversarial

**What You're Really Negotiating:**
- Base salary
- Signing bonus
- Annual bonus/commission
- Equity (stock options, RSUs)
- Benefits (401k match, insurance)
- Perks (vacation, remote work, professional development)
- Start date, Title

## Research Phase

### Step 1: Determine Market Rate

**Sources to Check:**
- Levels.fyi (best for tech)
- Glassdoor (general, take with grain of salt)
- LinkedIn Salary
- Blind (anonymous reports)
- PayScale, Salary.com
- H1B salary data (publicly available)

**Build a Range:**
```
Low (25th percentile): $XXX,XXX
Target (50th percentile): $XXX,XXX
High (75th percentile): $XXX,XXX
Stretch (90th percentile): $XXX,XXX
```

### Step 2: Know Your Value

**Factors That Increase Your Worth:**
- Years of relevant experience
- Specialized/rare skills
- Track record of results
- In-demand certifications
- Current competing offers
- Referral from employee
- Market demand in your field

**Factors That May Limit:**
- Entry level or career change
- Less experience than ideal candidate
- Gaps in required skills
- Location arbitrage (lower cost of living)

## Negotiation Strategy

### When to Negotiate

**Best Time:** After you have a written offer, before you sign

**Timeline:**
1. Receive verbal offer → Express enthusiasm, ask for written offer
2. Receive written offer → Thank them, ask for time to review
3. Research and prepare → 24-48 hours
4. Counter with ask → Email or call
5. Discussion/back and forth → May take several rounds
6. Final agreement → Get in writing

### The Counter-Offer Framework

**Structure:**
1. Express enthusiasm
2. Reinforce your value
3. Make specific ask
4. Provide justification
5. Open discussion

### Counter-Offer Email Template

```
Subject: [Your Name] - Offer Discussion

Hi [Recruiter/Hiring Manager],

Thank you so much for the offer to join [Company] as [Title]. I'm very excited about the opportunity to [specific thing about the role]. After speaking with the team and learning more about [something specific], I'm confident this is the right fit.

I've had time to review the offer details and wanted to discuss the compensation. Based on my research of the market and my [X years of experience / specific valuable skill / competing offer], I was hoping we could discuss a base salary of $[Your Ask] rather than $[Their Offer].

[Optional: Add specific justification]

I'm flexible and open to discussing other elements of the package as well. Would you have time for a quick call to discuss?

Thank you again for this opportunity. I'm looking forward to finding a package that works for both of us.

Best,
[Your Name]
```

### Counter-Offer Call Script

**Opening:** "Hi [Name], I'm really excited about this opportunity. Based on my market research, I was hoping for a base closer to $[Amount]. Is there flexibility?"

**If pushback:** "I understand. Could we look at signing bonus, equity, or other elements to bridge the gap?"

**If need to check:** "That's fair. When should we reconnect?"

## Common Negotiation Scenarios

### Scenario 1: First Offer Is Low

**Script:**
```
"I'm thrilled about the opportunity. The base salary is lower than I expected based on my research. For this role and market, I was expecting something in the $X-$Y range. Is there room to move closer to $X?"
```

### Scenario 3: They Won't Budge on Base

**Alternatives to Negotiate:**
- Signing bonus (one-time, easier to approve)
- Additional equity
- Earlier performance review (sooner raise)
- More vacation days
- Remote work flexibility
- Professional development budget
- Title upgrade
- Relocation assistance

**Script:**
```
"I understand the base salary is firm. Could we discuss a signing bonus to help bridge the gap? Something in the range of $X would make this work."
```

### Scenario 4: You Have Competing Offers

**Use Carefully:**
- Only mention if true
- Don't make it a threat
- Frame as problem-solving

**Script:**
```
"I want to be transparent - I'm also in discussions with [another company/a few other companies]. They're offering $X. [Your Company] is my first choice because [genuine reason], but I want to make sure the compensation is competitive."
```

## Negotiation Tactics

### Do's:
- ✅ Always negotiate (respectfully)
- ✅ Get the offer in writing before negotiating
- ✅ Research thoroughly
- ✅ Be specific with numbers
- ✅ Express genuine enthusiasm
- ✅ Give them a way to say yes
- ✅ Consider total compensation
- ✅ Get final agreement in writing

### Don'ts:
- ❌ Accept on the spot
- ❌ Give a salary history (if not required by law)
- ❌ Make ultimatums
- ❌ Lie about competing offers
- ❌ Be rude or aggressive
- ❌ Accept verbal promises without writing

## Negotiation Timeline

| Phase | Timing | Actions |
|-------|--------|---------|
| Receive | Day 1 | Thank them, ask for written offer and deadline |
| Research | Day 1-3 | Verify market rate, calculate total comp, prepare counter |
| Counter | Day 3-5 | Send email or schedule call with specific ask |
| Discuss | Day 5-10 | Be patient but responsive through rounds |
| Resolve | Day 10+ | Agree on terms, get in writing, sign |

---

## Output Format

### For Offer Comparison

```markdown
# JOB OFFER COMPARISON

## Offers Being Compared
- **Offer A:** [Role] at [Company]
- **Offer B:** [Role] at [Company]

## Total Compensation Comparison

| Component | Offer A | Offer B | Difference |
|-----------|---------|---------|------------|
| Base | $X | $X | |
| Bonus | $X | $X | |
| Equity (annual) | $X | $X | |
| Benefits | $X | $X | |
| **Year 1 Total** | $X | $X | |
| **Ongoing Total** | $X | $X | |

## Non-Monetary Comparison

| Factor | Offer A | Offer B | Notes |
|--------|---------|---------|-------|
| Career Growth | X/10 | X/10 | |
| Work-Life | X/10 | X/10 | |
| Team/Culture | X/10 | X/10 | |
| Risk Level | X/10 | X/10 | |

## Weighted Analysis
- Offer A Score: X.XX
- Offer B Score: X.XX

## Recommendation
Based on your stated priorities of [X, Y, Z], **Offer [A/B]** appears to be the stronger choice because:
- [Reason 1]
- [Reason 2]

## Negotiation Opportunities
- [Opportunity 1]
- [Opportunity 2]
```

### For Salary Negotiation

```markdown
# SALARY NEGOTIATION STRATEGY

**Market Range:** 25th: $XXX | 50th (target): $XXX | 75th: $XXX | 90th (stretch): $XXX

## Their Offer
| Component | Amount |
|-----------|--------|
| Base | $XXX,XXX |
| Bonus | X% |
| Equity | $XXX,XXX |
| Signing | $XXX |
| Total Year 1 | $XXX,XXX |

## Your Counter
| Component | Ask | Justification |
|-----------|-----|---------------|
| Base | $XXX,XXX | [Why] |
| Signing | $XXX | [Why] |

## Script & Fallback
**Counter Script:** [Customized email or call script]
**Plan B:** [Alternative elements]
**Walk-away Point:** [Your minimum]
```

## Checklist

**Comparison:**
- ✅ Total comp (not just base), equity, benefits, non-monetary factors
- ✅ Career growth, team/manager quality, company risk

**Negotiation:**
- ✅ Market research from 3+ sources, walk-away point defined
- ✅ Counter-offer prepared with justification, pushback scenarios planned
- ✅ Final agreement in writing

## Gotchas

- ** verbal promises ≠ written offer**：任何口头承诺（如"我们明年会给你涨薪"）如果没有写进 offer letter，都不具备约束力。务必要求书面确认。
- **Equity 的税务陷阱**：RSU 在归属时按普通收入征税，行权时可能触发 AMT（替代性最低税）。Options 的行权成本容易被忽略，需提前准备现金。不同国家/地区的股权税务处理差异巨大，建议咨询税务顾问。
- **Non-compete 和 IP 条款**：签字前仔细阅读竞业限制和知识产权归属条款。某些州的 non-compete 可能不具法律效力，但签字后产生纠纷依然耗时耗力。如有疑虑，请律师审阅。
- **Vesting Cliff 的隐形损失**：如果 offer 要求 1 年 cliff，意味着入职 11 个月离职将拿不到任何股权。接受 offer 前应将这一风险纳入总薪酬评估。
- **"Up to"  bonus 的水分**："up to 20%" 不等于 "20%"。应追问实际发放的中位数和历史发放率，避免用理论最大值做决策。
- **Location arbitrage 的双刃剑**：远程或低生活成本地区的 offer 可能总包较低，但需综合考虑税收、通勤成本、职业网络密度。未来若 relocated，薪资可能不会被调整到当地水平。
- **Counter-offer 的时机窗口**：最佳谈判窗口是拿到书面 offer 后、签字前。一旦签字后再提出异议，会严重损害信任。若公司催促在 24 小时内答复，可礼貌请求延期。
- **使用竞争 offer 的风险**：提及竞争 offer 必须基于事实。一旦被要求提供书面 proof 而无法提供，将直接摧毁 credibility。更安全的做法是引用市场数据而非竞争 offer。
- **Title 的长期影响**：较低的 title 可能影响未来跳槽时的职级对标。如果 base 无法提升，争取更高 title 有时比现金更有长期价值。
- **福利的退出成本**：某些高额福利（如高端医疗保险、子女教育补贴）在换工作时将消失，实际现金等价价值可能被低估。评估时应考虑这些福利的替代成本。