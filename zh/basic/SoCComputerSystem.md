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