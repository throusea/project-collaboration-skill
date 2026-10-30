# Project Collaboration Skill

每个项目是一个小的共识区：按语境切换执行、讨论与教学，积累精简的共同理解，用逐步点亮的学习地图记录进展。

## 直接使用

在目标项目中把下面这句话交给支持读取仓库和文件操作的助手：

> 请读取 https://github.com/throusea/project-collaboration-skill/blob/main/skills/project-collaboration-setup/SKILL.md ，按这个 Skill 为当前项目初始化协作机制。

只需要这个初始化入口。助手负责获取两项核心 Skill、空共识模板并接入 AGENTS.md，不要求你手工下载文件。客户端会按自身权限要求确认文件或网络操作。

如果使用 Codex 的 skill-installer，也可安装本仓库 `skills/project-collaboration-setup`，然后说“为当前项目初始化协作机制”。

## 内容

- `skills/shared-understanding`：共同术语、理解反馈与精简共识维护；保留原始 Skill。
- `skills/adaptive-teaching`：知识地图、实践反馈与学习节奏；保留原始 Skill。
- `skills/project-collaboration-setup`：无需预装依赖的初始化入口。
- `templates`：可迁移的项目入口、空共识库、学习地图结构。
- `examples`：压缩后的 UE 记录示例，仅参考，不安装。

初始化产物：项目 `.agents/skills/` 下两个核心 Skill、AGENTS.md 协作入口、`docs/CollaborationConsensus.md`。学习记录在首次持续学习时创建于 `docs/learning/`；原始模板不自动建立课程。

已有文件保留。重复运行不重复追加；同名 Skill 内容不同则停止等待合并。下载以一次解析到的提交为准，`.collaboration-kit-source.json` 记录来源，不自动追随远端升级。模板中的约定可以按项目需要调整。

## 手动运行与验证

需要 Git 和 Python 3：

```sh
git clone https://github.com/throusea/project-collaboration-skill.git
python project-collaboration-skill/scripts/setup.py --project /absolute/path/to/project
python -m unittest discover -s project-collaboration-skill/tests
```

自定义库路径使用 `--consensus notes/consensus.md --learning notes/learning`，路径均相对于目标项目。

这套模板来源于实际的共识协作和 UE 学习实践；公开内容不包含原项目的研究记录或个人绝对路径。
