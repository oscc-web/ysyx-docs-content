---
sidebar_position: 4
---

# Build a verilator simulation environment

verilator is an open source verilog simulation tool, in the "One Student One Chip" project, you will use it to carry out RTL functional simulation, so as to verify your RTL code.

The framework code provides an `npc` directory by default, where `npc` stands for `New Processor Core`, the directory where you will design your own processors. However, in order to set an environment variable `NPC_HOME`, you need to run the following command:

> ```bash
> cd ysyx-workbench
> bash init.sh npc
> ```

This environment variable will be used in the future. The `npc` directory contains a few simple files:

```
ysyx-workbench/npc
├── csrc
│   └── main.cpp
├── Makefile
└── vsrc
    └── example.v
```

Currently these three files are almost empty, in this chapter, we will guide you to set up the verilator simulation environment, and write two simple digital circuit modules for simulation.

:::danger[It doesn't even have a simulation frame. It's a shame.]
The reason why we set up this part of the experiment is to let you know that <Highlight color="#c40e0e">all the details of the project are relevant to you.</Highlight>.

In the previous course labs, it was not uncommon for people to think that the framework was supposed to be provided by the TA, and that all you had to do was to write the code in the designated places, and that the rest of the code/files were extraneous, and that you didn't need to care about them. In fact, this kind of lab is <Highlight color="#c40e0e">very dangerous</Highlight>, not only will it not train you to be a real professional, but it will also prevent you from surviving in a real project:

1. when you encounter a systematic bug, you will not be able to find it, because you will not even be able to understand the module that calls your code, not to mention you will not be able to clearly understand the whole project structure and every detail of it.
2. away from the handouts, you can not do anything, because you are always waiting for others like these handouts clearly tell you what to do next how to do, rather than stand in the project's point of view to actually analyze what should be done now!

A very realistic scenario is, when you go to a company or join a project team, there will be no more handouts and framework code to take care of you, your boss will say "try verilator", you have to run verilator by yourself, write a report on how to use it, and present your work to your boss in next week's team meeting.

Therefore, we want to provide you with a more realistic training: give you a goal, let you learn to break it down, and use your own skills to reach that goal step by step. Building a verilator simulation framework is a very achievable goal, so it's appropriate to use it as a training exercise to test the skills.
:::
:::tip[If you want to use Chisel]
Please run the following command:

```bash
cd ysyx-workbench
bash init.sh npc-chisel
```

The above command will replace the files in the `npc` directory with a Chisel development environment, as described in `README.md`.

This chapter focuses on the use of verilator, even if you want to develop with Chisel, we recommend that you follow the handout and walk through the process using verilog.
:::
## STFW + RTFM

Without further hesitation, let's get started.

:::warning[Getting to know verilator]
You have probably heard of verilator for the first time, and that's normal. It's normal to want to learn more about verilator, and it's normal to want to know more about it. But if your first reaction is to ask someone, that's not appropriate. In fact, verilator is such a well-known tool in the simulation field that you can easily search for it on the Internet. You need to find the official website via STFW and read the introduction.
:::
After finding the official website and reading about it, the next step is to run it. But before we can do that, we need to install it.

:::warning[Installation of verilator]
Find the steps for installing verilator on the official website, and follow the steps for installing from git. The reason we don't use `apt-get` is because it is an older version. Also, in order to standardize the version, you need to install `5.008` from git. To do this, you'll also need to do some simple git work, and if you're not up to speed on this, you may want to look for some git tutorials to learn how to do this. It is also a good idea to do this in a directory other than `ysyx-workbench/`, otherwise git will track down verilator's source code and take up unnecessary disk space.

After successful installation, run the following command to check if the installation was successful and if the version is correct.

```bash
verilator --version
```
:::
<!-- -->

:::warning[Run Samples]
The verilator manual contains a C++ sample, which you need to find in the manual and follow the steps of the setup process.
:::
## Example: Dual Control Switch

The example in the manual is so simple that it is not even a real circuit module. Let's write a real circuit module, a dual control switch, to test it. Write the following verilog code:

```verilog
module top(
  input a,
  input b,
  output f
);
  assign f = a ^ b;
endmodule
```

One application of the dual control switch is the joint control of the same light (`f`) by two switches (`a` and `b`). Unlike the example in the manual, this module has input and output ports. In order to drive the input ports and get the results from the output ports, we need to modify the `while` loop in the C++ file:

```c
// The following is pseudo-code

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

while (???) {
  int a = rand() & 1;
  int b = rand() & 1;
  top->a = a;
  top->b = b;
  top->eval();
  printf("a = %d, b = %d, f = %d\n", a, b, top->f);
  assert(top->f == (a ^ b));
}
```

In a loop, the code will generate two random 1-bit signals to drive the two input ports, and then update the state of the circuit with the `eval()` function, so that we can read the value of the output port and print it. To automatically check that the result is correct, we check the output with an `assert()` statement.

:::warning[Simulation of a dual-control switch module]
Try to simulate the dual switch module in verilator. Since the top-level module name is different from the manual sample, you will need to make some changes to the C++ file accordingly. Also, this project does not have an end-of-simulation statement, so in order to exit the simulation, you need to type `Ctrl+C`.
:::
<!-- -->

:::tip[What does the above code mean?]
If you don't know what to change, you're not familiar with C programming, and you should go back to the previous chapter to review the C language.
:::
<!-- -->

:::warning[Understanding the behavior of RTL simulation]
Read the C++ code compiled by the verilator, and then, in conjunction with the verilog code, try to understand what happens when the simulator performs a simulation.
:::
## Print and view waveforms

Viewing waveform files is one of the most common methods of RTL debugging. Verilator supports waveform generation, and you can view waveforms with the open source waveform viewer GTKWave.

:::warning[Generate and view waveforms]
The verilator manual already describes the method of waveform generation, you need to read the manual to find the relevant content, and then follow the steps in the manual to generate a waveform file, and run the following command:

```bash
apt-get install gtkwave
```

to install GTKWave to view waveforms.
:::
<!-- -->

:::tip[There's so much in the manual, how do I find it?]
Try typing `Ctrl+F`.
:::
<!-- -->

:::danger[Do not generate waveforms for long periods of time]
Waveform files generally take up a lot of disk space, and generating waveforms for a long time may lead to running out of disk space, which may cause the system to crash.
:::
## Write a makefile

:::warning[One-Click Simulation]
It is inconvenient to type the compile command repeatedly, try to write a rule `sim` for `npc/Makefile` to achieve one-click simulation, e.g. type `make sim` to carry out the above simulation.
:::
<!-- -->

:::danger[Be careful to keep the git trace commands]
The framework code already provides a default `sim` rule in `npc/Makefile`, which already contains the command `$(call git_commit, "sim RTL")` for git tracking, be careful not to change this command when writing the Makefile, otherwise it will affect the development tracking functionality, which is the most important basis for documenting the originality of the `One Student One Chip` results. This is an important basis for documenting the originality of the "One Student One Chip" results. So after writing the Makefile and running it, you also need to make sure that git is tracking the simulation correctly.
:::
## Connecting to the nvboard

[NVBoard][nvboard]\(NJU Virtual Board) is developed by Nanjing University, used to teach the virtual FPGA board project, it can provide a virtual board interface in the RTL simulation environment, support for dip switches, LED lights, VGA display and other functions, in the case of no perf requirement it can replace the real FPGA board (after all, not everyone around an FPGA on hand). Get the code of NVBoard by running the following commands.

```bash
cd ysyx-workbench
bash init.sh nvboard
```

[nvboard]: https://github.com/NJU-ProjectN/nvboard.git

:::warning[Run the NVBoard example]
Read the introduction to the NVBoard project and try to run the examples provided in the NVBoard project.
:::
<!-- -->

:::tip[Not sure how NVBoard works?]
Try starting with the `make` command and see how it all works. You have enough background to understand how NVBoard works, including the use of Makefiles, and the basic use of classes in C and C++. Now try to read the code (Makefiles are also code) and see how the verilog top-level ports, constraints, and NVBoard are connected in the examples.
:::
<!-- -->

:::warning[Dual control switching on NVBoard]
Read the description of the NVBoard project, modify your C++ file based off of the C++ sample and Makefile, assign pins to the inputs and outputs of the dual control switches, and modify the `npc/Makefile` to connect to NVBoard.
:::
<!-- -->

:::info[The NVBoard Story]
Although NVBoard is a teaching program at Nanjing University, it has a special connection with the participants of "One Student One Chip": there are two special students in the third "One Student One Chip" flow list, they were only freshmen when they enrolled in the program, and one of them, sjr, is the first author of NVBoard.

In fact, it was sjr's independent problem-solving skills and self-confidence that he developed during his participation in "One Student One Chip" helped him to successfully develop the NVBoard project. Now the NVBoard program is helping "One Student One Chip" to improve the learning outcomes. NVBoard carries not only the function of virtual FPGA boards, but also the independent problem solving concept that "One Student One Chip" upholds.

These are not far away from you, when you are willing to learn on your own and no longer wait for others to give you the answer, your future will be full of unlimited possibilities.
:::
## Example: LED Blinking

(If that sample code is difficult to understand, you can do the [Digital Circuit Fundamentals lab](DigitalCircuitBasicExperiment.md)!)

LED blinking is a group of LEDs that turn on and off sequentially, the following is a reference implementation of LED blinking.

```verilog
module light(
  input clk,
  input rst,
  output reg [15:0] led
);
  reg [31:0] count;
  always @(posedge clk) begin
    if (rst) begin led <= 1; count <= 0; end
    else begin
      if (count == 0) led <= {led[14:0], led[15]};
      count <= (count >= 5000000 ? 32'b0 : count + 1);
    end
  end
endmodule
```

Each bit of the output signal led corresponds to one led of the virtual FPGA board. Since the code contains sequential logic components that need to be reset, we need to modify the verilator's simulation code as follows:

```c
// The following is pseudo-code

void single_cycle() {
  top->clk = 0; top->eval();
  top->clk = 1; top->eval();
}

void reset(int n) {
  top->rst = 1;
  while (n -- > 0) single_cycle();
  top->rst = 0;
}

...
reset(10);  // 复位10个周期
while(???) {
  ...
  single_cycle();
  ...
}
```

:::warning[Connecting LED blinking to the NVBoard]
Write a LED Blinking module, then connect it to the NVBoard and assign the pins. If your implementation is correct, you will see the lights turn on and off sequentially from the right end to the left end.
:::
<!-- -->

:::warning[Understanding the behavior of RTL simulation (2)]
Read the C++ code compiled by verilator, and then combine it with the verilog code to try to understand how the simulator simulates a sequential logic circuit.
:::
:::info[verilator advanced learning]
[Please click here](https://www.itsembedded.com/)
:::
