# State of the Art: AI Geopolitics, Technological Sovereignty, and Semiconductor Supply Chains

*Critical review of indexed literature (2019–2026), prepared as academic support for Volume 2: Frontiers and Applications*

## 1. Main Research Lines

**Line 1: Techno-nationalism as a dominant paradigm.** The systematic review in Frontiers (2026) on semiconductor industry governance identifies that post-2018 empirical research overwhelmingly points to "techno-nationalism" as the primary driver of current national strategies (Gao et al., 2023; Hsu, 2025; Kim & Rho, 2024; Manning & Richter, 2023). The central finding of this line is a paradigm shift: industrial policy's objective is no longer economic efficiency, but "supply chain resilience" (Kim & Rho, 2024) and "technological sovereignty" (Lavery & Lopes-Valenca, 2025; Yuan et al., 2025)—the exact shift that Chapter 19 of the original work in this series describes as moving "from technical neutrality to digital sovereignty," now backed by direct, verifiable academic research.

**Line 2: Politics of AI supply chains.** An article published in *AI & Society* (Lee & Hawkins, 2024, on strategic secrecy among suppliers) documents how organizations within the AI supply chain treat supplier identity as a strategic trade secret, compounded by AI's perceived geopolitical importance. This line connects directly with this book's "agnostic backend" warning: if even industry firms cannot verify their complete supplier chain with certainty, an architecture team has even less visibility. This reinforces (from a source external to this book) the imperative to design for substitutability rather than assuming supplier transparency.

**Line 3: Forward-looking scenarios for the AI-relevant semiconductor supply chain.** A study by the Geneva Graduate Institute (2024) develops four scenarios for 2040 regarding the geopolitics of the AI-relevant semiconductor supply chain, ranging from complete fragmentation to managed cooperation. It is the only source in this review with an explicitly long time horizon (15+ years), offering a valuable contrast to the short- and medium-term focus dominating the rest of the literature as well as this volume.

**Line 4: AI in supply chain management (SCM), beyond fabrication geopolitics.** This distinct yet related line explores how AI integrates *within* supply chain management (demand forecasting, inventory optimization), documented by a systematic literature review (SLR) published in *Frontiers in AI* (Samuels, 2025, PRISMA protocol, Web of Science/Scopus/IEEE/Google Scholar/ScienceDirect databases, 2010–2023) and by a bibliometric review specifically targeting AI-assisted supply chain risk assessment. This line supports the industry chapters of Volume 2 (mining, manufacturing) from an angle distinct from geopolitics: operational resilience rather than national sovereignty.

## 2. Theoretical Frameworks Used

An **international political economy** framework dominates (Farrell & Newman, 2019, on weaponized interdependence; Aggarwal & Reddie, 2021), treating technology as an instrument of state power. This is complemented by **supply chain risk management** frameworks of managerial rather than geopolitical origin (Govindan et al., 2020, on supply network risk contagion). Notably—and representing a substantive divergence rather than merely a difference in emphasis—these two traditions rarely cite each other: international political economy literature treats the semiconductor chain as an arena of state power, whereas SCM literature treats it as an operational optimization problem. By integrating both country-level geopolitical chapters and applied industry cases within a single volume, this book bridges a divide that academic literature still confines to separate disciplinary silos.

## 3. Methodologies Applied

Three approaches predominate: systematic reviews following the PRISMA protocol (Samuels, 2025), secondary source analyses employing case study approaches by country or geopolitical bloc (the CEU study on semiconductors as a geopolitical weapon explicitly notes its reliance on secondary source analysis), and prospective scenario modeling (Graduate Institute, 2024). Unlike Volume 1 and Volume 3, this research domain **lacks a dominant methodological consensus**: it is a younger, more fragmented field split across international relations, economics, and industrial engineering. This is itself a relevant finding that contextualizes this book's own approach, which deliberately blends geopolitical and technical analysis within the same volume.

## 4. Recurring Findings

- The shift from a "market-first" to a "security-first" paradigm in semiconductor policy is consistently documented across multiple independent studies (Bown & Wang, 2024; Donnelly, 2023).
- The formation of regional technological alliances as a direct response to US–China competition (the Chip 4 Alliance: United States, Taiwan, Japan, South Korea) is replicated across several sources (Chow, 2025; Peterson, 2022; Chu, 2024), aligning with the country-by-country analysis conducted in this volume's geopolitical chapters.
- Data from 2025–2026 (dependency risk analysis source, Cloud Security Alliance) empirically corroborates this book's substitutability thesis with a concrete figure: 74% of surveyed enterprises in April 2026 would face significant disruption if they lost access to their primary AI vendor. This provides the most direct quantitative argument favoring an agnostic backend located outside this book itself.

## 5. Author Discrepancies

The underlying discrepancy is normative rather than empirical: authors from the international political economy tradition tend to portray techno-nationalism as a rational, if costly, response to a genuine risk of coercion. Conversely, authors from the supply chain management tradition tend to portray resulting fragmentation as an *additional* source of operational risk rather than its remedy. Both positions are defensible based on available evidence, and this book does not resolve this tension—nor does it attempt to. Instead, it documents, chapter by chapter and country by country, how each geopolitical bloc manages this tension differently.

## 6. Methodological Limitations of the Reviewed Literature

- **Heavy reliance on secondary and journalistic sources** across much of the semiconductor geopolitics literature, an aspect explicitly acknowledged by authors themselves (CEU, 2025). This limitation applies proportionally to the country-specific chapters of this book, which combine technical analysis with recent press reporting (e.g., Global Times, SCMP) given the unfolding nature of current events.
- **Predominantly reactive time horizon**: Most studies analyze events post facto (sanctions, tariffs) rather than constructing robust predictive frameworks; the exception is the 2040 scenario study, which, by its forward-looking nature, possesses lower immediate empirical verifiability.
- **Disciplinary fragmentation** (Section 2): No study in this review systematically integrates software engineering perspectives with infrastructure geopolitics, leaving academically unresolved the core question this book addresses: what an engineering architecture team—rather than a sovereign government—must do when confronting these risks.

## 7. Knowledge Gaps

1. **Scant indexed academic research on Latin America** within the context of AI geopolitics and semiconductors: reviewed sources focus overwhelmingly on the United States, China, the European Union, Taiwan, Japan, and South Korea.
2. **Absence of frameworks translating macro-level geopolitical risk into concrete software architecture decisions**: The literature offers either geopolitical diagnoses or physical supply chain risk management, but lacks a bridge to AI system design decisions at the individual organizational level—a void directly filled by this volume's Agnostic Backend principle and geopolitical traceability matrix.
3. **Lack of longitudinal data on the actual impact of "design for substitutability"** as a mitigation strategy: The 74% vendor disruption exposure metric (Section 4) represents a point-in-time snapshot rather than a longitudinal investigation into whether organizations that deliberately engineer for substitutability reduce that vulnerability over time.

## 8. Relationship to the Central Thesis of the Book

The thesis of this volume—that systems architecture must be engineered assuming the inevitable need for vendor substitution, and that geopolitics constitutes an architectural constraint every bit as real as latency or cost—is directly corroborated by the reviewed literature. The documented transition from "market-first" to "security-first" (Section 4) is precisely the macro-level phenomenon that necessitates, at the engineering level, the Agnostic Backend discipline proposed in this book. The gap identified in Section 7 (the absence of a bridge between macro-geopolitics and software architecture decisions) defines the exact space this volume occupies, bridging a divide that academic literature, compartmentalized between international relations and industrial engineering, has yet to close.
