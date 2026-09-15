#!/usr/bin/env python3
"""人力编制申请合规测算（通用模板）。

所有阈值均可通过命令行参数覆盖；默认值仅作示例，不代表任何组织的实际口径。
仅依赖 Python 3 标准库。
"""
import argparse


def compute(revenue, headcount, margin, min_rph, min_margin, cap_ratio,
            bonus_margin, bonus_ratio):
    steps = []
    ok = True

    rph = revenue / headcount if headcount else 0.0
    if rph < min_rph:
        ok = False
        steps.append('人均产值 %.2f 万元/人 < 门槛 %g 万元/人 → 不通过' % (rph, min_rph))
    else:
        steps.append('人均产值 %.2f 万元/人 ≥ 门槛 %g 万元/人 → 通过' % (rph, min_rph))

    if margin < min_margin:
        ok = False
        steps.append('毛利率 %.1f%% < 下限 %.1f%% → 不通过' % (margin*100, min_margin*100))
    else:
        steps.append('毛利率 %.1f%% ≥ 下限 %.1f%% → 通过' % (margin*100, min_margin*100))

    cap = revenue * cap_ratio
    per_head = cap / headcount if headcount else 0.0
    steps.append('总薪资上限 = %g × %.0f%% = %.2f 万元；人均上限 = %.2f 万元/人/年'
                 % (revenue, cap_ratio*100, cap, per_head))

    bonus = None
    if margin > bonus_margin:
        bonus = revenue * margin * bonus_ratio
        steps.append('毛利率 %.1f%% > %.0f%%，超额奖金 = %g × %.1f%% × %.0f%% = %.2f 万元（单独计发）'
                     % (margin*100, bonus_margin*100, revenue, margin*100, bonus_ratio*100, bonus))

    return ok, steps, cap, per_head, bonus


def main():
    p = argparse.ArgumentParser(description='人力编制审批测算（通用模板）')
    p.add_argument('--revenue', type=float, required=True, help='全年营业额（万元）')
    p.add_argument('--headcount', type=int, required=True, help='申请人数')
    p.add_argument('--margin', type=float, required=True, help='目标毛利率，如 0.30')
    p.add_argument('--min-revenue-per-head', type=float, default=50.0,
                   help='人均产值门槛（万元/人/年，示例默认 50）')
    p.add_argument('--min-margin', type=float, default=0.25,
                   help='最低毛利率（示例默认 0.25）')
    p.add_argument('--payroll-cap-ratio', type=float, default=0.25,
                   help='薪资上限占营业额比例（示例默认 0.25）')
    p.add_argument('--bonus-margin', type=float, default=0.50,
                   help='超额奖金触发毛利率（示例默认 0.50）')
    p.add_argument('--bonus-ratio', type=float, default=0.10,
                   help='超额奖金计提比例（示例默认 0.10）')
    a = p.parse_args()

    ok, steps, cap, per_head, bonus = compute(
        a.revenue, a.headcount, a.margin, a.min_revenue_per_head,
        a.min_margin, a.payroll_cap_ratio, a.bonus_margin, a.bonus_ratio)

    for s in steps:
        print('- ' + s)
    print('结论：' + ('通过' if ok else '不通过'))
    print('合规薪资上限：%.2f 万元/年' % cap)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

