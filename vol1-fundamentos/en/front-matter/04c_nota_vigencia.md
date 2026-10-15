# Note on Technological Shelf Life

*Added in response to the critique of "short-term technological obsolescence risk."*

This book explicitly names concrete tools, SDKs, and models. A volume discussing only abstract principles would be far easier to maintain over time, but far less useful to an engineer who needs to ship working software this week. Our editorial decision was to deliberately embrace the cost of partial deprecation in exchange for immediate operational utility, counterbalancing it in two ways:

1. **Explicit separation between architectural patterns and specific tools.** Whenever the text details an architectural pattern—the control harness, the Synthetic Enterprise, the AI Gateway, or MCP as an open protocol—that pattern remains independent of the vendor or SDK chosen to illustrate it.
2. **Identifying what decays, and how to verify it.** Model identifiers, per-token pricing tables, SDK versions, and feature comparison matrices carry the shortest shelf life. Always verify official vendor documentation before making high-stakes architectural commitments based on a specific figure in this book.
