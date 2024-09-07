---
sidebar_position: 6
---

# Complete PA1

PA is the first and the only simulator lab in China for the course "Computer System Fundamentals" at Nanjing University. We introduced PA into "One Student One Chip" for the following reasons:

- PA covers most of the tasks of system engineering skills development: from hardware simulators, ISAs, and runtime environments, to homebrew OSes, libraries, and applications, it gives you a deep understanding of every detail of how a program runs on a computer.
  - If you choose to build your system software directly on an RTL-implemented processor, you first need to make sure that your processor is the implemented correct: if your pipeline has problems interacting with the bus in some extreme scenario, your homebrew OS and complex applications (such as complex games) won't run. In contrast, it is much easier to implement a simulator correctly than to implement RTL correctly.
- The simulator is an important component of processor verification: we want you to understand every detail of the simulator, to customize it when you need to, and not to treat it as an external tool that has nothing to do with you.

:::info[Course resources for "Fundamentals of computer systems"]
In the process of completing the PA, if you need to complement some theoretical knowledge, you can refer to Ms. Yuan Chunfeng's course on China University MOOC: [Part 1][mooc1], [Part 2][mooc2], [Part 3][mooc3]
:::
[mooc1]: https://www.icourse163.org/course/NJU-1001625001

[mooc2]: https://www.icourse163.org/course/NJU-1001964032

[mooc3]: https://www.icourse163.org/course/NJU-1002532004

:::warning[Read the FAQ (Frequently Asked Questions) in the PA handout.]
Before doing the PA, we strongly recommend that you read [FAQ in the PA handout][PA FAQ] to get a better understanding of the PA.
:::
<!-- [PA FAQ]: ../../ics-pa/FAQ.html -->

:::warning[Complete PA1]
Complete the content according to the PA handout (ISA chose the default `riscv32`) until you see the following prompt box:

- [Infrastructure: Simple Debugger][gdb]
- [Expression evaluation][expr]
- [Watchpoint][watchpoint]
- Complete the required exercises in PA1 until you see the following prompt box:

#### flag::hint

This is the end of PA1...
:::

<!-- [gdb]: ../../ics-pa/1.4.md

[expr]: ../../ics-pa/1.5.html

[watchpoint]: ../../ics-pa/1.6.html -->
