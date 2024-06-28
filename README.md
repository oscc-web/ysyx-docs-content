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
