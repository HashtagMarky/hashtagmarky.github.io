---
title: "Overworld Encounters Merged into pokeemerald-expansion"
date: 2026-04-29
project: expansion
summary: "After five months of development, the Overworld Encounters feature I co-developed with Bivurnum was merged into pokeemerald-expansion, adding modern wild Pokémon encounters to the GBA Pokémon decompilations."
description: "A breakdown of how the Overworld Encounters system works in pokeemerald-expansion, how Bivurnum and I built it over five months, and what went into getting the pull request merged."
stats:
  Opened: November 19th, 2025
  Merged: April 29th, 2026
  Commits: 818
  Files changed: 46
  Lines added: "3,641"
---

## How It Started

This pull request had an odd start, so let me set the scene.
- I had created an overworld encounter system, but it was now outdated and quite frankly, not the best.
- **Pokabbie** had open sourced *Pokémon Emerald Rogue*.
- **Jamie** (FosterProgramming) had already isolated and ported Pokabbie's overworld encounter system to **Phantonomy**'s *Pokémon Ultra Eclipse*.

Back in November, Bivurnum mentioned in Team Aqua's Hideout that they were looking to create a public Overworld Encounters implementation, to which I ~~joked~~ said that we should pick it up properly and create a pokeemerald-expansion pull request for it. And just like that a five month journey was about to begin. We messaged Jamie and Pokabbie, asking for permission to use the work they'd done so far, then started on our iteration, review cycles, and at least one "I don't know how the PR keeps getting closed" from Biv.

## How It Works

<div style="display: flex; gap: 8px; align-items: flex-start;">
<video src="/images/devlog/overworld-encounters/emerald-ow.mp4" poster="/images/devlog/overworld-encounters/emerald-ow-poster.jpg" controls playsinline title="Overworld Encounters in Emerald" width="240" height="160"></video>
<video src="/images/devlog/overworld-encounters/firered-ow.mp4" poster="/images/devlog/overworld-encounters/firered-ow-poster.jpg" controls playsinline title="Overworld Encounters in FireRed" width="240" height="160"></video>
</div>

*Some examples of Overworld Wild Encounters on the first routes in Generation 3.*

Overworld Encounters (OWEs) are wild Pokémon that appear as actual objects on the map, the same mechanic you'd recognise from Generation 8 and Generation 9, but now running on a GBA. Instead of stepping into grass and triggering a blind random battle, you can see the Pokémon walking around and choose whether or not to engage.

Here's what the implementation supports:
- **Automatic spawning.** OWE objects generate from the map's existing land and water encounter tables. It's automatic, it uses the same encounter system within the game already, just spawns them in the overworld.
- **Manual spawning.** Specific OWEs with a defined species, level, gender, or shininess can be created, useful for specific story events.
- **Special cases.** Feebas fishing spots spawn as OWEs, shiny Feebas can't be despawned, and Mass Outbreaks, Roamers, Safari Zone, Battle Pyramid, and Battle Pike each have their own OWE configurations.
- **Despawning and replacement.** Older OWEs despawn over time and are replaced with new ones. Shiny Pokémon can be kept permanently, perfect for AFK shiny hunting.
- **Per-species movement.** Each species can have its own movement type and behaviours, chasing the player or running away depending on what you set for them to do.
- **Repel and Lure support.** Repels despawn OWEs that would be effected by them normally, while Lures keep all their benfits.
- **Legends Shiny sparkle effect.** Shiny OWEs will have a sparkle graphic as they spawn and will play the shiny sound effect, like in the Legends series of games.

The core implementation lives in a new `include/config/wild_encounter.h` config file, with a lot of settings able to be toggled per project.

## How It Went

Biv and I worked well together, with a fairly natural split emerging over time. Biv, talented as they are, handled a lot of the core logic, including: the Repel and level checks, the despawn behaviours, the Feebas edge cases and the movement behaviours. My contributions were a bit more varied. Having already attempted to build my own OWE system before this PR, I knew what the difficulties tended to be. I focussed on things like the consistent storage of OWE data, ability interactions so the encounters wouldn't feel different to pre-existing ones, and field effect behaviour. And yes, there was plenty of refactoring between the two of us as well.

Even after Biv and I rebuilt the code for expansion, it was only fitting that Jamie would review the PR. Over April there were 130 review comments between the three of us, and ended up having to move most of the conversations to the rh-hideout Discord. During review, there was a lot of back-and-forth about naming conventions, removing redundant code, and getting edge cases spot on. But we needed to be thorough for a feature this size. We also managed to find a few bugs in the wider codebase on our travels.

By the time it was done, the PR had touched 46 files, added 3,641 lines, removed 181, and accumulated 818 commits across both our branch and the review fixes. [#8434 - Overworld Encounters](https://github.com/rh-hideout/pokeemerald-expansion/pull/8434) was merged into `upcoming` on 29th April 2026.

## What This Means for Ikigai

Overworld encounters have always been planned for Pokémon Ikigai, but now they will be implemented in a much better way. Being able to see Pokémon in the world before engaging them, rather than every encounter being a blind roll with some many options in how it's used, will be perfect. Having this in the expansion as a first-party feature means I and other users can use it without worrying about maintaining it personally. It was worth the five months.
