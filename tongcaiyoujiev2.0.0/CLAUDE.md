# CLAUDE - Development Guide

## 开发规范

- 遵循 OpenClaw AgentSkill 标准结构
- 每个技能独立放在 `skills/` 目录下
- 每个技能必须包含：`SKILL.md`、`LICENSE.txt`、测试用例 `test-cases.md`、测试报告 `test-report.md`
- 参考文档放在 `references/` 目录下

## 代码风格

- Markdown 文件使用 UTF-8 编码
- 中文使用简体中文，标点符号遵循中文规范
- 标题层级清晰，一级标题用于文件名，二级用于主要章节

## 发布流程

1. 确保所有测试用例通过
2. 更新版本号
3. 提交 PR 到仓库
4. 等待内部审核
5. 审核通过后发布到 ClawHub

## 质量要求

- 无敏感信息泄露
- 文档清晰易懂
- 测试覆盖率 100%
- 结构符合规范
