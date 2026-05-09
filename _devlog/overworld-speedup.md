---
title: "Overworld Speedup"
date: 2025-01-17
project: feature-branch
summary: "An overworld speed multiplier for pokeemerald, 1x, 2x, 4x, or 8x, that runs extra animation and camera iterations without touching collision or input logic."
description: "A pokeemerald overworld speedup implementation — four speed levels controlled by a VAR, suppressed by holding R or a flag, by including extra loop iterations for animations and the camera only."
stats:
  Last branch update: 17th January 2025
  Speed levels: 1x, 2x, 4x, or 8x
  Files changed: 4
---

## What It Does

Adds a speed multiplier to the overworld loop with four levels: 1x, 2x, 4x, and 8x, using `VAR_OVERWORLD_SPEEDUP` to control which level is active. The speedup runs additional iterations of `AnimateSprites()`, `CameraUpdate()`, and `UpdateCameraPanning()` within the normal `OverworldBasic()` call, resulting in 0, 1, 3, or 7 extra iterations respectively. Collision detection, script execution, and input handling are not re-run in the extra iterations, so the game logic stays consistent while movement and animation run faster.

The speedup can be disabled on the fly by holding R, or blocked entirely with `FLAG_PREVENT_OVERWORLD_SPEEDUP`, useful for cutscenes or specific areas where running at full speed would break something.

<video src="/images/devlog/overworld-speedup/overworld_speedup.mp4" autoplay loop muted playsinline title="Overworld Speedup in Emerald" ></video>


## How It's Implemented

Four files changed: `include/overworld.h` (speed constants and the function declaration), `src/overworld.c` (`OverworldSpeedup_AdditionalIterations()` implementation and the hook into `CB2_Overworld()`), `include/constants/flags.h` (`FLAG_PREVENT_OVERWORLD_SPEEDUP`), and `include/constants/vars.h` (`VAR_OVERWORLD_SPEEDUP`).

Both the flag and VAR constants are set to `0` as placeholders — any ROM hack using this branch needs to assign real slot values in `flags.h` and `vars.h`. The flag guard in the source is written specifically so that a value of `0` makes the prevention check dead code by default, which is a safe no-op until real slots are assigned.

One practical note from testing: the difference between 8x and 16x is not noticeably meaningful, and 32x starts to produce visible performance issues, so 8x is a reasonable ceiling for the speed levels.

### Installation

The [diff for this feature](https://github.com/HashtagMarky/pokeemerald/commit/ab8d603353fdb1c354abc884978ac67d3120aaab) can be used to add these changes. A full step-by-step tutorial is also available on the [Team Aqua's Asset Repo wiki](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Overworld-Speedup), which covers porting to `pret/pokefirered` and `RHH/pokeemerald-expansion` as well.

## Why It's In Ikigai

When playing on an emulator, players tend to use speedup. In games with custom music, emulator speedup will cause it to be inaudible, or players may even breeze past important story elements. Adding a controllable speedup option, even just 2x makes a noticeable difference to how the game feels to navigate without making it feel out of control.
