---
sidebar_position: 9
---

# SoC计算机系统

:::info[总线讲义更新]
我们在2023年11月29日在总线部分的讲义中追加了UART和CLINT的练习, 完成它们有利于接下来SoC的接入.
:::

实现总线之后, 我们就可以将NPC接入到"一生一芯"的SoC环境中, 为流片做好准备!
SoC是System On Chip的缩写, 这意味着SoC不仅仅只包含一个处理器,
还有诸多的外围设备, 以及连接处理器和外围设备之间的总线.
在这里, 我们把存储器也看成一种广义的设备, 毕竟对于SoC来说,
存储器和其他狭义的设备没有区别, 都是一段可以访问的地址空间.

## ysyxSoC

我们提供一个可以在verilator上运行的SoC环境, 称为ysyxSoC.
我们提前让大家接入ysyxSoC, 一方面是为了让大家学习其中的细节,
另一方面也是尽早在SoC环境中测试你的NPC,
从而帮助你缩短从完成流片考核到提交代码之间的时间.
当然, 在接入ysyxSoC后你还需要完成一些优化工作, 才能达成B阶段的流片指标.

### ysyxSoC介绍

我们先给出ysyxSoC包含的外围设备和相应的地址空间.

<!--
TODO: 加个总线和设备的框图
-->

| 设备           | 地址空间                 |
| ---            | ---                      |
| CLINT          | `0x0200_0000~0x0200_ffff`|
| SRAM           | `0x0f00_0000~0x0fff_ffff`|
| UART16550      | `0x1000_0000~0x1000_0fff`|
| SPI master     | `0x1000_1000~0x1000_1fff`|
| GPIO           | `0x1000_2000~0x1000_200f`|
| PS2            | `0x1001_1000~0x1001_1007`|
| MROM           | `0x2000_0000~0x2000_0fff`|
| VGA            | `0x2100_0000~0x211f_ffff`|
| Flash          | `0x3000_0000~0x3fff_ffff`|
| ChipLink MMIO  | `0x4000_0000~0x7fff_ffff`|
| PSRAM          | `0x8000_0000~0x9fff_ffff`|
| SDRAM          | `0xa000_0000~0xbfff_ffff`|
| ChipLink MEM   | `0xc000_0000~0xffff_ffff`|
| Reverse        | 其他                     |

图中除了AXI以外, 还有[APB][apb manual], [wishbone][wishbone manual]和[SPI][spi manual]这些总线.
不过这些总线都比AXI简单, 甚至比AXI-Lite还简单.
你已经了解AXI-Lite了, 因此学习这些总线协议也并不难, 需要时可查阅相关手册.

[apb manual]: https://developer.arm.com/documentation/ihi0024/latest/
[wishbone manual]: https://cdn.opencores.org/downloads/wbspec_b3.pdf
[spi manual]: https://www.mouser.com/pdfdocs/tn15_spi_interface_specification.PDF

:::danger[一些设备和地址空间在将来可能会产生变化]
为了获得更好的展示效果, “一生一芯”项目组正在重新设计SoC,
一些设备和地址空间可能会在将来发生变化,
最终的设备地址空间分配情况以流片版本为准.
不过这并不影响目前的学习, 你可以安全地忽略这一情况.
:::

<!-- -->
:::todo[获取ysyxSoC的代码]
你需要克隆[ysyxSoC](https://github.com/OSCPU/ysyxSoC)项目:
```bash
cd ysyx-workbench
git clone git@github.com:OSCPU/ysyxSoC.git
```
接下来你将会使用ysyxSoc提供的设备进行仿真, 来验证NPC可以正确访问SoC中的设备.
我们将在下文介绍具体如何接入.

需要注意的是, ysyxSoC与最终流片使用的SoC仍有一定差异.
因此, 通过ysyxSoC的测试并不代表最终也能通过流片SoC仿真环境的测试.
但即使这样, 也可以借助ysyxSoC项目提前暴露一部分问题,
若将来接入流片SoC时仍有问题, 则可重点关注两者差异带来的影响.
:::

对大家来说, ysyxSoC项目有两部分值得大家关注. 第一部分是ysyxSoC的总线部分,
我们主要借助开源社区[rocket-chip][rocket-chip]项目的[diplomacy][diplomacy]框架来实现它,
相关代码在`ysyxSoC/src/`目录下.
借助diplomacy, 我们可以很容易地将一个具备总线接口的设备接入ysyxSoC.
例如, 我们只需要改动以下两行Chisel代码, 即可实例化一个AXI接口的MROM设备,
同时指定其地址空间为`0x2000_0000~0x2000_0fff`, 并将其连接到AXI Xbar的下游.
如果采用传统的Verilog方式来接入, 仅仅是端口声明就要添加将近100行代码,
这还没计算对AXI Xbar的修改.

[rocket-chip]: https://github.com/chipsalliance/rocket-chip
[diplomacy]: https://github.com/chipsalliance/rocket-chip/blob/master/docs/src/diplomacy/adder_tutorial.md

```diff
diff --git a/src/SoC.scala b/src/SoC.scala
index dd84776c..758fb8d1 100644
--- a/src/SoC.scala
+++ b/src/SoC.scala
@@ -39,9 +39,10 @@ class ysyxSoCASIC(implicit p: Parameters) extends LazyModule {
     AddressSet.misaligned(0x10001000, 0x1000) ++    // SPI controller
     AddressSet.misaligned(0x30000000, 0x10000000)   // XIP flash
   ))
+  val lmrom = LazyModule(new AXI4MROM(AddressSet.misaligned(0x20000000, 0x1000)))

   List(lspi.node, luart.node).map(_ := apbxbar)
-  List(chiplinkNode, apbxbar := AXI4ToAPB()).map(_ := xbar)
+  List(chiplinkNode, apbxbar := AXI4ToAPB(), lmrom.node).map(_ := xbar)
   xbar := cpu.masterNode

   override lazy val module = new Impl
```

第二部分是ysyxSoC的设备部分, 我们收集了一些设备控制器的开源项目,
相关代码在`ysyxSoC/perip/`目录下.
部分设备通过直接实例化rocket-chip项目中的IP来实现,
这部分设备并不在`ysyxSoC/perip/`目录下, 具体可以参考`ysyxSoC/src/`中的相关代码.

### 接入ysyxSoC

由于SoC中包含多个设备, 这些设备的属性可能有所不同, 这将会带来一些新问题.
例如, `ysyxSoC/perip/uart16550/rtl/uart_defines.v`中有如下代码:

```
// Register addresses
`define UART_REG_RB `UART_ADDR_WIDTH'd0  // receiver buffer
`define UART_REG_IE `UART_ADDR_WIDTH'd1  // Interrupt enable
`define UART_REG_II `UART_ADDR_WIDTH'd2  // Interrupt identification
`define UART_REG_LC `UART_ADDR_WIDTH'd3  // Line Control
```

上述代码定义了UART中一些设备寄存器的地址, 由于UART位于`0x1000_0000`,
因此上述4个寄存器的地址分别是`0x1000_0000`, `0x1000_0001`, `0x1000_0002`, `0x1000_0003`.
假设UART通过AXI-Lite总线连接Xbar, 考虑通过AXI-Lite读取receiver buffer中的内容.
显然, `araddr`信号应为`0x1000_0000`, 但如果要读取4字节,
是否会同时读出后面3个设备寄存器的内容呢?

我们之前没有考虑"读多长"的问题, 是因为对内存进行读操作时, 并不会改变内存中存储数据的状态,
因此无论CPU期望读出多少字节, 总线都可以一次读出4字节或8字节, 让CPU从中选出目标数据.
这甚至有助于一些带有缓存的CPU提高性能:
从内存中读取一次数据一般需要较长时间, 如果能充分利用总线的带宽,
一次多读出一些数据, 就有可能减少将来真正访问内存的次数.

不过对于设备的访问, 上述前提不再成立:
访问设备寄存器可能会改变设备的状态!
这意味着, 对于设备来说, 读出1字节和读出4字节, 最终导致的行为可能不同.
如果我们没有按照设备寄存器的约定来访问它们, 可能会导致设备进入不可预测的状态.
因此在通过总线访问设备时, 我们需要仔细地处理这个问题.

但是, AXI-Lite总线并不能解决上述问题, 其AR通道中没有足够的信号用于编码读取长度信息,
设备只能认为实际访问的数据位宽与AXI-Lite总线的数据位宽相同.
因此, 若AXI-Lite总线上的单个读请求覆盖多个设备寄存器, 则可能导致设备状态出错.
也正因为这个原因, 并非所有设备都适合通过AXI-Lite总线接入.

例如, 上述UART就不能通过数据位宽为32位的AXI-Lite总线接入,
因为UART中设备寄存器的间隔只有1字节, 这意味着通过AXI-Lite读出其中的一个设备寄存器,
也会影响相应的设备寄存器的状态, 这并不是我们期望的.
对于另一款设备寄存器地址空间如下的UART, 则可以通过数据位宽为32位的AXI-Lite总线接入,
因为这些寄存器的间隔为4字节, 正好能在不影响相邻寄存器状态的情况下读出其中某个寄存器.

```
// Register addresses
`define UART_REG_RB `UART_ADDR_WIDTH'd0  // receiver buffer
`define UART_REG_IE `UART_ADDR_WIDTH'd4  // Interrupt enable
`define UART_REG_II `UART_ADDR_WIDTH'd8  // Interrupt identification
`define UART_REG_LC `UART_ADDR_WIDTH'd12 // Line Control
```

为了解决AXI-Lite的上述问题, 完整的AXI总线协议通过`arsize`/`awsize`信号来指示实际访问的数据位宽,
同时引入"窄传输"的概念, 用于指示"实际数据位宽小于总线数据位宽"的情况.
这两个"数据位宽"的概念并非完全一致, 具体地, 总线数据位宽是在硬件设计时静态决定的,
它表示一次总线传输的最大数据位宽, 也用于计算总线的理论带宽;
而实际数据位宽(即`arsize`/`awsize`信号的值)则由软件访存指令中的位宽信息动态决定,
它表示一次总线传输的实际数据位宽, 例如, `lb`指令只访问1字节, 而`lw`指令则访问4字节.

有了`arsize`/`awsize`信号, 设备就可以得知软件需要访问的实际数据位宽,
从而在若干设备寄存器的地址紧密排布时, 亦可仅访问其中的某个寄存器, 避免意外改变设备的状态.

:::todo[生成ysyxSoC的Verilog代码]
首先你需要进行一些配置和初始化工作:
1. 根据[mill的文档介绍][mill doc]安装mill
   * 可通过`mill --version`检查安装是否成功;
     此外, `rocket-chip`项目要求`mill`的版本不低于`0.11`,
     如果你发现`mill`的版本不符合要求, 请安装最新版本的`mill`
1. 在`ysyxSoC/`目录下运行`make dev-init`命令, 拉取`rocket-chip`项目

以上两个步骤只需要进行一次即可.
完成上述配置后, 在`ysyxSoC/`目录下运行`make verilog`,
生成的Verilog文件位于`ysyxSoC/build/ysyxSoCFull.v`.
:::

[mill doc]: https://mill-build.com/mill/Intro_to_Mill.html

:::todo[接入ysyxSoC]
依次按照以下步骤将NPC接入ysyxSoC:
1. 依照`ysyxSoC/spec/cpu-interface.md`中的`master`总线, 将之前实现的AXI4Lite协议扩展到完整的AXI4
2. 调整NPC顶层接口, 使其与`ysyxSoC/spec/cpu-interface.md`中的接口命名规范<font color=red>**完全一致**</font>,
   包括信号方向, 命名和数据位宽
   * 对于不使用的顶层输出端口, 需要将其赋值为常数`0`
   * 对于不使用的顶层输入端口, 悬空即可
   * 为了兼容前几期的设计, 我们采用64位数据位宽的接口,
     如果NPC是32位, 目前只需要使用数据的低32位即可, 后面我们会再次讨论这个问题
3. 将`ysyxSoC/perip`目录及其子目录下的所有`.v`文件加入verilator的Verilog文件列表
4. 将`ysyxSoC/perip/uart16550/rtl`和`ysyxSoC/perip/spi/rtl`两个目录加入verilator的include搜索路径中
   * 具体如何加入, 请RTFM(`man verilator`或verilator的官方手册)
     * 如果你从来没有查阅过verilator有哪些选项, 我们建议你趁这次机会认真阅读一下手册中的`argument summary`,
       你很可能会发现一些新的宝藏
5. 在verilator编译选项中添加`--timescale "1ns/1ns"`和`--no-timing`
6. 将`ysyxSoCFull`模块(在`ysyxSoC/build/ysyxSoCFull.v`中定义)设置为verilator仿真的顶层模块
   * 如果你不知道如何加入, RTFM
7. 将`ysyxSoC/build/ysyxSoCFull.v`中的`ysyx_00000000`模块名修改为你的处理器的模块名
   * 注意, 你的处理器模块不应该包含之前作为习题的AXI4-Lite接口的SRAM和UART,
     我们将使用ysyxSoC中的存储器和UART替代它们
   * 但你的处理器模块应该包含CLINT, 它将作为流片工程中的一个模块, ysyxSoC不包含它
8. 在仿真的cpp文件中加入如下内容, 用于解决链接时找不到`flash_read`和`mrom_read`的问题
   ```cpp
   extern "C" void flash_read(int32_t addr, int32_t *data) { assert(0); }
   extern "C" void mrom_read(int32_t addr, int32_t *data) { assert(0); }
   ```
9. 在仿真环境的`main`函数中仿真开始前的位置加入语句`Verilated::commandArgs(argc, argv);`,
   用于解决运行时plusargs功能报错的问题
10. 通过verilator编译出仿真可执行文件
   * 如果你遇到了组合回环的错误, 请自行修改你的RTL代码
11. 尝试开始仿真, 你将观察到代码进入了仿真的主循环, 但NPC无有效输出.
   我们将在接下来解决这个问题

`ysyxSoC`中还有一些代码检查相关的步骤说明, 但你后续还要改进NPC,
因此我们将要求你在考核前再进行代码检查.
如果你感兴趣, 目前开展代码检查的工作亦可, 我们不做强制要求.
:::

接下来我们会依次介绍ysyxSoC中的设备, 以及如何让程序使用它们.
一些任务会要求你在RTL层面对一些设备模块进行实现或增强,
对于这些任务的大部分, 你都可以选择采用Chisel或者Verilog来完成.
特别地, 如果你选择使用Chisel, 你仍然需要阅读一些Verilog代码来帮助你完成任务.

## 最简单的SoC

回想TRM的其中两个要素, 有程序可以执行, 并且可以输出.
在之前的仿真过程中, 这两点都是通过仿真环境来实现的:
仿真环境将程序的镜像文件放到存储器中, NPC取第一条指令的时候, 程序已经位于存储器中了;
为了输出, 我们借助DPI-C函数`pmem_read()`调用仿真环境的功能, 并通过仿真环境的`putchar()`函数来实现输出.
但在真实的SoC中, 板卡上电后并没有仿真环境或运行时环境提供上述功能, 因此需要通过硬件来实现这些基本功能.

### 程序的存放

首先需要考虑程序放在哪里.
一般的存储器是易失存储器(volatile memory), 例如SRAM和DRAM, 它们在上电时并没有存放有效数据.
如果上电后CPU直接从内存中读取指令执行, 存储器读出什么数据是未定义的,
因此整个系统的行为也是未定义的, 从而无法让CPU执行预期的程序.

因此, 需要使用一种非易失存储器(non-volatile memory)来存放最初的程序,
使其内容能在断电时保持, 并在上电时能让CPU马上从中取出指令.
一个最简单的解决方案就是ROM(Read-Only Memory), 每次从ROM中相同位置读出的内容都是相同的.

ROM的实现有很多种, 总体上都是通过某种方式来将信息(在这里也是程序)存储在ROM中,
而且这种存储方式不会受到断电的影响, 从而具备非易失的属性.
如果考虑在ysyxSoC中的易用性, 最合适的就是mask ROM(掩膜ROM), 简称MROM,
其本质是将信息"硬编码"在门电路中, 因此对NPC来说访问方式非常直接.

不过因为MROM的某些问题, 我们并不打算在流片的时候使用它.
但MROM作为ysyxSoC中的第一个简单的非易失存储器来存放程序, 对我们测试ysyxSoC的接入还是非常合适的.
我们已经在ysyxSoC中添加了一个AXI4接口的MROM控制器, 其地址空间是`0x2000_0000~0x2000_0fff`.

:::todo[测试MROM的访问]
修改NPC的复位PC值, 使其从MROM中取出第一条指令,
并修改`mrom_read()`函数, 使其总是返回一条`ebreak`指令.
如果你的实现正确, NPC取到的第一条指令即是`ebreak`指令, 从而结束仿真.

因为NEMU还没有添加MROM的支持, 而NPC此时需要从MROM中取指, 故此时DiffTest机制不能正确工作.
不过目前的测试程序规模还很小, 你可以先关闭DiffTest功能, 后面我们再回过头来处理DiffTest的问题.
:::

### 输出第一个字符

可以存放程序之后, 我们就需要考虑如何输出了.
为此, SoC中还需要提供一个最基本的输出设备.
真实的SoC中通常使用UART16550, 它包含一些设备寄存器, 用于设置字符长度, 波特率等信息.
在发送队列未满时, 即可通过写入对应的设备寄存器来发送字符.

ysyxSoC中已经集成了一个UART16550控制器.
为了测试它, 我们先编写一个最简单的程序`char-test`, 它直接输出一个字符之后就陷入死循环:

```c
#define UART_BASE 0x?L
#define UART_TX   ?
void _start() {
  *(volatile char *)(UART_BASE + UART_TX) = 'A';
  *(volatile char *)(UART_BASE + UART_TX) = '\n';
  while (1);
}
```

:::todo[在ysyxSoC中输出第一个字符]
你需要:
1. 根据ysyxSoC中的设备地址空间约定, 以及UART手册(在`ysyxSoC/perip/`下的相关子目录中)中输出寄存器的地址,
   来填写上述C代码中的`?`处, 使代码可以正确访问输出寄存器来输出一个字符
2. 通过`gcc`和`objcopy`命令编译`char-test`, 并将ELF文件中的代码节单独抽取到`char-test.bin`中
3. 修改仿真环境的相关代码, 读入`char-test.bin`并将其作为MROM的内容,
   然后正确实现`mrom_read()`函数, 使其根据参数`addr`返回MROM中相应位置的内容

如果你的实现正确, 仿真过程将会在终端输出一个字符`A`.

Hint: 如果你不知道如何通过`gcc`和`objcopy`命令实现上述功能,
你可以参考"一生一芯"某节课的视频或课件. 如果你不知道应该参考哪一节课,
我们建议你把所有视频和课件都查看一遍, 相信这能帮助你补上很多你还不了解的知识点.
:::

<!-- -->
:::hint[RTFM理解总线协议]
如果你发现仿真过程中发现总线的行为难以理解, 先尝试RTFM尽可能理解手册中的所有细节.
随着项目复杂度的增加, 你将要为不仔细RTFM付出越来越大的代价.
:::

如果你通过`objdump`等工具查看生成的ELF文件,
你会发现代码节的地址位于地址`0`附近, 与MROM的地址空间不一致.
实际上, 这个程序很小, 我们很容易确认, 无论将它放在哪个地址, 都能正确地按预期执行.
对于更复杂的程序, 上述条件不一定能满足, 我们需要显式地将程序链接到一个正确的位置,
使得NPC复位后可以正确地执行程序. 我们将在后面解决这个问题.

此外, 在真实的硬件场景下, 串口还需要根据波特率来将字符转换成串行的输出信号,
通过线缆传送到串口的接收端, 因此发送端在发送字符前, 软件还需要在串口的配置寄存器中设置正确的除数.
但当前的ysyxSoC仿真环境中并没有串口的接收端, 因此我们在串口控制器的RTL代码中添加了若干打印语句,
直接将串口发送队列中的字符打印出来, 这样软件也无需设置除数.
也因此, 上述代码在真实的硬件场景中并不一定能正常工作,
但作为前期测试, 这可以方便我们快速检查字符是否被正确写入串口发送队列.
我们将在成功运行足够多程序后, 再添加除数的设置, 使得代码可以在真实的硬件场景中工作.

:::todo[去掉换行也能输出]
上述`char-test`在输出字符`A`之后, 还输出一个换行符.
尝试仅仅输出字符`A`而不输出换行符, 你应该会观察到仿真过程连字符`A`都不输出了.
但如果每次输出一个字符之后都紧接着输出一个换行符, 打印出的信息将很难阅读.

为了解决这个问题, 你只需要给verilator传递一个选项.
尝试根据你对这个问题的理解, 通过RTFM找到并添加这个选项.
如果你添加了正确的选项, 你将会看到即使上述程序仅输出单个字符`A`, 也能成功输出.

Hint: PA讲义已经在好几处讨论过相关问题了.
如果你对此没有任何印象, 我们建议你重新仔细阅读讲义的每一处细节来查缺补漏.
:::

## 更实用的SoC

确认ysyxSoC可以输出一个字符之后, 我们认为NPC访问设备的数据通路基本上打通.
不过, MROM虽然可以很好地实现程序的存放, 但它有一个很大的问题: 不支持写入操作.
但大多数程序都需要向存储器写入数据, 例如, C语言的调用约定允许被调用函数在栈上创建栈桢, 并通过栈桢存取数据.
因此, 一个仅包含MROM作为存储器的SoC可能无法支持那些需要调用函数的程序, 显然这并不实用.
为了支持写入操作, 我们需要添加RAM作为存储器, 并将程序的数据分配在RAM中.

最简单的RAM就是我们之前提到的SRAM, 我们可以在SoC中集成SRAM存储器.
SRAM能够使用与处理器制造相同的工艺进行生产, 同时读写延迟只有1周期, 因此速度很快.
但SRAM的存储密度较低, 需要占用一定的芯片面积, 因此从流片价格的角度来计算, 成本是十分昂贵的.
考虑到流片成本, 我们只在SoC中提供8KB的SRAM.
我们已经在ysyxSoC中添加了一个AXI4接口的SRAM控制器, 其地址空间是`0x0f00_0000~0x0f00_1fff`.
注意到在前文的介绍中, SRAM的地址空间是`0x0f00_0000~0x0fff_ffff`, 共16MB,
这只是说明ysyxSoC中给SRAM预留了16MB的地址空间, 但考虑到实际的成本, 只使用了其中的8KB,
剩余的地址空间是空闲的, NPC不应该访问这部分空闲的地址空间.

有了这部分SRAM的空间, 我们就可以考虑将栈分配在SRAM空间, 从而支持一些AM程序的执行了.

### 为ysyxSoC添加AM运行时环境

为了运行更多程序, 我们需要基于ysyxSoC提供向程序提供相应的运行时环境.
噢, 这不就是实现一个新的AM吗? 这对你来说已经很熟悉了.
不过我们还是需要考虑ysyxSoC的一些属性对于运行时环境带来的影响.

首先我们来看TRM. 回顾TRM的内容, 我们需要考虑如何在ysyxSoC上实现TRM的API:
* 可以用来自由计算的内存区间 - 堆区
  * 堆区需要分配在可写的内存区间, 因此可以分配在SRAM中
* 程序 "入口" - `main(const char *args)`
  * `main()`函数由AM上的程序提供, 但我们需要考虑整个运行时环境的入口,
    即需要将程序链接到MROM的地址空间, 并保证TRM的第一条指令与NPC复位后的PC值一致
* "退出"程序的方式 - `halt()`
  * ysyxSoC不支持"关机"等功能, 为方便起见, 可借助`ebreak`指令让仿真环境结束仿真
* 打印字符 - `putch()`
  * 可通过ysyxSoC中的UART16550进行输出

由于NPC复位后从MROM开始执行, 而MROM不支持写入操作, 因此我们需要额外注意:
1. 程序中不能包含对全局变量的写入操作
1. 栈区需要分配在可写的SRAM中

:::todo[为ysyxSoC添加AM运行时环境]
添加一个`riscv32e-ysyxsoc`的新AM, 并按照上述方式提供TRM的API.
添加后, 将`cpu-tests`中的`dummy`测试编译到`riscv32e-ysyxsoc`,
并尝试在ysyxSoC的仿真环境中运行它.

Hint: 为了完成这个任务, 你需要一些链接的知识.
如果你不熟悉, 可以参考"一生一芯"相关的视频和课件.
:::

<!-- -->
:::option[无法运行的测试]
尝试在ysyxSoC中运行`cpu-tests`中的`fib`, 你将发现运行失败.
尝试阅读提示信息, 你觉得应该如何解决这个问题?
:::

<!-- -->
:::todo[重新添加DiffTest]
我们新增了MROM和SRAM, 接下来一段时间我们都会在MROM和SRAM上运行程序.
但目前NEMU并没有MROM和SRAM, 如果我们在DiffTest的时候跳过MROM和SRAM和访问,
将会跳过所有指令的执行, 使得DiffTest将无法起到预期的作用.

为了重新添加DiffTest, 你需要在NEMU中添加MROM和SRAM,
并在NPC的仿真环境初始化DiffTest时, 将MROM中的内容同步到NEMU中,
然后检查在MROM中执行的每一条指令.

你可以按照你的想法修改NEMU的代码, 但我们还是建议你尽量不添加新的DiffTest API,
框架代码提供的DiffTest API已经足够实现上述功能了.
:::

<!-- -->
:::option[让NPC抛出Access Fault异常]
尽管这不是必须的, 我们建议你在NPC中添加Access Fault的实现.
在系统运行发生意外导致访问了未分配的地址空间, 或者设备返回错误时,
ysyxSoC可以通过AXI的`resp`信号传递相关的错误信息.
即使程序未启动CTE, 也可以让NPC在发生这些事件时跳转到地址`0`,
让你感觉到程序运行不正常.
相比于放过这些错误事件让NPC继续运行, 这也许能帮助你节省大量的调试时间.
:::

### 内存访问测试

可以执行`dummy`测试后, 我们认为NPC基本上能成功访问ysyxSoC的SRAM了.
我们知道, 访存是程序运行的基础. 为了对访存行为进行更充分的测试,
我们需要编写一个程序`mem-test`来测试更大范围的内存.

从范围上看, `mem-test`希望能测试所有可写内存区域.
但`mem-test`本身的运行需要栈区的支持, 而栈区需要分配在可写内存区域,
因此在测试时需要绕开栈区, 避免栈区内容被覆盖, 导致`mem-test`本身运行出错.
我们可以把栈区放在SRAM的末尾, 并把堆区的起始地址设置在SRAM的开始,
堆区的结束地址设置在栈区的起始地址(即栈顶的初值).
设置好堆区的范围之后, 就可以把堆区作为`mem-test`的测试范围.

从测试方式上看, 我们采用一种最直观的方式: 先往内存区间写入若干数据, 再读出并检查.
我们可以让写入的数据与内存的地址相关, 从而方便检查, 例如`data = addr & len_mask`.
以下示意图展示了通过8位, 16位, 32位, 64位的写入地址和地址之间的关系.

```txt
    SRAM_BASE                                    SRAM_BASE + 0x10
        |                                               |
        V                                               V
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
8-bit   |00|01|02|03|04|05|06|07|08|09|0a|0b|0c|0d|0e|0f|
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
16-bit  |00|00|02|00|04|00|06|00|08|00|0a|00|0c|00|0e|00|
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
32-bit  |00|00|00|0f|04|00|00|0f|08|00|00|0f|0c|00|00|0f|
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
64-bit  |00|00|00|0f|00|00|00|00|08|00|00|0f|00|00|00|00|
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

测试分两步, 第一步是依次向各个内存区间写入相应数据,
第二步是依次从各个内存区间中读出数据, 并检查是否与之前写入的数据一致.
可分别通过8位, 16位, 32位, 64位的写入方式重复上述过程.

