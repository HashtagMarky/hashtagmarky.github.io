---
title: "Overworld Speedup"
date: 2025-01-17
project: feature-branch
summary: "An overworld speed multiplier for pokeemerald, 1x, 2x, 4x, or 8x, that runs extra animation and camera iterations without touching collision or input logic."
description: "A pokeemerald overworld speedup implementation with four speed levels controlled by a VAR, which can be suppressed by holding R or a flag."
stats:
  Last branch update: 17th January 2025
  Speed levels: 1x, 2x, 4x, or 8x
  Files changed: 4
---

## What It Does

This adds a speed multiplier to the overworld callback with four levels: 1x, 2x, 4x, and 8x, using `VAR_OVERWORLD_SPEEDUP`. The speedup runs additional calls of `AnimateSprites()`, `CameraUpdate()`, and `UpdateCameraPanning()` within `OverworldBasic()`, resulting in 0, 1, 3, or 7 extra iterations. Collision detection, script execution, and input handling are not re-run, so other game logic should stays consistent while movement and animations run faster.

The speedup can be disabled on the fly by holding R, or blocked entirely with `FLAG_PREVENT_OVERWORLD_SPEEDUP`, useful for cutscenes or specific areas where running at full speed would break something.

<video src="/images/devlog/overworld-speedup/overworld_speedup.mp4" autoplay loop muted playsinline title="Overworld Speedup in Emerald" ></video>


## How It's Implemented

The main logic lives in `CB2_Overworld()` within `overworld.c`. Both the `FLAG` and `VAR` constants are set to `0` as placeholders, and they need to be assigned 'real' values from `flags.h` and `vars.h`.

*A note from testing: the difference between 8x and 16x is not noticeably meaningful, and 32x starts to produce visible performance issues, so 8x is a reasonable ceiling for the speed levels.*

### Installation

The [diff for this feature](https://github.com/HashtagMarky/pokeemerald/commit/ab8d603353fdb1c354abc884978ac67d3120aaab) can be used to add these changes. A full step-by-step tutorial is also available on the [Team Aqua's Asset Repo wiki](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Overworld-Speedup), which covers porting to `pret/pokefirered` and `RHH/pokeemerald-expansion` as well.

## Why It's In Ikigai

When playing on an emulator, players tend to use speedup. In games with custom music, such as [Pokémon Ikigai](/productions/ikigai), emulator speedup will cause it to be inaudible, or players may even breeze past important story elements. Adding a controllable speedup option, even just 2x makes a noticeable difference to how the game feels to navigate without making it feel out of control.
