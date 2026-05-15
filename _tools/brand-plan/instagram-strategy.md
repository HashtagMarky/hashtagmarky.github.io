# #M Productions — Instagram Strategy

**Version 2.0 · May 2026**

-----

Instagram is the primary social platform for the HashtagMarky brand. The goal is to grow both the ROM hacking and bookstagram audiences while cross-linking to the website for long-form content and SEO.

## Account Setup

| Setting | Action |
|---|---|
| Account type | Switch to **Creator** (not Business) — required for Insights and Google indexing of posts |
| Bio | `Pokémon ROM Hacker \| Sci-Fi & Fantasy Bookstagram \| Building Pokémon Ikigai` |
| Link in bio | Live site URL (or Later multi-link if linking to specific posts) |
| Alt text | Fill in on every post — Instagram uses it for indexing. Write it, don't leave it auto-generated. |
| Category label | Set to match your niche — signals context to the algorithm |

**Why Creator over Business:** Same analytics access, more flexible link-in-bio options, better DM organisation. Business accounts are for companies with ad spend. Creator is right for solo builders and content creators.

-----

## Caption Structure

Every caption follows this structure regardless of post type:

```
[Hook — first line, no hashtags, keyword-rich sentence]
What I built: an image processor that runs in the browser.

[Body — 2–4 lines expanding on the hook]
No uploads, no server. Pure client-side JS using the Canvas API.
Drag in an image, pick a filter, download the result.

[Call to action]
Full breakdown on my site — link in bio.

[Hashtags — after a blank line, at the very end]
#pokemonromhack #pokeemerald #romhacking
```

**Why this order matters:** Instagram indexes the first line for search. It also truncates captions in the feed after ~125 characters, so the hook is what people see without tapping. Put the actual topic there — not a teaser, not a question, not an emoji string.

**Keyword placement rules:**
- First caption line: primary topic keyword (name the thing — "Route 3 redesign", "canvas image processor", "Name of the Wind review")
- Alt text on every image: describe what's literally shown + topic context. Do not leave it auto-generated.
- Location tag: add if relevant — it's an additional indexing signal

-----

## Post Structure

**Content format by reach:**

| Format | Algorithm reach | Save/share weight | Notes |
|---|---|---|---|
| Reels | Highest — pushed to Explore | Medium | Best for discovery; first 1–3 seconds decide watch-time |
| Carousels | Medium | High — saves weighted more than likes | Underrated; high save rate signals quality content |
| Static image | Low | Low | Mostly reaches existing followers |
| Stories | Followers only — not indexed | — | Use for link stickers and driving traffic, not discovery |

**Book review post:**

- Carousel format: 5–7 slides
- Slide 1: Cover image + title + author + star rating
- Slide 2: Hook sentence + plot summary
- Slide 3: Your take
- Slide 4: Who's it for
- Slide 5: Verdict quote + rating breakdown
- Caption: first line = keyword-rich summary (title + author + one-word take). Hashtags at end.
- Alt text: `[Book title] by [Author] — [one sentence description]`

**Devlog / project post:**

- Reel format preferred for discovery (30–60 seconds)
- Show something moving — a route being walked, a map scrolling, a button press
- On-screen text overlay with key info; subtitles help retention
- Caption: episode number + 2–3 sentence summary + "full devlog at link in bio"
- Hashtags: 5–8 tags placed at the end after a blank line

-----

## Driving Traffic to the Site

The goal of every post is to move people from Instagram to the site, where they stay longer and generate signals that improve search ranking.

**Mechanics:**
- **Link in bio** — point directly to `hashtagmarky.github.io` or use a tool like Later to create a multi-link landing page (latest devlog, books index, site home)
- **Link sticker in Stories** — available to all accounts. Post a Story teasing a devlog or review, add a link sticker pointing to the specific post URL (`/devlog/slug/` or `/books/slug/`)
- **Explicit CTA in every caption** — "full breakdown at link in bio" or "read the devlog at link in bio." People don't click unless prompted.
- **Reels that cut off** — show 30 seconds of a project walkthrough then end with "full writeup on my site" — traffic from that Reel is a behavioral signal Google weights

**Note on Instagram links and SEO:** Instagram profile links are `nofollow` — they don't pass link authority directly to your site. The SEO value comes from the referral traffic itself. People arriving from Instagram and spending time on your site is a behavioral signal. Build brand association around your name and niche so that when people search `hashtagmarky` or `pokémon ikigai rom hack`, your site ranks because they already know to look for it.

-----

## Hashtag Strategy

**Volume mix — aim for 5–10 tags per post:**

| Type | Volume | Example | Purpose |
|---|---|---|---|
| Broad | 1M–10M posts | `#pokemonromhack` | Visibility ceiling — you won't rank but you get seen by followers of the tag |
| Mid | 50k–500k posts | `#pokeemerald` | Realistic ranking potential — most value here |
| Niche | 5k–50k posts | `#pokemonroutescripting` | High signal-to-noise, smaller but engaged audience |

**Avoid tags with 10M+ posts** — your post will never surface in them. The feed moves too fast.

**Finding accounts via hashtags:** Instagram removed the Recent sort from hashtag feeds. Instead: tap a post you like → check that account's followers/following for a pre-filtered niche list. Use keyword search (not hashtag search) to surface accounts and reels directly. The Suggested for you feed after following a niche account is also reliable.

**Maintain a consistent core set of 10–15 tags** across posts in the same content pillar. Instagram uses tag history to classify your account. Jumping between unrelated tags every post resets that signal.

**Tag sets by pillar:**

- ROM hacking: `#pokemonromhack` · `#pokeemerald` · `#romhacking` · `#gbaromhack` · `#pokeemeraldexpansion` · `#pokemonhack`
- Books: `#bookstagram` · `#scifibooks` · `#fantasybooks` · `#bookreview` · + exact series/author tag when applicable
- Lego Gameboy / builds: `#buildlog` · `#raspberrypi` · `#diygameboy` · `#legotech` · `#raspberrypizero`

**Posting cadence:** Consistency beats frequency. Three posts per week maintained is worth more to the algorithm than seven posts one week then nothing. The engagement window after posting is roughly the first hour — reply to comments in that window.

-----

## Instagram Post Checklist

- [ ] First caption line contains the primary keyword (names the thing — not a teaser)
- [ ] Caption ends with a CTA pointing to the site ("full devlog at link in bio")
- [ ] Hashtags placed at the end after a blank line — 5–10 tags, mix of broad/mid/niche
- [ ] Alt text written on every image (not auto-generated)
- [ ] Bio link is up to date (site URL or multi-link landing page)
- [ ] Creator account mode active (required for Insights and Google indexing)
- [ ] For devlog posts: link sticker Story published pointing to the specific `/devlog/slug/` URL
- [ ] Replied to comments within the first hour after posting
