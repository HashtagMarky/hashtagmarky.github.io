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

Back in November, **Bivurnum** mentioned in Team Aqua’s Hideout that they were looking to create a more definitive public Overworld Encounters implementation, to which I ~~joked~~ said that we should pick it up properly and create a pokeemerald-expansion pull request for it. After I hit accept on that fated friend request, our five month journey was set to begin. Let me set the scene:

- I had created [some overworld encounter tools](/devlog/overworld-encounter-scripting-tools), but they had become outdated. And if I’m being honest, they were very basic as it was from a time when I was far less confident in the codebase. But like most things, doing it once allowed me to do it much better the next time around.
- **Pokabbie** had open sourced *Pokémon Emerald Rogue*.
- **Jamie** (FosterProgramming) had already isolated and ported Pokabbie’s overworld encounter system to **Phantonomy**’s *Pokémon Ultra Eclipse*.

We messaged Jamie and Pokabbie, asking for permission to use the work they’d done so far, then started on our own iteration, with a lot of review cycles, and at least one “I don’t know how the PR keeps getting closed” from Biv after accidentally hitting the close PR button. We consider ourselves very lucky, as we had nothing but support during development for this feature, whether it was complicated code contributions, or a simple “This is cool, good job”, we were really driven to make this the best it could be.

## How It Works

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<video src="/images/devlog/overworld-encounters/emerald-owe.mp4" poster="/images/devlog/overworld-encounters/emerald-owe-poster.jpg" controls playsinline title="Overworld Encounters in Emerald" width="240" height="160"></video>
<video src="/images/devlog/overworld-encounters/firered-owe.mp4" poster="/images/devlog/overworld-encounters/firered-owe-poster.jpg" controls playsinline title="Overworld Encounters in FireRed" width="240" height="160"></video>
</div>

*Some examples of Overworld Wild Encounters on the first routes in Generation 3.*

Overworld Wild Encounters (OWEs) are wild Pokémon that appear as actual objects on the map, the same mechanic you'd recognise from Generation 8 and Generation 9, just now running on a GBA. Instead of stepping onto an encounter tile, triggering a random battle, you can see the Pokémon in the overworld, and choose whether or not to engage.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/overworld-encounters/owe-behavior-wander.gif" alt="Wander OWE Behaviour" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-behavior-watch.gif" alt="Watch OWE Behaviour" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-behavior-approach.gif" alt="Approach OWE Behaviour" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-behavior-chase.gif" alt="Chase OWE Behaviour" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-behavior-flee.gif" alt="Flee OWE Behaviour" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-behavior-despawn.gif" alt="Despawn OWE Behaviour" width="240" height="160">
</div>

*The six preset movement behaviours: wander, watch, approach, chase, flee, and despawn.*

Here's what the implementation supports:
- **Automatic spawning**: OWE objects get generated from the map's existing land and water encounter tables. It's automatic and should be easy as it uses the same encounter system within the game already, just spawning them in the overworld.
- **Manual spawning**: Specific OWEs with a defined species, level, gender, or shininess can be created. We wanted something useful for specific story events.
- **Special cases**: Feebas fishing spots spawn can spawn a Feebas OWE, Mass Outbreaks, Roamers, Safari Zone, Battle Pyramid, and Battle Pike each have their own OWE configurations. We even allowed for just these edge cases of OWEs to be spawned, so they will be really special.
- **Despawning and replacement**: Older OWEs despawn over time and are replaced with new ones. Shiny Pokémon can be kept permanently, which is perfect for AFK shiny hunting.
- **Per-species movement**: Each species can have its own movement type and behaviours, chasing the player or running away depending on what you want them to do. There are some preset options included with the release.
- **Repel and Lure support**: Repels despawn OWEs that would be effected by them normally, while Lures keep all their benefits.
- **Restricted Movemenent** : OWEs can be restricted to certain metatiles or prevented from leaving a map. This will hopefully mean a player can always run away from an encounter, and it will help stop them from getting cornered into certain areas.
- **Legends Series Shiny Effects**: We recreated the Legends series shiny spawning, where shiny OWEs will have a sparkle graphic and play the shiny sound effect.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/overworld-encounters/wander_in_grass_movement.gif" alt="OWE Restricted Movement" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-full-odds-shiny.jpg" alt="Full Odds Shiny Overworld Wild Encounter" width="240" height="160">
</div>

*One of the [wander movement types from my previous OWE Tools](/devlog/overworld-encounter-scripting-tools/#wander-movement-types) was ported to this iteration. Is that…? **Holy sh\*t is that a full odds shiny?!** Excuse the rogue Moltres on Route 102, but yes it is actually. Even crazier, it was one of three that I had spawn during my hours of testing and bug fixing. I almost lost my mind.*

The core implementation lives in a new `include/config/wild_encounter.h` config file, with a lot of settings able to be toggled per project.

## How It Went

Biv and I worked well together, with a fairly natural split occuring over time. I was initially worried about working so closely with someone else, but all of these worries went, thankfully, unfounded. Biv, talented as they are, handled a lot of the core logic, including: the Repel and level checks, the despawn cycling, the Feebas edge cases and the movement behaviours. My contributions were a bit more varied. Having already attempted to build my own OWE system before this PR, I knew what the difficulties tended to be. I focussed on things like the consistent storage of OWE data, ability interactions so the encounters wouldn't feel different to pre-existing ones, and field effect behaviour. And yes, there was plenty of refactoring between the two of us as well.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/overworld-encounters/owe-safari.gif" alt="Safari Zone OWEs" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-mass-outbreak.gif" alt="Mass Outbreak OWEs" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-roamer.gif" alt="Roamer as an OWE" width="240" height="160">
</div>

*Mass Outbreak, Roamer, and Safari Zone each have their own OWE configurations.*

Even after Biv and I rebuilt the code for expansion, it was only fitting that Jamie would review the PR. Over April there were 130 review comments between the three of us, and ended up having to move most of the conversations to the rh-hideout Discord due to not being able to keep track of them. During review, there was a lot of back-and-forth about naming conventions, removing redundant code, and getting edge cases spot on. But we really appreciate the work Jamie and the rest of the expansion team for putting in the work needed for a feature like this.

A special mention has got to go to **Luuma** as well for testing and helping us squash a few bugs in the PR. As well as Biv's and my apologies, for managing to find a few bugs in the wider codebase on our travels, but a shoutout to the expansion contributors who have managed to fix them already, and who will continue to make this feature even better.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/overworld-encounters/owe-bike-scare.gif" alt="Cycling scares OWEs away" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-double-battle.gif" alt="OWE triggering a double battle" width="240" height="160">
<img src="/images/devlog/overworld-encounters/owe-repel.gif" alt="Repel despawning OWEs" width="240" height="160">
</div>

*Cycling scares nearby OWEs away. OWEs also support double battles, and Repel correctly despawns those it would normally affect.*

Now I have to admit something, there were times where we had to be practical rather than as extravagant as we wanted. Due to the object, tile and palette limits of the GBA, we could only feasibly have a few encounters on screen at once, potentially limiting which ones spawn in some scenarios. This **is not** exclusive to the use of OWEs, but just the nature overworld itself, and we had to remind ourselves of that instead of being disappointed that we might not meet expectations. These can be circumvented by a developer, but it will require manual tweaking for their own project.

By the time it was done, the PR had touched 46 files, added 3,641 lines, removed 181, and accumulated 818 commits across both our branch and the review fixes. [#8434 - Overworld Encounters](https://github.com/rh-hideout/pokeemerald-expansion/pull/8434) was merged into `upcoming` on 29th April 2026.

## What This Means for Ikigai

Overworld encounters have always been planned for [Pokémon Ikigai](/ikigai), but now they will be implemented in a much better way. Being able to see Pokémon in the world before engaging them, rather than every encounter being a blind roll with some many options in how it's used, will be perfect.

It goes without saying, the journey from my first toolset to this level of integration was one of the most satisfying in my ROM hacking career so far. Having such an exciting feature in the expansion as first-party code means I and other users can use it without worrying about just one person maintaining it. It was massively worth the five months, and I loved working on my first big expansion feature alongside the more experienced and massively talented Bivurnum.
