---
sidebar_position: 5
---

# Basic Digital Circuit Lab

Digital Circuits is the introductory course of "One Student One Chip", we have listed some of the knowledge points that you need to master, you not only need to know their concepts, but also need to learn to use the hardware description language to implement the circuit module respectively.

- Binary encoding of information
- Combinational Logic Design: Multiplexers, Decoders, Priority Encoders, Adders, Comparators
- Timing logic design: clocks, D-flip-flops, counters, SRAM and DRAM, finite state machines, timing analysis

:::info[Digital Circuit Study Materials]
- [Digital Design and Computer Architecture: RISC-V Edition][book] ch1-5
- [HDLBits — Verilog Practice][hdlbits], recommand to read and practice in same time
- [USTC Verilog OA][ustc verilog oj]\(Chinese, need registration and login), recommand to read and practice in same time
- Verilog Advanced Digital System Design Techniques and Case Studies
:::
[book]: https://pages.hmc.edu/harris/ddca/ddcarv.html

:::info[Chisel Study Materials]
It is recommended to study in the following order:

1. [Chisel Bootcamp][bootcamp] It is a very good chisel tutorial, also supports running chisel code online, you can write chisel code while learning. Among them are
   - Chapter 1 is an introduction to scala.
   - Chapter 2 is chisel basics.
   - Chapter 3 is a mix of advanced scala features and chisel.
   - Chapter 4 is about the FIRRTL backend You will need to complete the first two chapters, and we strongly recommend that you take Chapter 3. Chapter 4 is not directly related to this course and can be used as extra reading material.
2. [Chisel Users Guide][users guide] It's a good introduction to chisel, as it organizes the features of chisel in a more systematic way.
3. [Chisel cheatsheet][cheatsheet] A concise list of common uses cases of the chisel language.
4. [Chisel API][api] All APIs of the chisel library are listed in detail for reference.

Then try to use Chisel to complete the above digital circuit experiments, you just need to connect the compiled Verilog code to the verilator and NVBoard.

Welcome to join the Chisel communication group (scan the QR code below on WeChat to contact the teaching assistant to join the group).

![Wang Rui](/ysyx-img/zh/preliminary/wangrui.jpg)
:::
[bootcamp]: https://mybinder.org/v2/gh/freechipsproject/chisel-bootcamp/master

[users guide]: https://www.chisel-lang.org/docs

[cheatsheet]: https://github.com/freechipsproject/chisel-cheatsheet/releases/latest/download/chisel_cheatsheet.pdf

[api]: https://www.chisel-lang.org/api/latest/

:::info[verilog learning materials]
What we need to cultivate is hardware thinking. We need to have circuits in our minds before writing code by hand. The essence of verilog is a hardware description language rather than a hardware design language. You can watch [verilog introductory video][verilog1] and [Introduction to syntax][verilog2] Get started.
:::
[verilog1]: https://www.bilibili.com/video/BV1PS4y1s7XW

[verilog2]: https://vlab.ustc.edu.cn/guide/doc_verilog.html

:::info[vscode automatic jump plugin]
- If you choose chisel programming, metals plugin is recommended.
- If you choose verilog programming, we recommend the [digital ide](https://digital-eda.github.io/DIDE-doc-Cn/#/?id=digital-ide-version-030) plugin.
:::
[hdlbits]: https://hdlbits.01xz.net/wiki/Main_Page

[ustc verilog oj]: https://verilogoj.ustc.edu.cn/oj/

:::warning[Complete digital circuit experiments with NVBoard]
We first recommend Nanjing University’s [Digital Circuit and Computer Composition Experiment][dlco].

Nanjing University has carried out teaching reforms and integrated the two courses of "Digital Circuits" and "Principles of Computer Composition". The experimental content runs from the basics of digital circuits to simple processor design. Recently, it has tried to add content related to the program runtime environment, which is related to The main content of "One Student One Chip" fits very well.

The following parts are **required exercises**:

- Experiment 1 Selector
- Experiment 2 Decoder and Encoder
- Experiment 3 Adder and ALU
- Experiment 6 Shift Register and Barrel Shifter
- Experiment 7 State Machine and Keyboard Input

Other contents are optional for understanding and are not specified in the preliminary part.  With NVBoard, you can use it as an FPGA and use it to implement experimental content that requires FPGA support.
:::
[dlco]: https://nju-projectn.github.io/dlco-lecture-note/index.html

:::warning[Evaluate timing after circuit synthesis]
We provide a post-synthesis timing evaluation project based on open source EDA. This project synthesizes the RTL design through the [open source RTL synthesizer yosys][yosys] and maps it to a 45nm open source process library [nangate45][nangate45], and then synthesizes the synthesized netlist file and process library The standard unit information file in is input into the [open source static timing analysis tool iSTA][ista]. iSTA will quickly evaluate the timing paths in the RTL design and provide several paths with the smallest timing margin for reference by RTL designers. Through the above method, RTL Designers can quickly learn the timing of RTL designs and quickly iterate on RTL designs.

You can clone the project with the following command. Please read the README in the project for specific instructions.

```bash
git clone git@github.com:OSCPU/yosys-sta.git
```

Try evaluating your digital circuit experiments with the above items.
:::
[yosys]: https://yosyshq.net/yosys

[nangate45]: https://mflowgen.readthedocs.io/en/latest/stdlib-freepdk45.html

[ista]: https://github.com/OSCC-Project/iEDA/tree/master/src/operation/iSTA

:::info[Limitations of open source EDA tools]
Of course, the above evaluation projects are not perfect. At least for now, they have the following shortcomings:

- The synthesis quality of the open source synthesizer yosys is not high. According to the evaluation work of the open source EDA team, for a certain RTL design, the standard unit area synthesized by yosys is 1.8 times that of the commercial synthesizer, and the circuit frequency synthesized by the commercial synthesizer is 153.8MHz. The circuit frequency synthesized by yosys is only 52MHz.
- nangate45 is a process library for academic research. The quantity and quality of standard units are also somewhat different from those of commercial process libraries.
- nangate45 cannot be used for tape-out, no factory uses it in the production line.

However, in the post-synthesis timing evaluation scenario, the above defects will not have a significant impact: even if the synthesis quality of yosys is not high, we can guide the direction of RTL optimization through the relative improvement of the synthesis results.
:::
<!-- -->

:::info[So do you still need FPGA to learn "One Student One Chip"?]
Basically no need:

- In terms of accuracy, Yosys' comprehensive process is geared towards ASIC design. Compared to the FPGA process, its principles and reporting accuracy are more suitable for "One Student One Chip".
- In terms of time, the main function of FPGA is simulation acceleration. That is to say, if the simulation task does not take a long time to complete, the advantage of using FPGA is not obvious. In fact, from the perspective of the simulation process, when the following inequality When established, the advantages of FPGA can be realized:
  ```
  FPGA_syn_time + FPGA_impl_time + FPGA_run_time < verilator_compile_time + verilator_run_time
  ```
  `FPGA_syn_time + FPGA_impl_time` usually reaches the order of hours, while `verilator_compile_time` can usually be completed within minutes. Therefore, only when `verilator_run_time` reaches the order of hours, the above inequality is possible. However, in the "One Student One Chip" learning, it is difficult for you Encounter simulation tasks that take hours to complete.
- In terms of debugging difficulty, FPGA debugging methods are very limited and can only capture the underlying waveform information under conditions of limited time and space; on the contrary, software simulation is much more flexible, and we can use many software methods to debug it from many aspects. Improve debugging efficiency.
:::
