---
sidebar_position: 2
---

# Linux system installation and basic usage

:::warning[Install a Linux operating system]
We're going to reuse the contents of the PA handout, and we're going to ask you to follow PA0 to install Linux OS.
:::
<!-- [pa0]: ../../../ics-pa/PA0.html -->

:::warning[Get "One Student One Chip" code framework]
When you read the PA0 handout and proceed to the section on getting the PA framework code, you will be prompted with a box asking you to return to the content of the handout here.

First of all, please add a ssh key on github, please STFW on how to do that. Then get the framework code of "One Student One Chip" by the following command:

```
git clone -b master git@github.com:OSCPU/ysyx-workbench.git
```

Once you have it, you can go back to the appropriate place in the PA handout and continue reading. But you should also note that:

- Please use `ysyx-workbench` as the project directory in the PA handout, i.e. replace occurance of `ics2022` in the PA handout with `ysyx-workbench`.
- When change the student number and name in `ysyx-workbench/Makefile`, you can leave the student number unchanged until you have completed the preliminary.

This jumping back and forth may cause you some trouble, but the reason we do it this way is that we want to manage the documentation as if it were code: we want to do something like `The "One Student One Chip" handout calls the PA handout`, so we mention as little as possible about the "One Student One Chip" project in the PA handout, and put all the "One Student One Chip" content in the "One Student One Chip" handout itself. Failure to follow this principle not only makes it difficult for us to maintain the handouts, but also makes it difficult for people to know where to look for relevant content when reading the handouts.
:::
<!-- -->

:::danger[Installing an OS is the easiest training for independent problem solving]
If you are installing and using Linux for the first time, you may encounter a lot of problems. Don't worry, since Linux is used all over the world, there is a high probability that the problems you have encountered have been encountered by other people, and searching for keywords on the Internet will most likely lead you to a solution.
:::
<!-- -->

:::danger[Establishing the right values and maximizing the training you get.]
In fact, you can always get around these drills with a little ingenuity, such as

- Use someone else's VM image or a one-click install and configuration script to accomplish the tasks in this subsection in a snap.
- Found the so-called PA guide on the Internet and happy that you don't need to study yourself.
- Getting the core code or code for previous "One Student One Chip" cohort from someone and call that study.

Some students will think, "Why can't I refer to other people's guides and codes? I know what I'm doing!" But from the training point of view, <Highlight color="#c40e0e">"understand" and "independent completion" is very different</Highlight>: do you know why the masters do this, rather than that? How many potholes have the masters stepped in, and what is the rationale behind these potholes, can you see it? You should think about what you have to lose as opposed to what you have to gain by just laying down and copying. The notion that "copying the right thing is a good thing" is a way of lowering your expectations is not in line with the values we are promoting.

In fact, if you're a beginner, these little witticisms can cause devastating damage to your training:

- You're referencing things that you shouldn't be referencing at this stage, and they become the upper boundary of your learning, because you're barely aware of what's wrong with them, which makes it almost impossible for you to do better than them.
- And it gives you the illusion that "I'm a good learner, I'm good at learning," and you don't try, and you don't know how to do it better.
- Worse, you don't get the training you need now, but in the future you'll always be faced with new problems for which there's no cheat sheet or reference code, and you won't be able to solve them.

But to be honest, the TA team has almost no effective way to prohibit people from playing smart. In fact, <Highlight color="#0b6623">it's more a matter of recognizing and enforcing them from the bottom of your heart</Highlight>: when you find some so-called cheat sheets, you should think to yourself that "reading them will reduce the effectiveness of the training", and then you voluntarily reject their temptation and insist on completing the experiments on your own. It's similar to the way we all recognize academic integrity: you know it's wrong to cheat on an exam, and then you take it upon yourself to complete the exam independently.

Indeed, academic integrity goes far beyond not cheating on exams, and we recommend reading [MIT's interpretation of academic integrity][integrity], especially [Academic integrity in writing code][coding integrity]. Here, we quote some sample statements.

- When the handout asks to "implement X", you must implement X independently without reusing any external resources.
- Sharing code and exchanging test cases are both inappropriate.

You may think these requirements are out of line, but these guidelines are ultimately designed to get you the results you want: don't forget that you're learning to improve, not delivering a program. If you stick with it, you can become a true professional.
:::
[integrity]: http://integrity.mit.edu/

[coding integrity]: http://integrity.mit.edu/handbook/writing-code

:::info[Can I use other Linux distributions?]
We don't make it mandatory to use a particular Linux distribution, so we often get questions like "will using xxx distro affect my experiments". First of all, please read the tips on distributions in PA0, but otherwise we probably can't give you a definitive answer, because we probably haven't used it.

In fact, if you decide to use a different distribution, you should be prepared to solve new problems on your own.
:::
<!-- -->

:::info[Getting started with Linux zero-based users]
We recommend [Linux101][Linux101] initiated by the Linux User Association of the University of Science and Technology of China. You can choose the parts you are interested in and read them.
:::
[Linux101]: https://101.ustclug.org/

:::info[The Art of Command Line]
[The Art of Command Line][cmd] This article summarizes a number of commonly used command line tools and is worth reading.
:::
[cmd]: https://github.com/jlevy/the-art-of-command-line

<!-- -->

:::warning[Learning basic Linux usage]
We recommend MIT's Linux Tools Series: [The Missing Semester of Your CS Education][missing]. By taking these courses, you will learn how to use the tools in Linux to easily accomplish various tasks, which will greatly improve your work efficiency.

**Mandatory Questions**:

- Course overview and shell
- Shell tools and scripts
- Editor (Vim)
- Data organization
- Command line environment
- Version control (Git)

Includes reading handouts and completing post-course exercises. In addition, [Lecture Video][missing bilibili] is here for reference.
:::
[missing]: https://missing-semester-cn.github.io/

[missing bilibili]: https://www.bilibili.com/video/BV1x7411H7wa
