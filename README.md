# VuePress 迁移到 Docusaurus 指南

本指南重点介绍如何将文档结构从 VuePress 迁移到 Docusaurus。

## 文件命名和索引

### 文件名
避免使用 `0.1/0.2` 这种数字前缀作为文件名。请使用以下规则：
- 使用文档的一级标题 `#` 作为文件名
- 采用驼峰命名法（第一个单词首字母小写，后续单词首字母大写）
- 文件名中不使用空格

示例：`gettingStarted.md` 而不是 `0.1 Getting Started.md`

### 侧边栏索引
使用 front matter 控制侧边栏中的位置。要将页面放在侧边栏的第一位：

```yaml
---
sidebar_position: 1
---
```

更多 front matter 选项，请参考 [Docusaurus 文档](https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-docs#markdown-front-matter)。

## 提示框（Admonitions）

将 VuePress 的自定义容器转换为 Docusaurus 的提示框：

VuePress:
```markdown
> #### hint::信息框说明
> 这是一个提示。
> > #### flag::进度提示
>
> > #### comment::扩展阅读
```

Docusaurus:
```markdown
:::info[信息框说明]
这是一个提示。
:::

:::tip[进度提示]
:::

:::info[扩展阅读]
:::
```

Docusaurus 提供五种内置的提示框类型。使用这些内置类型可以更好地兼容未来的迁移。更多自定义选项，请参阅 [提示框文档](https://docusaurus.io/docs/markdown-features/admonitions)。

## 链接

使用相对链接引用所有本地文件，以确保多语言支持的正确性：

```markdown
[链接到另一页](./anotherPage.md)
```

## 文本高亮

将内联 HTML 替换为 Docusaurus 的 `<Highlight>` 组件：

VuePress:
```html
<font color=red>重要文本</font>
```

Docusaurus:
```jsx
<Highlight color="#c40e0e">重要文本</Highlight>
```

指定颜色时使用十六进制 RGB 值。`<Highlight>` 组件定义如下：

```jsx
import React from 'react';

export default function Highlight({children, color}) {
  return (
    <span
      style={{
        backgroundColor: color,
        borderRadius: '2px',
        color: '#fff',
        padding: '0.2rem',
      }}>
      {children}
    </span>
  );
}
```

按照这些指南操作，您可以确保从 VuePress 到 Docusaurus 的平滑过渡，同时保持一致的格式，并利用 Docusaurus 的特定功能。

## 如何贡献到此仓库

### 仓库地址

[ysyx-docs-content](https://github.com/oscc-web/ysyx-docs-content)

### 分叉仓库

1. 进入仓库主页。
2. 点击右上角的“Fork”按钮。
3. 选择您的账户作为分叉的目标。

### 设置本地环境

1. 克隆您分叉的仓库：
   ```bash
   git clone https://github.com/your-username/ysyx-docs-content.git
   cd ysyx-docs-content
   ```

2. 添加原始仓库为远程仓库，以便保持同步：
   ```bash
   git remote add upstream https://github.com/oscc-web/ysyx-docs-content.git
   ```

### 创建开发分支

1. 创建并切换到一个新的分支，用于您的功能或修复：
   ```bash
   git checkout -b dev-your-feature-name
   ```

### 开发更改

1. 在 `dev-your-feature-name` 分支上进行开发。
2. 定期提交更改，提交信息要描述清楚：
   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

### 准备提交更改

1. 获取上游仓库的最新更改：
   ```bash
   git fetch upstream
   ```

2. 在最新的主分支上变基您的开发分支：
   ```bash
   git checkout dev-your-feature-name
   git pull --rebase
   ```

> **为什么要使用rebase**  
> 使用 git pull --rebase 可以帮助我们保持线性的 Git 历史记录，这是因为它会将本地的提交应用在从远程仓库拉取的最新提交之上，而不> 是创建一个新的合并提交。这种方法有助于保持提交历史的整洁和线性，便于阅读和理解。
> 使用 git pull --rebase 的优点
> 1. 保持线性历史记录
> 通过避免合并提交，git pull --rebase 确保所有提交都在一条直线上，这使得历史记录更加简洁清晰。
> 2. 提高代码审查效率
> 线性的提交历史使得代码审查变得更加容易。审查者可以更清晰地看到每个提交的变化，而不必处理复杂的合并提交。
> 3. 减少冲突
> 由于 git pull --rebase 会将本地提交重新应用在最新的远程提交之上，冲突通常会在本地解决，而不是在合并时。这样可以减少冲突的频率和复杂度。
> 4. 提高协作效率
> 当多个开发人员协作时，线性的历史记录使得每个人都能更容易地理解项目的进展和变化。这有助于团队成员更有效地协作。
> 5. 清晰的提交历史
> 线性的提交历史更容易追踪和理解每个功能或修复是如何引入的。这对于调试和回溯问题非常有帮助。
> 6. 避免冗余的合并提交
> 使用 git pull --rebase 可以避免产生大量的合并提交，这些合并提交通常是冗余的，并且会使历史记录变得混乱。
> 总的来说，使用 git pull --rebase 可以帮助团队保持一个清晰、整洁的提交历史，从而提高协作效率和代码质量。

3. 将您的提交压缩成一个提交：
   ```bash
   git rebase -i HEAD~<要压缩的提交数>
   ```
   在交互式变基中，将除第一个提交外的所有提交标记为“squash”。

4. 强制推送您的更改到您的分叉仓库：
   ```bash
   git push -f fork dev-your-feature-name
   ```

### 提交拉取请求

1. 进入原始仓库的GitHub页面。
2. 点击“Pull requests”然后点击“New pull request”。
3. 选择“compare across forks”并选择您的分叉和分支。
4. 点击“Create pull request”。

### 处理审查和CI要求

1. 确保所需的状态检查“L0”通过。
2. 等待至少一个代码所有者的批准审查。
3. 处理审查员的任何评论或请求的更改。
4. 在合并之前解决所有审查线程。

### 其他注意事项

- 仓库要求线性历史，因此避免合并提交。
- 所有拉取请求都需要代码所有者的审查。
- 确保在合并之前解决所有讨论线程。
- 主分支不允许直接推送，因此始终在单独的分支上工作并提交拉取请求。

按照这些步骤，您将能够在遵守分支保护规则的同时，为此仓库做出贡献，并保持清晰的线性历史。
