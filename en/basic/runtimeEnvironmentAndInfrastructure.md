---
sidebar_position: 3
---

# Runtime Environment and Infrastructure

You have implemented NPC using RTL, and currently it is a simple single-cycle processor that only supports two instructions: `addi` and `ebreak`.
To run more programs, it is natural to add more instructions to NPC.
However, you will soon encounter a problem: how should we compile a program that can run on NPC and then run it on NPC?

In this section, we will first introduce an important abstraction layer between programs and computer hardware: the runtime environment.
At the same time, we will guide you to build more powerful infrastructure, which will play a significant role when designing NPC later on.

:::warning[Understand the Runtime Environment, Build More Infrastructure]
Complete PA2 Phase 2 according to the PA lecture notes until you see the following prompt:

#### flag::Hint

End of PA2 Phase 2.
:::