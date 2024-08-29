---
sidebar_position: 3
---

# Single-cycle NPC (Non-Pipelined CPU) supporting RV32E

With a basic understanding of the runtime environment, you will know what kind of runtime environment to provide for NPC to support program execution.
Since the goal of Stage B is to establish a basic understanding of processor chips, we have downplayed performance metrics in Stage B.
Based on this, we can save chip fabrication costs by reducing the complexity of the design, allowing more designs from students to fit within the same area.
Therefore, currently, we have NPC adopting the RV32E instruction set.
As we progress to the later stages of Stage A, when launching Linux, we will gradually transition to the RV64IMAC instruction set.

It should be noted that while NEMU adopts RV32IM, which differs from NPC's use of RV32E, programs written for RV32E can run directly on a processor using the RV32IM instruction set. Therefore, as long as we ensure that the program has been compiled for RV32E, even if we use the RV32IM version of NEMU as the REF for DiffTest, it should function correctly.

:::tip[How to Modify RV64IM to RV32E?]
To modify RV64IM to RV32E, you need to perform the following steps:

- **NEMU**: You can change the `Base ISA` to `riscv32` by using `make menuconfig`,then implement RV32IM under `nemu/src/isa/riscv32`.
  Since some RV32 instructions have different semantics from RV64, it's recommended to re-implement them according to the manual to ensure a correct understanding of the instructions.
- **AM**: Supporting RV32E requires significant changes. We suggest you clone `abstract-machine` again, following these steps:
  1. Copy the `ysyx-workbench/abstract-machine` directory to another location.
  2. Delete the `ysyx-workbench/abstract-machine` directory.
  3. Modify the `ysyx-workbench/init.sh` file as follows:
     ```diff
     --- ysyx-workbench/init.sh
     +++ ysyx-workbench/init.sh
     @@ -45,4 +45,4 @@
        abstract-machine)
     -    init NJU-ProjectN/abstract-machine ysyx2204 abstract-machine true AM_HOME
     +    init NJU-ProjectN/abstract-machine ics2023 abstract-machine true AM_HOME
          init NJU-ProjectN/fceux-am ics2021 fceux-am false
          ;;
     ```
  4. Run `bash init.sh abstract-machine`.
  5. Refer to the `abstract-machine` copied to another directory to bring back the corresponding code.
  6. Delete the `abstract-machine` directory copied to another directory.
- NPC: Directly modify the RTL implementation.
:::
## Build a runtime environment for riscv32e-npc.

The AM project has provided the basic framework for RISC-V32E-NPC. You only need to execute the following command in the `am-kernels/tests/cpu-tests/` directory:

```bash
make ARCH=riscv32e-npc ALL=xxx
```

This will compile the test named `xxx` into the runtime environment of `riscv32e-npc`.
To familiarize ourselves with the process, let's first attempt to run a dummy program on NPC.

:::warning[Read NPC Program Execution Path from Command Line]
Next, we will continuously run various programs on NPC. It would be inefficient to recompile NPC every time we run a new program.
To improve efficiency, we can instruct the simulation environment to read the program's path from the command line, and then place the program content into the memory.
:::
<!-- -->

:::tip[Where is the Program? How to Load it into the Simulation Environment?]
If you're still uncertain about these aspects, it indicates that you may not have fully understood how NEMU reads programs before.
:::
<!-- -->

:::warning[Compile and Run AM Programs on NPC with One Command]
In the AM project, the Makefile does not provide a `run` target for `riscv32e-npc`.
Try to provide a `run` target for `riscv32e-npc` so that typing `make ARCH=riscv32e-npc ALL=xxx run` will compile the AM program and run it on NPC.
:::
To run the dummy program, NPC needs to implement some instructions. Specifically:

- `auipc` and `lui`: They belong to integer computation instructions. Consider how to share the same adder with `addi`.
- `jal` and `jalr`: They are unconditional jump instructions. After execution, the Program Counter (PC) will be modified. How should this be implemented?
- `sw`: This instruction requires memory access. However, for the dummy program, not implementing this `sw` instruction will not affect the program's execution.
  Therefore, you can implement it as a no-operation (NOP) instruction for now. We'll implement it correctly later on.

:::warning[If you are a beginner, try drawing the architecture diagram yourself.]
If you're new to processor design, try adding circuits for `auipc`, `lui`, `jal`, and `jalr` to the previous architecture diagram.
:::
<!-- -->

:::warning[Run the dummy Program on NPC]
Implement the instructions mentioned above so that NPC can run the dummy program.
However, currently, the `halt()` function in `riscv32e-npc` is an infinite loop.
You can check whether NPC successfully enters the `halt()` function by examining the waveform.
:::
<!-- -->

:::warning[Implement the `halt()` Function in `riscv32e-npc`]
To automatically end the program, you need to implement the `halt()` function in `riscv32e-npc`, where you add an `ebreak` instruction.
After this, when an AM program running on NPC finishes, it will execute the `ebreak` instruction, signaling the NPC's simulation environment to end the simulation.

Once implemented, you can run AM programs on NPC and automatically end the simulation with a single command.
:::
<!-- -->

:::warning[Implement HIT GOOD/BAD TRAP for NPC]
NEMU can output information about whether the program has successfully completed execution. Try implementing similar functionality in NPC.
This way, you'll be able to know whether the program has successfully ended on NPC in the future.
:::
## Build Infrastructure for NPC

Through the process of learning PA, you should realize the importance of infrastructure.
In PA, there are four main infrastructures: sdb, trace, native, and DiffTest.
Except for native, which belongs to AM, the other three infrastructures can be built in NPC.

:::danger[I can already see the waveform, why do I need these infrastructures?]
This is to prevent everyone from becoming mere tools, thus wasting life.

While waveforms indeed contain information about every signal in the circuit for each cycle, this information is too low-level. It cannot carry any higher-level semantics, which means users need to sift through this massive amount of information to find errors themselves.

In fact, errors caused by bugs manifest themselves at different abstraction levels. For example, a single signal error in RTL implementation might result in fetching the wrong instruction or accessing illegal memory during program execution, or returning to an incorrect position from a function call...
While you can eventually analyze these errors from the changing 0s and 1s in the waveform,
wouldn't it be better if you could directly identify the problem from the output of itrace/mtrace/ftrace?
Why waste so much time doing what these tools can already do well?
Moreover, if the bug is a software-level problem, isn't it troublesome to debug by looking at waveforms?

A scientific debugging process first requires an understanding of how programs run on computers.
Additionally, it requires an understanding of the strengths and weaknesses of various tools and selecting the right tools to analyze problems based on different scenarios.
From the perspective of abstraction layers in computer systems, we can observe program behavior at different levels:

Program -Module -Function -Instruction -Memory Access -Bus -Signal

The higher the level, the easier it is to understand behavior, but the details become more obscure.
On the other hand, the lower the level, the more precise the details, but the behavior becomes harder to understand.
Therefore, a scientific debugging method should:

- First, use the right software tools to help you quickly locate the approximate location where the bug occurred.
- Then, combine waveforms to conduct more granular diagnosis within a very small range to find the precise location of the bug.
:::
<!-- -->

:::warning[Build sdb for NPC]
You need to implement single-step execution, register printing, and memory scanning functionalities for NPC. 》 Expression evaluation and watchpoints are both based on printing registers and scanning memory.
Single-step execution and memory scanning are both straightforward to implement.
To print registers, you can access general-purpose registers using the C++ files compiled by Verilator, such as `top->rootp->NPC__DOT__isu__DOT__R_ext__DOT__Memory`. The specific C++ variable names are related to the module names and variable names in Verilog, which can be found by reading the compiled C++ header files.
:::
<!-- -->

:::warning[Add trace support to NPC]
You have already implemented itrace, mtrace, and ftrace in NEMU. Try implementing them in NPC.
Specifically, when implementing itrace, two points need to be noted:

- You need to obtain the currently executed instruction through DPI-C.
- You need to link the LLVM library. For details, you can refer to `nemu/src/utils/filelist.mk`.

Once you have obtained the currently executed instruction in the simulation environment, implementing ftrace should not be difficult. As for mtrace, since NPC does not yet support memory access instructions, we will implement it later.
:::
<!-- -->

:::warning[Add DiffTest support to NPC]
DiffTest is a powerful tool for processor debugging. Before implementing more instructions for NPC, setting up DiffTest for it is a wise choice.
Here, the Device Under Test (DUT) is NPC, while the Reference (REF) is NEMU. To achieve this, you need to:

- Implement the DiffTest API in `nemu/src/cpu/difftest/ref.c`, including `difftest_memcpy()`, `difftest_regcpy()`, and `difftest_exec()`. Additionally, `difftest_raise_intr()` is prepared for interrupts, which are not currently used.
- Select the shared library as the compilation target in NEMU's menuconfig:

```
Build target (Executable on Linux Native)  ---
  (X) Shared object (used as REF for differential testing)
```

- Recompile NEMU. After successful compilation, a dynamic library file `nemu/build/riscv32-nemu-interpreter-so` will be generated.
- Link the above dynamic library file in the simulation environment of NPC through dynamic linking, and implement the functionality of DiffTest through its API.You can refer to the relevant code in NEMU for details.

Try running the dummy program correctly in NPC with the DiffTest mechanism enabled.
To verify whether the DiffTest mechanism is effective, you can inject an error into the implementation of the `addi` instruction in NPC and observe if DiffTest can correctly report this error as expected.

Note that to compile NEMU back to ELF format, you also need to modify the compilation target in NEMU's menuconfig.
:::
<!-- -->

:::info[Can I choose Spike as REF?]
Considering that NEMU's implementation is simpler than Spike's, and everyone is more familiar with it, we still recommend prioritizing using your own NEMU as REF.
There will come a day when you need to add some personalized features to REF to help with debugging,
We don't want everyone to feel like they have no connection to the REF code.
Therefore, if you have the ability to read open source software code, you can use Spike as REF.
:::
## Implement RV32E Instruction Set

With these foundational infrastructures ready, you can conveniently implement more RV32E instructions in NPC. You've already implemented these instructions in NEMU, but implementing them in RTL requires focusing on some details:

- Arithmetic Instructions: The execution of these instructions is primarily handled by the ALU unit, which you have encountered in digital circuit experiments. Specifically,
  - Addition and Subtraction - You've already implemented two's complement addition when implementing the `addi` instruction earlier.
    Two's complement subtraction can be achieved through two's complement addition.
    In RISC-V, both addition and subtraction instructions do not require checking for carry and overflow.
  - Logical Operations - These are straightforward.
  - Shift Operations: These are also not difficult; you can directly implement them using operators.
  - Comparison Operations - These can be reduced to subtraction operations. The result of the subtraction operation is used to determine the result of the comparison operation.

:::info[How does hardware differentiate between signed and unsigned numbers?]
Try writing the following program:

```c
#include <stdint.h
int32_t fun1(int32_t a, int32_t b) { return a + b; }
uint32_t fun2(uint32_t a, uint32_t b) { return a + b; }
```

Then compile and examine the disassembly code:

```bash
riscv64-linux-gnu-gcc -c -march=rv32g -mabi=ilp32 -O2 test.c
riscv64-linux-gnu-objdump -d test.o
```

What are the differences between these two functions? Consider why this is the case.
:::
- Branch Instructions: Branch conditions can be calculated using subtraction operations in the ALU.
- Memory Access Instructions: Memory access instructions require accessing the memory. Unlike instruction fetching, memory access instructions may also involve writing data into memory.
  Our previous simplistic implementation of bringing the instruction fetch interface to the top level couldn't correctly handle memory access instructions.
  This is because the signals for memory access depend on the currently fetched instruction, which the simulation environment cannot handle correctly.
  To address this issue, we can implement memory access through the DPI-C mechanism:
  ```verilog
  import "DPI-C" function void pmem_read(
    input int raddr, output int rdata);
  import "DPI-C" function void pmem_write(
    input int waddr, input int wdata, input byte wmask);
  wire [63:0] rdata;
  always @(*) begin
    if (valid) begin // When there are read or write requests
      pmem_read(raddr, rdata);
      if (wen) begin // When there are write requests
        pmem_write(waddr, wdata, wmask);
      end
    end
    else begin
      rdata = 0;
    end
  end
  ```
  ```c
  extern "C" void pmem_read(int raddr, int *rdata) {
    // Always read 4 bytes aligned to the address `raddr & ~0x3u` and return to `rdata`
  }
  extern "C" void pmem_write(int waddr, int wdata, char wmask) {
    // Always write `wdata` according to the write mask `wmask` into 4 bytes aligned to the address `waddr & ~0x3u`
    // Each bit in `wmask` represents a mask for 1 byte in `wdata`
    // For example, `wmask = 0x3` means only write the lowest 2 bytes, leaving the other bytes in memory unchanged
  }
  ```
  These memory read and write functions simulate the behavior of a 32-bit bus: they only support read and write operations aligned to 4 bytes.
  Read operations always return data aligned to 4 bytes, which needs to be selected by the RTL code based on the read address.
  This setup ensures that minimal changes are required when implementing the bus in the future.
  You need to pass the correct parameters to these function calls in Verilog code and implement the functionality of these two functions in C++ code.
  For instruction fetching, you need to remove the previous implementation of bringing signals to the top level and instead call `pmem_read()` once additionally to implement it.

<!-- https://github.com/verilator/verilator/issues/2626 -->

:::warning[Add mtrace support for NPC]
After implementing memory access read and write functions through DPI-C, adding mtrace becomes straightforward.
:::
<!-- -->

:::warning[If you are a beginner, try drawing the architecture diagram yourself.]
Nowadays, companies all use Quartus/Vivado, so using Verilator for "RISC-V: Make Your Own CPU" is outdated.
:::
<!-- -->

:::warning[Observe the synthesis results of ALU]
Try using the `yosys-sta` project to synthesize the ALU, observe the synthesis results, and answer the following questions:

1. We know that two's complement subtraction can be implemented using an adder,and comparison instructions and branch instructions essentially require two's complement subtraction.
   If we directly write `-` or `<` operators in RTL code,
   can yosys automatically merge their subtraction functionality into the same adder?
2. What circuit does yosys synthesize for the shift operators `<<` and `>>`?
3. Is there room for improvement when yosys synthesizes circuits directly from operators?

hint: If you find it difficult to read the synthesis results for 32-bit data, consider observing and analyzing the synthesis results for 16-bit, 8-bit, or even 4-bit data first.
:::
<!-- -->

:::warning[Ensure all cpu-tests run correctly in NPC]
With the strong support of the infrastructure in place, you should be able to easily implement RV32E support in NPC and ensure that all cpu-tests run correctly.
:::
<!-- -->

:::info[How does NPC correctly execute C programs containing multiplication and division operations if RV32E does not include multiply and divide instructions?]
This is because the RISC-V instruction set is modular. GCC can determine how to compile multiplication and division operations based on whether the instruction set includes the M extension.
If the instruction set does not include the M extension, GCC will compile multiplication and division operations into function calls such as `__mulsi3()`.
These functions provide software simulation versions of integer arithmetic operations, computing multiplication and division results using addition and subtraction operations.
The declarations of these functions can be found on [this page][libgcc]. Their function bodies reside in the libgcc library, which is typically linked into the ELF executable during the linking process.

We have ported some common integer multiplication and division operations corresponding to software simulation functions from libgcc to `riscv32e-npc`.
Therefore, ELF executables can be compiled without multiply and divide instructions while still correctly performing multiplication and division operations.
:::
[libgcc]: https://gcc.gnu.org/onlinedocs/gccint/Integer-library-routines.html

:::danger[Liberate Your Thinking, Use the Right Tools for the Job]
Some students have raised the question: why bother with tools like Verilator and Makefile when you can simply click a button in ModelSim?
This is because relying solely on waveform debugging is not a scientific approach.
For small-scale programs like `cpu-tests`, you might survive with waveform debugging, but as programs grow larger, debugging efficiency decreases.
If an error occurs after simulating one hundred million cycles, how will you find the error in the waveform?

However, most students haven't thought about improving debugging efficiency.
It's not because they lack the ability (for example, tracing is essentially a `printf()` statement), but rather because of various unprofessional ideas:

- My major is not computer science, so software isn't relevant to me.
- I'm here to work on hardware, so I can just gloss over the software part.
- Nowadays, companies all use Quartus/Vivado, so using Verilator for "One Student One Chip" is outdated.

These ideas instinctively deter people from engaging with software concepts.
For instance, in the NSCSCC (National Student Computer System Capability Challenge), successfully booting Linux is the pinnacle achievement of the demonstration phase. However, not every participating team manages to reach this pinnacle.
But we believe that everyone can successfully boot Linux on their own designed CPU within a reasonable timeframe, as long as they learn to use the right tools. For example, in the third session of "RISC-V: Make Your Own CPU," which lasted three months, there was a student from the electronics department who had never designed a CPU before,
yet single-handedly managed to boot Linux Debian on their CPU.
In fact, even writing a small script can significantly improve your work efficiency at times.
Understanding, borrowing, and assimilating advanced methods from other fields can make you more powerful compared to sticking to traditional methods.
:::
<!-- -->

:::tip[If you are a beginner, now is a good time to look at the architecture diagram in the textbook]
If you are a beginner in processor design, try comparing the architecture diagram of the single-cycle processor you've drawn with the architecture diagram in the textbook. Consider the similarities and differences between the two.
Reflect on which architecture is better or worse and why.
:::