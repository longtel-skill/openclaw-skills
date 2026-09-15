#!/usr/bin/env python3
"""
发票税务核查说明文档自动生成脚本
参数:
    --company: 企业名称
    --credit-code: 统一社会信用代码
    --address: 注册地址
    --business: 主要经营范围/业务
    --year: 核查年度
    --invoice-count: 发票份数
    --invoice-amount: 发票金额合计
    --invoice-tax: 税额合计
    --conclusion: 核查结论文本
    --tax-office: 税务局名称（默认：贵局）
    --output: 输出文件名（不含扩展名）
    --date: 回复日期（默认：今日）
"""

import argparse
import datetime
import subprocess
import os

template = """# 关于{year}年度{company}发票核查情况的说明

{tax_label}：

根据贵局核查要求，我司对{year}年度涉及核查的发票进行了全面核查，现将核查情况说明如下：

## 一、企业基本情况
**企业名称：** {company}  
**统一社会信用代码：** {credit_code}  
**注册地址：** {address}  
**主要经营业务：** {business}

## 二、发票核查基本信息
本次核查共涉及发票 **{invoice_count}** 份：
- 金额合计：**{invoice_amount:.2f}** 元
- 税额合计：**{invoice_tax:.2f}** 元
- 价税合计：**{total_amount:.2f}** 元

## 三、核查结论

{conclusion}

## 四、其他说明

如有未尽事宜，请随时与我司联系。

特此说明。

---

{company}（盖章）  
{date}
"""

def main():
    parser = argparse.ArgumentParser(description='生成发票税务核查说明Word文档')
    parser.add_argument('--company', required=True, help='企业名称')
    parser.add_argument('--credit-code', required=True, help='统一社会信用代码')
    parser.add_argument('--address', required=True, help='注册地址')
    parser.add_argument('--business', required=True, help='主要经营业务')
    parser.add_argument('--year', required=True, help='核查年度')
    parser.add_argument('--invoice-count', type=int, required=True, help='发票份数')
    parser.add_argument('--invoice-amount', type=float, required=True, help='金额合计')
    parser.add_argument('--invoice-tax', type=float, required=True, help='税额合计')
    parser.add_argument('--conclusion', required=True, help='核查结论（详细文本）')
    parser.add_argument('--tax-office', default='贵局', help='税务局名称（默认：贵局）')
    parser.add_argument('--output', default='发票核查情况说明', help='输出文件名（不含扩展名）')
    parser.add_argument('--date', help='回复日期（YYYY-MM-DD，默认今日）')
    
    args = parser.parse_args()
    
    # 处理日期
    if args.date:
        doc_date = args.date
    else:
        doc_date = datetime.date.today().strftime('%Y年%m月%d日')
    
    # 处理税务局标签
    if args.tax_office == '贵局':
        tax_label = args.tax_office
    else:
        tax_label = f'{args.tax_office}'
    
    # 计算价税合计
    total_amount = args.invoice_amount + args.invoice_tax
    
    # 格式化文档
    content = template.format(
        company=args.company,
        credit_code=args.credit_code,
        address=args.address,
        business=args.business,
        year=args.year,
        invoice_count=args.invoice_count,
        invoice_amount=args.invoice_amount,
        invoice_tax=args.invoice_tax,
        total_amount=total_amount,
        conclusion=args.conclusion,
        tax_label=tax_label,
        date=doc_date
    )
    
    # 保存Markdown
    md_file = f'{args.output}.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✓ Markdown文档已保存: {md_file}')
    
    # 转换为Word
    docx_file = f'{args.output}.docx'
    cmd = ['pandoc', '-s', md_file, '-o', docx_file]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f'✓ Word文档已生成: {docx_file}')
        return 0
    except subprocess.CalledProcessError as e:
        print(f'✗ 转换Word失败: {e.stderr}')
        return 1
    except FileNotFoundError:
        print(f'✗ 未找到pandoc，请先安装pandoc')
        print(f'  Markdown文件已保留: {md_file}')
        return 2

if __name__ == '__main__':
    exit(main())
