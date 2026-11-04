# Project Collaboration Skill

每个项目是一个小的共识区：按语境切换合作推进、平等讨论与教学，积累精简的共同理解，用逐步点亮的学习地图记录进展。

## 直接使用

在目标项目中把下面这句话交给支持读取仓库和文件操作的助手：

> 请读取 https://github.com/throusea/project-collaboration-skill/blob/main/skills/project-collaboration-setup/SKILL.md ，按这个 Skill 为当前项目初始化协作机制。

只需要这个初始化入口。助手负责获取两项核心 Skill、语境识别文档、空共识模板并接入 AGENTS.md，不要求你手工下载文件。客户端会按自身权限要求确认文件或网络操作。

如果使用 Codex 的 skill-installer，也可安装本仓库 `skills/project-collaboration-setup`，然后说“为当前项目初始化协作机制”。

## 内容

- `skills/shared-understanding`：共同术语、理解反馈、根据目标判断分工与精简共识维护。
- `skills/adaptive-teaching`：围绕必要能力安排实践，维护知识地图、实践反馈与学习节奏。
- `skills/project-collaboration-setup`：无需预装依赖的初始化入口。
- `templates`：可迁移的项目入口、语境与语义识别、空共识库、学习地图结构。
- `examples`：压缩后的 UE 记录示例，仅参考，不安装。

初始化产物：项目 `.agents/skills/` 下两个核心 Skill、AGENTS.md 协作入口、`docs/CollaborationConsensus.md` 和 `docs/ContextAndIntent.md`。学习记录在首次持续学习时创建于 `docs/learning/`；原始模板不自动建立课程。

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

## 语境与语义识别

每轮区分合作推进、平等讨论与教学，再判断询问、异议、理解反馈或授权。纠正先讨论，不自动认同；询问不自动切换教学。共识更新保留必要的助手理解修正，核对不强制新增条目。详细流程随初始化安装到 `docs/ContextAndIntent.md`。

已有安装不会自动升级或覆盖定制文件；更新时对照新模板手动合并。安装测试验证文件保护与重复运行，不能代替真实对话效果测试。

合作分工依据当前目标、角色、能力与资源：值得亲自实践的部分由用户练习，只需了解的部分提供必要解释并由助手完成或复用，已有共识直接沿用。用户保有方向与决定权；助手主动提出判断、执行和核查，不逐项把分工问题交回用户，也不把交付任务自动变成课程。
