---
name: project-collaboration-setup
description: 从 GitHub 为新项目或已有项目搭建语境切换、共识库与学习地图机制，自动获取两个核心 Skill 并保留已有内容。用户请求初始化或接入时使用，普通项目任务不触发。
---

# 项目协作机制初始化

用户只需提供本 Skill 或仓库链接，并要求“为当前项目初始化协作机制”。无需预装另外两个 Skill，也无需当前作者的路径或上下文。

源仓库：https://github.com/throusea/project-collaboration-skill

1. 确定目标项目，读取已有 AGENTS.md/AGENT.md，查找共识库及学习记录路径。已有自定义位置继续使用，不复制示例中的知识状态。不明确目标时才询问。
2. 用 Git 在临时目录克隆上述仓库；记录 `git rev-parse HEAD` 的完整提交号。读取该提交的 `scripts/setup.py`、模板及两个核心 Skill 后执行，整个安装只用这一份快照。缺 Git 时可通过 GitHub API 将 main 解析为完整 SHA，再下载该 SHA 的文件；不安装依赖工具或绕开网络限制。无法访问时报告具体缺口，不声称初始化完成。
3. 使用 Python 3 标准库运行 `python scripts/setup.py --project <项目绝对路径>`。自定义路径用 `--consensus <项目内相对路径> --learning <项目内相对目录>`。该脚本将两 Skill 放到项目 `.agents/skills/`，创建空共识库并补入口，学习主题文件按需创建。缺 Python 时按同样模板与保留规则手动安装，记录提交号；不依赖全局 Skill 路径。
4. 已有 AGENTS 时先判断重复、矛盾及原入口路径：若已有等价机制，手动补缺项，不盲追加。脚本遇到不同版本的同名 Skill、不同配置的已管理入口或 AGENT.md 单入口会停止，不覆盖。核对差异后在当前授权范围合并，实质改变已有规则含义时向用户说明具体选择。安装不是升级授权，不强行覆盖用户定制。
5. 核对入口与文件可读，记录来源提交及新增/保留的路径。已有文件不被覆盖、重复运行无变化才算文件验收通过；真实对话效果另行验证。简述如何使用：以后直接讨论、安排任务或开始学习，入口会路由到对应 Skill；若客户端尚未刷新 Skill 列表，新会话读取项目 AGENTS 即可找到文件。

模板在 templates/；examples/ 仅供理解写法，不安装。共识由 shared-understanding 维护，教学由 adaptive-teaching 负责；新项目默认没有任何已确认知识。初始化请求授权建立这些入口，不授权执行示例工程或迁移其他项目记录。
