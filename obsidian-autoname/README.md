# obsidian-autoname

Obsidian 插件：把粘贴 / 拖入笔记的附件**自动改名**为规范名（默认 `<笔记名>-图N.png`），并用 Obsidian 自己的 `fileManager.renameFile` **同步全库引用**，不留断链。

> 与「落位类插件」（如 Custom Attachment Location）分工：**它们管附件放哪个目录，本插件管附件叫什么**。两者可同时启用，互不干扰。

## 它做什么

1. 监听新建与改名事件：命中「待整理前缀 + 附件目录 + 指定扩展名」的文件，延迟片刻（等 Obsidian 把 `![[...]]` 引用插入编辑器）后改名。
2. 启用插件 / 打开库时补扫一次历史堆积。
3. 提供侧栏图标、两条命令与完整设置面板；命名模板、附件根目录、延迟等全部可配置，持久化到插件目录下的 `data.json`。

## 它不做什么

- 不接管粘贴、不改动落位插件的任何设置。
- 不做断链检查、散落附件归位（留给外部脚本兜底，避免两套逻辑互相覆盖）。
- 未被引用的孤儿附件**默认不命名**（无法确定出处，交人工判断；可在设置里关闭该限制）。
- 附件根目录下（未归入笔记子目录）的文件默认不处理，可在设置里开启。

## 目录约定

```
<库>/
└──根目录文件夹名/          # 附件根目录（可配置）
    └── 我的笔记/             # 子目录名 = 笔记名
        ├── 我的笔记-图1.png
        └── 我的笔记-图2.png
```

图号取「该目录既有最大号 + 1」，不做全量重编，因此与外部脚本（如 `check_attachments.py`）的编号口径一致，谁先跑结果都一样。

## 安装

### 方式一：手动安装（推荐先这样验证）

1. 到 Releases 下载 `main.js`、`manifest.json`、`styles.css` 三个文件（或用本仓库已构建好的根目录同名文件）。
2. 在库内创建 `<库>/.obsidian/plugins/obsidian-autoname/`。
3. 把三个文件放进该目录。
4. 重启 Obsidian → 设置 → 第三方插件 → 关闭「限制模式」→ 启用 **AutoName**。
5. 首次启用会自动生成 `data.json`（默认配置，可在设置面板调整）。

### 方式二：BRAT（从仓库直接装）

1. 安装 [BRAT](https://github.com/TfTHacker/obsidian42-brat) 插件并启用。
2. BRAT 设置 → Add Beta Plugin → 填 `SOLOMON-GHUB/obsidian-autoname`。
3. Add Plugin → 回到第三方插件列表启用 AutoName。

> BRAT 直接拉取仓库默认分支的文件，因此**仓库根目录必须提交 `main.js`**，否则 `npm run build` 后需手动提交一次（本仓库 `.gitignore` 按社区规范忽略了 `main.js`，若打算长期走 BRAT，请把它从 `.gitignore` 中移除并随代码提交）。

### 方式三：Obsidian 社区插件市场

本插件尚未提交官方市场。若要提交，需向 [obsidian-releases](https://github.com/obsidianmd/obsidian-releases) 提 PR，并在 README 中提供 `fundingUrl` 等信息（可选）。

## 设置项

| 设置 | 默认值 | 说明 |
| --- | --- | --- |
| 附件根目录 | `Attachments` | 库根相对路径，附件按 `<根>/<笔记名>/` 组织 |
| 待整理文件名前缀 | `Pasted image ` | 只有以此前缀开头的文件才会被改名 |
| 命名模板 | `{note}-图{n}` | `{note}` = 笔记名，`{n}` = 图号（最大号 + 1） |
| 处理的扩展名 | `png,jpg,jpeg,gif,webp,svg,bmp` | 小写逗号分隔；留空 = 不限制 |
| 改名延迟（毫秒） | `1500` | 等引用插入编辑器后再改名，过早会留下旧名引用 |
| 打开库时补扫历史堆积 | 开 | 启用 / 打开库时扫一次全库 |
| 只处理已被笔记引用的附件 | 开 | 孤儿附件保持原名交人工判断 |
| 也处理附件根目录下的文件 | 关 | 根目录无笔记名层，按引用它的笔记命名 |
| 显示提示 | 开 | 整理完成 / 失败时弹 Notice |

## 命令

- **AutoName：扫描全库并整理未命名附件** —— 立刻全库扫一遍。
- **AutoName：整理当前笔记的未命名附件** —— 只处理当前笔记对应的附件子目录。

侧栏图标（图片 + 加号）等价于第一条命令。

## 从源码构建

```bash
npm install          # 安装 esbuild / typescript / obsidian 类型
npm run dev          # watch 模式，输出可读的 main.js
npm run build        # 类型检查 + 压缩构建（发布用）
npm run build:readable   # 只构建一次，输出可读的 main.js（人工审阅用）
```

源码在 `src/`：

> 仓库根目录的 `main.js` 是**可读构建产物**（`npm run build:readable`），方便直接手动安装与逐行审核；
> 发布前请执行 `npm run build` 生成压缩版覆盖它。`.gitignore` 按社区规范忽略 `main.js`，
> 若打算长期用 BRAT 从仓库直接装，需把它纳入 git 提交。

| 文件 | 职责 |
| --- | --- |
| `src/main.ts` | 插件主体：事件注册、调度、改名、补扫、命令与侧栏图标 |
| `src/settings.ts` | 设置项类型、默认值、设置面板 UI |

## 发布新版本

```bash
npm version patch    # 或 minor / major；自动同步 manifest.json 与 versions.json
git push --follow-tags
```

推送 tag 后，`.github/workflows/release.yml` 会自动构建并把 `main.js`、`manifest.json`、`styles.css` 打包上传到 GitHub Release。

如果是手动发布：本地 `npm run build`，然后把这三个文件作为 Release 附件上传（**Release 的 tag 必须与 `manifest.json` 的 `version` 一致**，否则 BRAT / 市场无法识别更新）。

## 测试库验证清单

在一个**副本库**（不要拿正用着的库冒险）里按序验证：

1. 放好三个文件 → 重启 → 启用插件，确认设置面板能打开、默认值正确。
2. 新建笔记 `测试笔记.md`，粘贴一张图片：
   - 图片落在 `Attachments/测试笔记/`（这一步由落位插件负责）；
   - 约 1.5 秒后自动改名为 `测试笔记-图1.png`；
   - 笔记正文中的引用同步变为 `![[测试笔记-图1.png]]`，无旧名残留。
3. 再粘两张，确认编号为 `图2`、`图3` 且不撞号。
4. 手动把一个 `Pasted image xxx.png` 扔进 `99-Attachments/测试笔记/` 但**不引用**它 → 补扫后应保持原名（孤儿不命名）。
5. 命令面板执行「扫描全库并整理未命名附件」→ 提示整理数量，文件与引用均正确。
6. 关闭插件 → 确认不再触发改名；重新开启 → 补扫正常。
7. 打开开发者控制台（Ctrl+Shift+I），确认无报错，改名日志前缀为 `[obsidian-autoname]`。

## 从原插件改写清单

原始版本是单文件 `main.js`（插件 ID `vault1-attachment-autoname`，`require('obsidian')` 直接跑，无构建、无 UI、参数硬编码）。改写为 `obsidian-autoname` 的分步动作如下：

| 步骤 | 改哪个文件 | 改动目的 | 验证方式 |
| --- | --- | --- | --- |
| 1 | `manifest.json` | id/name 统一为 `obsidian-autoname`；补齐 `description`、`minAppVersion`；`isDesktopOnly` 改为 `false`（原为 `true`，但插件不用任何 Node/Electron API） | 放入 `.obsidian/plugins/obsidian-autoname/` 后插件能被识别并启用 |
| 2 | `package.json` | 新增依赖与 `dev/build/version` 脚本，使他人可复现构建 | `npm install && npm run build` 无报错 |
| 3 | `tsconfig.json` | 新增 TS 严格检查配置（`noImplicitAny`、`strictNullChecks`） | `npx tsc --noEmit` 无类型错误 |
| 4 | `esbuild.config.mjs` | 新增构建脚本：`obsidian`/`electron`/Node 内置模块标为 external，输出 CJS `main.js` | 构建产物顶部有 esbuild banner，且不含 `require("obsidian")` 的打包实现 |
| 5 | `src/main.ts` | 原 JS 重构为 TS：`export default class extends Plugin`；`require` 改为 `import`；补类型与空值判断 | 类型检查通过；插件加载无报错 |
| 6 | `src/main.ts` | 事件注册改用 `registerEvent`（原代码 `vault.on` 未注册，卸载后监听器残留）；定时器句柄存入 Map 并在 `onunload` 中 `clearTimeout`；`scheduleRename` 增加 `unloaded` 判断 | 关闭插件后不再触发改名；控制台无报错 |
| 7 | `src/main.ts` | `onLayoutReady` 回调加 `unloaded` 标志兜底（该回调无反注册接口） | 快速禁用后补扫不再执行 |
| 8 | `src/main.ts` | 硬编码 `99-Attachments`、`Pasted image `、`${note}-图${n}` 改为设置项（模板 `{note}-图{n}`） | 设置面板改成其他根目录/模板后行为随之变化 |
| 9 | `src/main.ts` | 新增扩展名白名单（原代码不判断扩展名，非图片文件也可能被改名） | 粘入 `Pasted image xxx.txt` 不会被处理 |
| 10 | `src/main.ts` | `file.parent` 空值判断；`normalizePath` 处理路径拼接 | 边界场景不抛异常 |
| 11 | `src/main.ts` | 引用检查由「每张图全库扫一遍」改为「批量一次全库扫描」，复杂度 O(N·M) → O(N+M) | 大量待整理图片时补扫明显变快 |
| 12 | `src/main.ts` | 新增命令 `扫描全库并整理未命名附件`、`整理当前笔记的未命名附件`；新增侧栏图标与自定义 SVG 图标（`addIcon` 注册，原插件无任何图标资源） | 命令面板可搜索到；侧栏出现图标且点击生效 |
| 13 | `src/settings.ts` | 新增设置面板与 `loadData/saveData` 持久化（原插件无 UI、无 `data.json`） | 改设置 → 重启 → 设置仍在；插件目录下生成 `data.json` |
| 14 | `styles.css` | 新增设置面板样式（原插件无样式资源） | 设置面板提示文字与命名预览排版正常 |
| 15 | `versions.json` | 新增版本 ↔ 最低 App 版本映射，供市场/BRAT 判断兼容性 | 文件存在且键与 `manifest.json` 的 version 一致 |
| 16 | `README.md` / `LICENSE` / `.gitignore` / `.github/workflows/release.yml` | 补齐社区插件规范要求的文档、许可、忽略规则与发布流水线 | 打 tag 后 Release 自动产出三个文件 |
| 17 | `main.js`（根目录） | 由 `npm run build:readable` 产出的可分发构建物 | 与 `manifest.json`、`styles.css` 一起拷进测试库即可运行 |

源码中所有被改写或新增的关键位置都带 `// [改写]` 注释，说明相对原始代码的改动原因，可与原 `main.js` 逐段对照。

## 许可

MIT，见 [LICENSE](LICENSE)。
