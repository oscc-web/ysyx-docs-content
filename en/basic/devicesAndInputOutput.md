---
sidebar_position: 5
---

# Devices and Input/Output

You've already implemented TRM on both NEMU and NPC. The next step, of course, is to make them support input/output.

:::warning[Implement input/output in NEMU]
Follow the PA lecture notes to complete Phase 3 of PA2 until you see the following prompt:

#### flag::hint

PA2 ends here...
:::
## Input/Output in NPC

For the RISC-V architecture, input/output is implemented through MMIO.
With the memory access read and write functions based on DPI-C, we can now implement input/output in NPC without modifying the RTL code!
We just need to perform simple address range checks in these two functions to redirect memory access requests from NPC to the correct devices.
MMIO in hardware is implemented based on a bus, and we will implement true MMIO later.

Regarding devices, we are not directly using NEMU's device model here. Instead, we are implementing a device model for NPC in the simulation environment that resembles the future SoC for chip fabrication.
Once we implement the bus, we will then implement RTL versions of the devices based on the bus.
At this point, the role of IOE abstraction in the abstract machine (AM) becomes apparent: the device addresses and device models for NEMU and NPC are different, but after abstraction, they can both run the same Nintendo Entertainment System (NES) emulator source code.
Furthermore, all programs on the AM do not need to be written differently for different execution environments.

## Running Super Mario in NPC

Now we have completed NEMU with support for RV32IM and peripherals, and successfully run Super Mario on NEMU. Similarly, we can also run Super Mario on NPC with RV32E, but this first requires implementing UART and a clock.

We know that RISC-V processors access peripherals through MMIO. For example, in NEMU, the UART is mapped to `0xa00003f8`.
Similarly, we can implement simple UART and a clock in NPC's simulation environment.
As mentioned in the previous section, we use DPI-C to allow NPC to call read and write functions `pmem_read()` and `pmem_write()` to access memory.
Similar to NEMU, we can add several checks in these two functions to implement MMIO functionality. Pseudocode is shown below:

```c
extern "C" void pmem_read(int raddr, int *rdata) {
  // Always read 4 bytes from address `raddr & ~0x3u` and return to `rdata`
  if (raddr == clock_address) { return current_time; }
  ...
}

extern "C" void pmem_write(int waddr, int wdata, char wmask) {
  // Always write to address `waddr & ~0x3u` according to write mask `wmask`
  // Each bit in `wmask` represents a byte in `wdata`,
  // For example, `wmask = 0x3` means only write the lowest 2 bytes, leaving other bytes in memory unchanged.
  if (waddr == uart_address) { putchar(...); }
  ...
}
```

After implementing the UART and clock, you can run the corresponding AM programs for testing and try running the character version of Super Mario on NPC.

:::warning[Add UART and Clock to NPC]
- Implement UART output functionality in NPC's simulation environment and run the hello program.
- Implement a clock in NPC's simulation environment and run the `real-time clock test` from `am-tests`. You can implement the clock functionality based on system time.As for the C libraries related to systemS time and how to retrieve system time, we leave it to you to STFW.
- Run the character version of the NES emulator.
:::
If you're interested, you can also mimic NEMU's VGA implementation and run the graphical version of Super Mario on NPC.

<!-- -->

:::info[Run the graphical version of Super Mario]
- Implement VGA peripheral in NPC's simulation environment and run the video test.
- Run the graphical version of the NES emulator.
:::