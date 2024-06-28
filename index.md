---
sidebarDepth: 3
sidebar: auto
pageClass: "ysyx-index"
---

# 第六期"一生一芯"课程主页

* 课时: 每周六15:00~17:00
  * [B站直播](https://live.bilibili.com/24416626) | [录播链接](https://space.bilibili.com/2107852263/channel/collectiondetail?sid=1523995)

## 学习目标

"一生一芯"将会培养大家的综合能力.
大家完成学习之后, 将会对以下问题有一定的认识:
1. 处理器是如何设计的?
1. 程序是如何在计算机上运行的?
1. 如何对处理器的性能进行优化?
1. 如何使用/设计正确的工具高效地进行调试?
1. 如何自己编写测试用例进行单元测试?
1. RTL设计如何生成可流片的版图?

我们将会引导大家设计一款RISC-V流水线处理器,
并在自己设计的处理器上运行操作系统,
在操作系统上运行真实游戏.
达成指标的处理器将可以接入到SoC, 并获得流片机会.

## 教学资源

* `时间`一栏是以小时为单位的预估完成时间
  * 预估完成时间为`2`的内容, 一般没有相关的编程任务,
    只有2小时的视频录播, 用于补充讲解相关知识
  * 鉴于同学们的基础水平有高有低, 此处按照"中等水平"同学的能力来预估.
    但这里的"中等水平"并不是指"程序设计课程总评80分以上",
    而是指"学习心态端正, 编写过500行以上代码的单个程序, 并且懂得调试".
  * 如果你是零基础的初学者, 你应该预期花费这个数字`2~3`倍的时间来完成学习.
    不过你不必为此感到沮丧, 所谓"闻道有先后", 之所以其他同学学得快,
    很大一部分原因是因为他们之前已经付出努力迈过了初学者的阶段.
* 可点击图标跳转到相应资源
* 完整的讲义可通过页面右上方导航栏查看
* S阶段讲义内容仍然在🕊

`C` = C语言(程序/模拟器/系统软件) | `R` = RISC-V指令集 | `P` = 处理器设计 | `T` = 工具

<style scoped type="text/css">
	@media (max-width: 719px) {
		table {
			font-size: 3vw
		}
	}
	@media (min-width: 720px) {
		[task] {
			width: 20em
		}
	}
	table {
		display: table;
		vertical-align: center;
		counter-reset: week;
	}
	table > * {
		min-width: 100%;
	}
	td {
		vertical-align: center;
		text-align: center;
	}
	table [_],
	table [x] {
		padding: 0;
		width: 3.6em;
	}
	[stage-title] {
		word-break:break-all;
		padding: 1em;
	}
	thead {
		position: sticky;
		/* Don't forget this, required for the stickiness */
		top: var(--navbar-height);
		/* Styles */
		padding-top: 0.5em;
		padding-bottom: 0.5em;
		backdrop-filter: contrast(0.5) blur(4px) brightness(120%);
	}
	[task] {
		padding-left: 0.8em;
		padding-right: 0.8em;
		text-align: left;
	}
	/* Auto increment number inside week column */
	[week] {
		width: 2.1em;
	}
	td[week]::before {
		counter-increment: week;
		content: counter(week);
	}
	/* Place a checkmark inside <td x> (short hand for <td xked>) */
	td[x]::before {
		content: '✓';
	}
	td[x] {
		background-color: hsla(var(--hue), calc(2 * var(--saturation)), 50%, 0.1) !important;
	}
	/* Coloring by style */
	.Achievement td {
		font-weight: bold;
		line-height: 1em;
		background-color: hsla(100, 100%, 30%, 0.3) !important;
		/* border-left: 12px Green solid; */
	}
	tbody > tr {
		--hue: 0;
		--saturation: 50%;
		background-color: hsla(var(--hue), var(--saturation), 50%, 0.1) !important;
	}
	.Preliminary {
		--hue: 000;
	}
	.Stage-B {
		--hue: 110;
	}
	.Stage-A {
		--hue: 220;
	}
	.Stage-S {
		--hue: 330;
	}
	.Other-Topic {
		--saturation: 0%;
	}
</style>
<table id="schedule-table">
	<thead>
		<tr>
			<th _>阶段</th> <th week>序号</th>
			<th>任务</th> <th>时间</th> <th>讲义</th> <th>课件</th> <th>视频</th>
			<th _>C</th> <th _>R</th> <th _>P</th> <th _>T</th>
		</tr>
	</thead>
	<tbody>
		<tr class="Preliminary">
			<td stage-title rowspan="8">预学习阶段</td>
			<td week></td> <td task>如何科学地提问</td> <td>2</td>
            <td _><a href="2306/preliminary/0.1.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/01.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV14F411975K" target="_blank">🎬</a></td>
			<td _></td> <td _></td> <td _></td> <td _></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>Linux系统安装和基本使用</td> <td>10</td>
            <td _><a href="2306/preliminary/0.2.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/02.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1vF4119726" target="_blank">🎬</a></td>
			<td _></td> <td _></td> <td _></td> <td x></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>计算机系统的状态机模型</td> <td>2</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/03.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1oN411Y7FK" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>复习C语言</td> <td>20</td>
            <td _><a href="2306/preliminary/0.3.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/04.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV13z4y147mB" target="_blank">🎬</a></td>
			<td x></td> <td _></td> <td _></td> <td x></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>程序的执行和模拟器</td> <td>2</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/05.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1Rm4y1p7Cg" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td _></td> <td _></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>搭建verilator仿真环境</td> <td>5</td>
            <td _><a href="2306/preliminary/0.4.html" target="_blank">📚</a></td>
            <td _> - </td>
            <td _> - </td>
			<td x></td> <td _></td> <td x></td> <td _></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>数字电路基础实验</td> <td>20</td>
            <td _><a href="2306/preliminary/0.5.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/06.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1ZH4y1Q7Cv" target="_blank">🎬</a></td>
			<td _></td> <td _></td> <td x></td> <td _></td>
		</tr>
		<tr class="Preliminary">
			<td week></td> <td task>完成PA1</td> <td>30</td>
            <td _><a href="2306/preliminary/0.6.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/07.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1up4y1j7Ji" target="_blank">🎬</a></td>
			<td x></td> <td _></td> <td _></td> <td x></td>
		</tr>
		<tr class="Achievement">
			<td colspan="11"><i class="fa fa-flag"></i>申请入学答辩</td>
		</tr>
		<tr class="Stage-B">
			<td stage-title rowspan="16">基础阶段</td>
			<td week></td> <td task>支持RV32IM的NEMU</td> <td>10</td>
            <td _><a href="2306/basic/1.1.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/08.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV15h4y1A7Up" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>程序的机器级表示(上)</td> <td>2</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/09.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1ow411275B" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td _></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>程序的机器级表示(下)</td> <td>2</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/10.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV19H4y1d7Yi" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td _></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>用RTL实现最简单的处理器</td> <td>5</td>
            <td _><a href="2306/basic/1.2.html" target="_blank">📚</a></td>
            <td _> - </td>
            <td _> - </td>
			<td _></td> <td _></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>AM运行时环境</td> <td>5</td>
            <td _><a href="2306/basic/1.3.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/11.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1Vu4y1s73Y" target="_blank">🎬</a></td>
			<td x></td> <td _></td> <td _></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>工具和基础设施</td> <td>5</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/12.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1RM411Q7Au" target="_blank">🎬</a></td>
			<td _></td> <td _></td> <td _></td> <td x></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>支持RV32E的单周期NPC</td> <td>10</td>
            <td _><a href="2306/basic/1.4.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/13.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1rc411f7mK" target="_blank">🎬</a></td>
			<td _></td> <td _></td> <td x></td> <td x></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>ELF文件和链接</td> <td>2</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/14.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1Ly4y1w7hn" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td _></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>设备和输入输出</td> <td>10</td>
            <td _><a href="2306/basic/1.5.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/15.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1sb4y1g7Xu" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>调试技巧</td> <td>2</td>
            <td _> - </td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/16.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1Vz4y1A7Rt" target="_blank">🎬</a></td>
			<td _></td> <td _></td> <td _></td> <td x></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>异常处理和RT-Thread</td> <td>15</td>
            <td _><a href="2306/basic/1.6.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/17.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1734y1w7ro" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>总线</td> <td>10</td>
            <td _><a href="2306/basic/1.7.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/18.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1gj411s7ah" target="_blank">🎬</a></td>
			<td _></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>SoC计算机系统(上)</td> <td>15</td>
            <td _><a href="2306/basic/1.8.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/19.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1NC4y1u7K3" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>SoC计算机系统(下)</td> <td>15</td>
            <td _><a href="2306/basic/1.8.html" target="_blank">📚</a></td>
            <td _><a href="https://ysyx.oscc.cc/slides/2306/20.html#/" target="_blank">📰</a></td>
            <td _><a href="https://www.bilibili.com/video/BV1FC4y1k7mP" target="_blank">🎬</a></td>
			<td x></td> <td x></td> <td x></td> <td _></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>性能优化和简易缓存</td> <td>20</td>
            <td _><a href="2306/basic/1.9.html" target="_blank">📚</a></td>
            <td _> </td>
            <td _> </td>
			<td _></td> <td _></td> <td x></td> <td x></td>
		</tr>
		<tr class="Stage-B">
			<td week></td> <td task>流水线处理器</td> <td>0</td>
            <td _><a href="2306/basic/1.10.html" target="_blank">📚</a></td>
            <td _> </td>
            <td _> </td>
			<td _></td> <td _></td> <td x></td> <td _></td>
		</tr>
		<tr class="Achievement">
			<td colspan="11"><i class="fa fa-flag"></i>达成B阶段流片指标</td>
		</tr>
		<tr class="Stage-A">
			<td stage-title rowspan="1">进阶阶段</td>
			<td week></td> <td task>由于时间关系, 详细的A阶段讲义无法按时发布. 我们先列出<a href="2306/advanced/advanced.html" target="_blank">一些大纲📚</a>, 感兴趣的同学可以按照我们给出的方向自行探索. </td> <td>0</td>
            <td _> </td> <td _> </td> <td _> </td>
            <!-- 环境       工具       数电        微结构       软件 -->
			<td _></td> <td _></td> <td _></td> <td _></td>
		</tr>
	</tbody>
</table>
<!-- End of table -->

> #### info::页面加载条卡住了？
>
> 跳转页面时, 如果进度条卡住 3 秒以上, 很可能是由于我们推送了网页版本更新.<br>
> 鉴于我们还在频繁更新、修订文档, 近期可能会比较容易遇到跳转卡住的情况.<br>
> 遇到这种情况, 只需要 __`刷新整个页面`__ 即可继续学习咯

## 往期课程主页

* [第五期](../2205/index.md)

## 其他资源

* [提问模板](../2205/misc/ask.md)

## 活动记录

* 2023/08/25 - [开源芯片技术生态论坛（原“一生一芯”技术论坛）](../events/20230825-2nd-tech-forum.md)
* 2023/07/02 - [第六期“一生一芯”启动会](https://space.bilibili.com/2107852263/channel/collectiondetail?sid=1497409)
* 2022/11/20 - [从软件工程视角看芯片开源与敏捷设计(包云岗)](https://www.bilibili.com/video/BV1Dd4y1474D/)
* 2022/08/28 - [第一届“一生一芯”技术论坛暨第五期启动会](../events/20220828-1st-tech-forum.md)
* 2022/03/12 - [软硬件协同能力在芯片设计中的应用(金越, 胡博涵, 高泽宇)](https://www.bilibili.com/video/BV1334y187zC/)
