# Gospel of Jesus

## Purpose

This repository exists to assemble a single, self-contained record of the teachings and actions of Jesus of Nazareth **restricted exclusively to the period of his lifetime**.

The sole objective is to collect and organize what Jesus himself said and did while he was alive. The resulting compilation is intended to stand as a book of primary material only.

No material that occurs after death is permitted.

## Table of Contents (Book)

A dedicated navigation page is available at [`book/00-toc.md`](book/00-toc.md).

- [Preface](book/00-preface.md)
- [1. Core Proclamation](book/01-core-proclamation.md)
- [2. Authority](book/02-authority.md)
- [3. Ethical Teaching](book/03-ethical-teaching.md)
- [4. Parables](book/04-parables.md)
- [5. Encounters](book/05-encounters.md)
- [6. Discipleship](book/06-discipleship.md)
- [7. Conflict](book/07-conflict.md)
- [8. Final Days](book/08-final-days.md)

**Spanish translation** of the full book is available in [`book-es/`](book-es/). See [`book-es/README.md`](book-es/README.md) for details.

## Strict Scope Boundaries

### Included

- Words attributed to Jesus during his public ministry and private conversations while alive.
- Actions performed by Jesus during that same period (healings, exorcisms, table fellowship, journeys, confrontations, prayers, etc.).
- Direct interactions between Jesus and other people (disciples, crowds, religious leaders, individuals who approached him, including non-Jews) as recorded in the lifetime narrative.
- The core announcement Jesus repeatedly made: the nearness of the kingdom of God, the call to repent, and the demand to believe that announcement.

### Explicitly Excluded

- Any account, appearance, conversation, or commission that occurs after death.
- All writings, letters, theological reflections, or interpretive frameworks produced by other people (including Paul and every other New Testament author writing after the events).
- Later ecclesiastical doctrines, creeds, systematic theologies, or denominational traditions.
- Opinions, commentary, or explanatory notes that originate outside the lifetime material itself.
- Speculative reconstructions that go beyond what the lifetime narratives record.

The boundary is chronological and authorial: only the living Jesus, only his own speech and deeds as presented in the portions of the Gospel accounts that describe events while he was still alive (up to and including the moment of death).

## Project Intent in Detail

The project answers a precise question:

> Can a coherent presentation of “the gospel of Jesus” be formed solely from the words and actions recorded while he was still alive, without dependence on any later teaching?

The answer pursued here is affirmative in method: the lifetime material itself contains a recognizable message centered on the arrival of God’s kingdom, the call to repentance and trust, the ethical demands of discipleship, and Jesus’ own exercised authority. That message is what this repository seeks to isolate and present without admixture.

Key observations drawn strictly from the lifetime record include:

- Jesus framed his public work as directed to the lost sheep of the house of Israel and restricted the initial mission of the Twelve accordingly.
- At the same time, individual non-Jews who approached him in faith received healing, deliverance, and recognition of that faith.
- Faith, not ethnic status, is repeatedly shown as the decisive human response that opens access to what Jesus offered.
- The content of the announcement remained the nearness of the kingdom and the demand to repent and believe; developed explanations of his death, justification theories, or multi-ethnic church structures lie outside the chronological limit and are therefore excluded.

## Directory Structure

```
gospel-of-jesus/
├── README.md                      # Project intent and hard boundaries
├── LICENSE                        # CC0 1.0 Universal (public-domain dedication)
├── book/                          # THE MAIN BOOK (English source of truth)
│   ├── 00-toc.md                  # Table of Contents
│   ├── 00-preface.md
│   ├── 01-core-proclamation.md
│   ├── 02-authority.md
│   ├── 03-ethical-teaching.md
│   ├── 04-parables.md
│   ├── 05-encounters.md
│   ├── 06-discipleship.md
│   ├── 07-conflict.md
│   └── 08-final-days.md
├── book-es/                       # Spanish translation of the book
│   ├── README.md                  # Relation to English source + notes
│   ├── 00-toc.md
│   ├── 00-preface.md
│   ├── 01-core-proclamation.md
│   ├── 02-authority.md
│   ├── 03-ethical-teaching.md
│   ├── 04-parables.md
│   ├── 05-encounters.md
│   ├── 06-discipleship.md
│   ├── 07-conflict.md
│   └── 08-final-days.md
├── references/                    # Reference & supporting documentation
│   ├── passage-map.md             # Maps included material to source locations
│   ├── chronology.md              # Notes on internal ordering
│   ├── exclusions.md              # Explicit record of what is omitted and why
│   ├── red-letter-inventory.md    # Master inventory of lifetime spoken words
│   └── gap-analysis.md            # Gap analysis for completeness work
└── supporting/                    # Project infrastructure
    ├── methodology.md             # Detailed inclusion / exclusion rules (locked)
    ├── editorial-notes.md         # Practical editorial practices (parallel accounts, etc.)
    └── status.md                  # Current progress tracker
```

### Role of each directory

- **`book/`**  
  Contains the main compilation. Each file is a thematic chapter. Content is drawn exclusively from Jesus’ lifetime words and actions. A table of contents (`00-toc.md`) provides navigation. This is the English source of truth.

- **`book-es/`**  
  Contains a faithful Spanish translation of every file in `book/`. It follows the same structure, chapter order, and locked methodology boundaries. No new content is introduced.

- **`references/`**  
  Holds supporting documentation that protects the boundary: source mapping, chronological decisions, a running log of exclusions, the red-letter inventory, and gap analysis.

- **`supporting/`**  
  Contains the methodological rules that govern the entire project, a short record of practical editorial practices, and a simple status file.

## Methodological Rules

1. **Source limitation**  
   Only material narrated as occurring while Jesus was still alive (up to and including the moment of death) is eligible. Scenes that occur after death, even if found in the same Gospel documents, are out of scope.

2. **No secondary voices**  
   The compilation contains Jesus’ words and a minimal narrative frame necessary to make those words and actions intelligible. It does not include the theological commentary of the Gospel writers, the letters of Paul, or any later author.

3. **No interpretive overlay**  
   The repository does not advance opinions about the meaning, application, or contemporary relevance of the material. Presentation is limited to organization and clear quotation or close paraphrase of the lifetime record.

4. **Transparency of boundaries**  
   Every section remains traceable to the lifetime narrative (while Jesus was still alive). Where a saying or action is included, its place inside the lifetime chronology is evident.

## Current Status

**PROJECT COMPLETE** (2026-08-03)

**RED-LETTER COMPLETENESS WORKSTREAM ALSO COMPLETE** (Issues #17–#22)

- Repository and boundaries defined
- Full directory structure scaffolded
- Methodology locked
- All eight book chapters populated with lifetime material (expanded under the red-letter workstream with high-priority missing sayings)
- Passage map completed, verified, and fully updated for all included material
- Chronology notes developed with major ordering decisions and lifetime-record rationales
- Exclusion log maintained and expanded (including explicit rationales for remaining red-letter items under the completeness mandate)
- Master red-letter inventory of all lifetime spoken words created and statused
- Gap analysis performed and acted upon
- Final boundary and consistency review completed (Issue #14)
- Red-letter final verification and boundary check completed (Issue #22)
- Status updated and both the original project and the red-letter completeness workstream formally closed

Every inventoried lifetime saying of Jesus (while still alive, up to the moment of death) is either fully present in the book or carries an explicit, logged exclusion rationale. No material that occurs after death is present. Style and thematic organization remain consistent with the locked methodology.

All content continues to be measured against the rules stated above. Material that cannot be located inside Jesus’ lifetime is rejected.

---

**Boundary reminder**  
If a text, idea, or interpretation cannot be shown to belong to the living Jesus (i.e., before or at the moment of death), it does not belong in this repository.

## License

This work is dedicated to the public domain under [CC0 1.0 Universal](LICENSE).
