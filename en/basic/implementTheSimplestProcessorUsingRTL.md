---
sidebar_position: 3
---

# Implement the simplest processor using RTL

By implementing NEMU, you've gained a conceptual understanding of how processors are structured and roughly how they operate.
Now, let's attempt to implement the simplest processor using RTL code.
As mentioned in the pre-learning stage, we'll collectively refer to the processor you design as NPC (New Processor Core, though of course, you're welcome to give your processor a more personalized name).

## Basic Architecture of the Processor

Specifically, you will need to implement the components mentioned in TRM from PA1 using RTL:

- PC - Actually a counter that increments by "1," where "1" represents the length of one instruction.
- Registers - Referring to General Purpose Registers (GPR), usually consisting of a set of registers. Particularly, the value read from register 0 is always 0.
- Adder - This is straightforward.
- Memory - Just like a writable/readable "large array."

In fact, you have already learned how to implement them using RTL in digital circuit experiments. We can divide the RTL project into modules according to the processor's operation: Instruction Fetch, Decode, Execute, and PC Update.
More in details:

- IFU (Instruction Fetch Unit): Responsible for fetching an instruction from memory based on the current PC.
- IDU (Instruction Decode Unit): Responsible for decoding the current instruction, preparing the data and control signals needed for the execution stage.
- EXU (Execution Unit): Responsible for executing operations on data based on control signals and writing the execution result back to registers or memory.
- PC Update: When implementing it through RTL, this operation is generally implemented along with the PC register, so there is no need to separate it into an independent module.

As for where to place the above components in which module, everyone can decide for themselves and delineate the interfaces between modules. One exception is the memory. For ease of testing, we won't implement the memory using RTL but instead use C++ to implement it. Therefore, we need to pull the signals for memory access interfaces to the top level, and access the memory through C++ code:

```c
while (???) {
  ...
  top->inst = pmem_read(top->pc);
  top->eval();
  ...
}
```

You can easily implement a simple memory using C++ code.

## Several Code Styles and Standards

In previous phases of the "One Student One Chip" initiative, we have found that certain non-standard code styles can bring about additional issues during the later stages of SoC integration.
To avoid impacting the progress of SoC integration in the future, we recommend that everyone adhere to the following code standards.

:::danger[1. If you are a beginner, do not use behavioral modeling.

In fact, the digital circuit experiment manual at Nanjing University also mentions that "behavioral modeling is not conducive for beginners to establish circuit thinking." Here's the relevant excerpt we're citing:]
#### caution::It is strongly recommended that beginners avoid using behavioral modeling to design circuits

Verilog was not originally introduced for synthesizable circuit design; its essence lies in being a circuit modeling language based on an event queue model.
Therefore, behavioral modeling can easily lead beginners away from the original intention of describing circuits:
Developers need to look at circuit diagrams, imagine the behavior of circuits, and then transform their thinking into the event queue model.
Finally, use behavioral modeling to describe the behavior of circuits, and synthesizers derive corresponding circuits based on such descriptions.
From this process, it is not only unnecessary but also prone to introducing errors:

- If developers already have a circuit diagram in mind, directly describing it is the most convenient option.
- If developers already have a circuit diagram in mind and their understanding of behavioral modeling is flawed, they may adopt an incorrect way of describing it, resulting in unintended circuits.
- If developers do not have a circuit diagram in mind and expect the synthesizer to generate a circuit with certain behaviors through behavioral modeling, this deviates from the essence of "describing circuits."Most students easily make this mistake, treating behavioral modeling as procedural C language, attempting to map arbitrary complex behaviors to circuits, and ultimately, the synthesizer will only generate low-quality circuits with large delays, areas, and power consumption.

Therefore, until everyone masters the thinking of "describing circuits" and is not misled by behavioral modeling,
We strongly advise beginners to stay away from behavioral modeling and directly describe circuits only through data flow modeling and structural modeling.
For example, the above statements about if and always are correct to some extent,
but the following questions can help you test whether you have mastered the essence of Verilog:

- What is the precise meaning of "execution" in hardware description languages?
- Who executes Verilog statements? Is it the circuit, the synthesizer, or something else?
- When the condition of if is met, the statements after else are not executed. What does "not executed" mean here? And how is it related to describing circuits?
- There are "concurrent execution," "sequential execution," "immediate execution when any variable changes," and "execution under any circumstances." How are they reflected in designed circuits?

If you cannot provide clear answers to these questions, we strongly advise against using behavioral modeling.
If you truly want to understand them, you need to read the [Verilog standard manual](https://inst.eecs.berkeley.edu/~cs150/fa06/Labs/verilog-ieee.pdf).
:::
<!-- -->

:::danger[True Circuit Description = Instantiation + Interconnection]
Forgetting behavioral modeling makes it easy to return to the simple essence of describing circuits.
Imagine you have a circuit schematic in your hand. If you need to describe the contents of the schematic to someone else, how would you do it?
You would probably say something like "there is a component/module A, its x pin is connected to another component/module B's y pin," because that's the most natural way to describe a circuit.
Designing circuits with HDL is simply describing the circuit schematic with HDL. Whatever is on the schematic, describe it directly.
So, describing circuits with HDL involves doing just two things:

- Instantiation: Placing a component/module on the circuit board, which can be a gate circuit or a module composed of gate circuits.
- Interconnection: Connecting the pins of components/modules correctly with wires.

You can see how data flow modeling and structural modeling embody these two actions,
while behavioral modeling complicates these two simple tasks.
:::
Therefore, we do not recommend beginners to write any `always` statements in Verilog code. To facilitate the use of flip-flops and multiplexers, we provide the following Verilog templates for everyone to use:

```verilog
// Trigger template
module Reg #(WIDTH = 1, RESET_VAL = 0) (
  input clk,
  input rst,
  input [WIDTH-1:0] din,
  output reg [WIDTH-1:0] dout,
  input wen
);
  always @(posedge clk) begin
    if (rst) dout <= RESET_VAL;
    else if (wen) dout <= din;
  end
endmodule

// Example of using trigger template
module example(
  input clk,
  input rst,
  input [3:0] in,
  output [3:0] out
);
  // The bit width is 1 bit, the reset value is 1'b1, and the write enable is always valid.
  Reg #(1, 1'b1) i0 (clk, rst, in[0], out[0], 1'b1);
  // The bit width is 3 bits, the reset value is 3'b0, and the write enable is out[0]
  Reg #(3, 3'b0) i1 (clk, rst, in[3:1], out[3:1], out[0]);
endmodule
```

```verilog
// The internal implementation of the Multiplexer template.
module MuxKeyInternal #(NR_KEY = 2, KEY_LEN = 1, DATA_LEN = 1, HAS_DEFAULT = 0) (
  output reg [DATA_LEN-1:0] out,
  input [KEY_LEN-1:0] key,
  input [DATA_LEN-1:0] default_out,
  input [NR_KEY*(KEY_LEN + DATA_LEN)-1:0] lut
);

  localparam PAIR_LEN = KEY_LEN + DATA_LEN;
  wire [PAIR_LEN-1:0] pair_list [NR_KEY-1:0];
  wire [KEY_LEN-1:0] key_list [NR_KEY-1:0];
  wire [DATA_LEN-1:0] data_list [NR_KEY-1:0];

  generate
    for (genvar n = 0; n < NR_KEY; n = n + 1) begin
      assign pair_list[n] = lut[PAIR_LEN*(n+1)-1 : PAIR_LEN*n];
      assign data_list[n] = pair_list[n][DATA_LEN-1:0];
      assign key_list[n]  = pair_list[n][PAIR_LEN-1:DATA_LEN];
    end
  endgenerate

  reg [DATA_LEN-1 : 0] lut_out;
  reg hit;
  integer i;
  always @(*) begin
    lut_out = 0;
    hit = 0;
    for (i = 0; i < NR_KEY; i = i + 1) begin
      lut_out = lut_out | ({DATA_LEN{key == key_list[i]}} & data_list[i]);
      hit = hit | (key == key_list[i]);
    end
    if (!HAS_DEFAULT) out = lut_out;
    else out = (hit ? lut_out : default_out);
  end
endmodule

// The Multiplexer template without default value.
module MuxKey #(NR_KEY = 2, KEY_LEN = 1, DATA_LEN = 1) (
  output [DATA_LEN-1:0] out,
  input [KEY_LEN-1:0] key,
  input [NR_KEY*(KEY_LEN + DATA_LEN)-1:0] lut
);
  MuxKeyInternal #(NR_KEY, KEY_LEN, DATA_LEN, 0) i0 (out, key, {DATA_LEN{1'b0}}, lut);
endmodule

// The Multiplexer template with default value.
module MuxKeyWithDefault #(NR_KEY = 2, KEY_LEN = 1, DATA_LEN = 1) (
  output [DATA_LEN-1:0] out,
  input [KEY_LEN-1:0] key,
  input [DATA_LEN-1:0] default_out,
  input [NR_KEY*(KEY_LEN + DATA_LEN)-1:0] lut
);
  MuxKeyInternal #(NR_KEY, KEY_LEN, DATA_LEN, 1) i0 (out, key, default_out, lut);
endmodule
```

The `MuxKey` module implements the "key-based selection" functionality, where, in a list `lut` of `(key, data)` pairs, the `out` is set to the data matching the given key `key`. If there is no data with a key equal to `key` in the list, `out` is set to `0`. Particularly, the `MuxKeyWithDefault` module can provide a default value `default_out`. When there is no data with a key equal to `key` in the list, `out` is set to `default_out`. When instantiating these two modules, the following two points should be noted:

- The user needs to provide three parameters: the number of key-value pairs `NR_KEY`, the bit width of the key `KEY_LEN`, and the bit width of the data `DATA_LEN`. It is essential to ensure that the signal widths of the ports match the provided parameters; otherwise, incorrect results will be output.
- If there are multiple data with a key equal to `key` in the list, the value of `out` is undefined, and the user needs to ensure that the keys in the list are all distinct.

The implementation of the `MuxKeyInternal` module uses many advanced features such as `generate` and `for` loops. It also utilizes behavioral modeling for ease of writing. However, we won't delve into these details here. Through the abstraction of structural modeling, users can ignore these details.

The following code uses the selector template to implement a 2-to-1 multiplexer and a 4-to-1 multiplexer respectively:

```verilog
module mux21(a,b,s,y);
  input   a,b,s;
  output  y;

  // Implement the following always block using MuxKey:
  // always @(*) begin
  //  case (s)
  //    1'b0: y = a;
  //    1'b1: y = b;
  //  endcase
  // end
  MuxKey #(2, 1, 1) i0 (y, s, {
    1'b0, a,
    1'b1, b
  });
endmodule

module mux41(a,s,y);
  input  [3:0] a;
  input  [1:0] s;
  output y;

  // Implement the following always block using MuxKeyWithDefault:
  // always @(*) begin
  //  case (s)
  //    2'b00: y = a[0];
  //    2'b01: y = a[1];
  //    2'b10: y = a[2];
  //    2'b11: y = a[3];
  //    default: y = 1'b0;
  //  endcase
  // end
  MuxKeyWithDefault #(4, 2, 1) i0 (y, s, 1'b0, {
    2'b00, a[0],
    2'b01, a[1],
    2'b10, a[2],
    2'b11, a[3]
  });
endmodule
```

:::info[If you are using Chisel, we also advise against using `when` and `switch` statements.]
In Chisel, the semantics of `when` and `switch` are very similar to Verilog's behavioral modeling, so it's not recommended for beginners to use them.
Instead, you can use library functions like `MuxOH` to implement selector functionality. For more details, refer to Chisel documentation.
:::
<!-- -->

:::danger[2. If you insist on using Verilog's behavioral modeling, avoid using `negedge`.]
Mixing `posedge` and `negedge` can make timing convergence more difficult and increase the difficulty of backend physical implementation.
If you are unsure how to maintain good timing while mixing the two, we recommend using only `posedge`.
Otherwise, if your processor significantly affects the overall timing of the SoC, and in tight timing situations during chip fabrication,
the "One Student, One Chip" project team will remove your processor from the batch's chip fabrication list.

If you use the above Verilog templates provided by us or use Chisel, you don't need to worry about this issue.
:::
<!-- -->

:::danger[3. If you insist on using Verilog's behavioral modeling, avoid using asynchronous reset.]
Using asynchronous reset can lead to metastability issues, causing the chip to fail to function correctly after reset.
Generally, the technique of using `asynchronous reset, synchronous release` is employed to address this problem.
If you are unsure how to use this technique, we recommend using only synchronous reset (i.e., the reset signal does not appear in the event list of `always` blocks).
Otherwise, the "One Student, One Chip" project team cannot guarantee that your processor will function correctly after chip fabrication.

If you use the above Verilog templates provided by us or use Chisel, you don't need to worry about this issue.
:::
<!-- -->

:::danger[4. If you insist on using Verilog's behavioral modeling, avoid using latches.]
Latches' behavior is not clock-driven, making it difficult for timing analysis tools to analyze them.
If you are unsure how to avoid latches, we recommend not using behavioral modeling.

If you use the above Verilog templates provided by us or use Chisel, you don't need to worry about this issue.
:::
<!-- -->

:::danger[5. It is necessary to add a student ID prefix before the module name.]
For example, `module IFU` needs to be modified to `module ysyx_22040000_IFU`.
This is because when everyone integrates their own processors into the SoC, modules with the same name will cause the tools to report errors of duplicate definitions.

If you use Chisel, we will provide a FIRRTL transform in the future to automatically add the prefix.
Currently, you don't need to add a student ID prefix before the module name when writing your code.
:::
<!-- -->

:::danger[6. If you are using Verilog, it is necessary to add a student ID prefix before the identifiers in macro definitions.]
For example, `` `define SIZE 5 `` needs to be modified to `` `define ysyx_22040000_SIZE 5 ``.
This is because when everyone integrates their own processors into the SoC, macros with the same name will cause the tools to report errors of duplicate definitions.

If you use Chisel, you don't need to worry about this issue.
:::
## Implement the First Instruction in NPC

Next, we will implement the simplest instruction: `addi`.
In NEMU, you already understand how this instruction is executed. Now, you need to implement it using RTL.

:::warning[If you are a beginner, try drawing the architecture diagram yourself.]
If you are new to processor design, try drawing the architecture diagram of a single-cycle processor that supports only the `addi` instruction.
:::
<!-- -->

:::info[Training to solve unknown problems independently]
In fact, the solution to a single-cycle processor is very mature, to the extent that you can find very detailed architecture diagrams in most textbooks.
The reason we don't provide an architecture diagram in the lecture notes is to present a mature problem as an "unknown" problem for beginners,
allowing beginners to solve this "unknown" problem through their own thinking.
This kind of training is very similar to the process of solving real problems in the future,
so when you find the answer to a problem directly from a textbook, you miss another opportunity to train yourself.
:::
<!-- -->

:::warning[Implement the addi instruction in NPC]
Specifically, you need to consider the following:

- Set the reset value of the PC to `0x80000000`.
- Place the binary encoding of several `addi` instructions in memory (you can utilize the behavior of register 0 to write behavior-determined instructions).
- Since jump instructions are not implemented yet, NPC can only execute sequentially. You can stop the simulation after NPC executes several instructions.
- You can check whether the `addi` instruction is executed correctly by viewing the waveform or printing the state of general-purpose registers in the RTL code.
- Regarding the general-purpose registers, you need to think about how to implement the feature of register 0. Furthermore, to avoid students who choose Verilog from writing less reasonable behavioral modeling code, we provide the following incomplete code for everyone to complete (you don't need to change the contents of the `always` block):

```verilog
module RegisterFile #(ADDR_WIDTH = 1, DATA_WIDTH = 1) (
  input clk,
  input [DATA_WIDTH-1:0] wdata,
  input [ADDR_WIDTH-1:0] waddr,
  input wen
);
  reg [DATA_WIDTH-1:0] rf [2**ADDR_WIDTH-1:0];
  always @(posedge clk) begin
    if (wen) rf[waddr] <= wdata;
  end
endmodule
```

- Using NVBoard requires better support for devices in RTL code, which will be introduced later. There is no need to connect to NVBoard for now.
:::
<!-- -->

:::tip[Don't know where to start?]
You might encounter the following questions:

- How to access memory correctly based on the PC value?
- How to place `addi` instructions in memory?
- How to end simulation after executing a certain number of instructions?
- How should the ports of the general-purpose register module be designed?

During the pre-learning stage when setting up the Verilator framework, we have already reminded you: <Highlight color="#c40e0e">Every detail in the project matters to you</Highlight>.
Whenever you feel stuck, it's likely reminding you that there might be something you didn't do well in your previous learning.
Instead of asking your peers, you should review the previous lab materials and make your best effort to understand every detail, thus finding the answers to the above questions.
:::
## Let the Program Decide When Simulation Ends

Previously, we let the simulation environment (C++ code) determine when to end the simulation after executing a certain number of instructions. Obviously, this approach is not very versatile: you need to know in advance how many instructions a program will execute. Is there a way to automatically end the simulation when the program finishes executing?

In fact, NEMU has already provided a good solution: the trap instruction. NEMU implements a special `nemutrap` instruction, which indicates the end of the client program. Specifically, in RISC-V, NEMU chooses the `ebreak` instruction to act as the `nemutrap` instruction. In NPC, we can also implement similar functionality: if the program executes the `ebreak` instruction, notify the simulation environment to end the simulation.

Implementing this functionality is not difficult. First, you need to add support for the `ebreak` instruction in NPC. However, to allow NPC to notify the simulation environment when executing the `ebreak` instruction, you also need to implement an interaction mechanism between RTL code and C++ code. We will use the DPI-C mechanism in SystemVerilog to achieve this interaction.

:::warning[Try DPI-C Mechanism]
Read the Verilator manual to find the relevant content about the DPI-C mechanism, and try running the examples provided in the manual.
:::
<!-- -->

:::warning[Implement ebreak via DPI-C]
Utilize the DPI-C mechanism in RTL code to notify the simulation environment to end simulation when NPC executes the `ebreak` instruction.
Once implemented, place an `ebreak` instruction in memory for testing purposes.
If your implementation is correct, the simulation environment no longer needs to worry about when the program ends simulation; it just needs to continue simulation until the program executes the `ebreak` instruction.

If you are using Chisel, you can utilize the BlackBox mechanism to call Verilog code and then let the Verilog code interact with the simulation environment through the DPI-C mechanism.
Please refer to relevant documentation for how to use BlackBox.
:::