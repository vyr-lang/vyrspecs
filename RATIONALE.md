# Vyr Design Rationale

Vyr is a programming language designed for AI agents as its primary users.

Human programmers still matter.  Humans set goals, review results, operate systems, and decide whether the produced software is valuable.  The difference is that Vyr treats AI agents as the main authors, maintainers, and readers of day-to-day program text.

Most existing programming languages were designed around human ergonomics: concise syntax, familiar notation, implicit convention, and flexibility for personal style.  Vyr instead optimizes for agent ergonomics: explicit structure, low ambiguity, localized reasoning, deterministic tooling, and machine-checkable intent.

The purpose of this document is to explain the assumptions about AI agents that drive Vyr's design.

## Agent Strengths and Weaknesses

AI agents have different strengths and weaknesses from human programmers.  Vyr is designed to exploit the strengths and compensate for the weaknesses.

### Strengths

- AI agents can generate and transform large amounts of code quickly.
- AI agents tolerate verbosity better than humans when the extra text carries useful structure.
- AI agents are good at repeating explicit patterns consistently across a codebase.
- AI agents can search, inspect, and cross-reference many files without fatigue.
- AI agents can use tools continuously: parsers, formatters, type checkers, tests, linters, databases, and source-control history.
- AI agents can work with multiple representations of the same program, including source text, syntax trees, schemas, generated documentation, and test traces.
- AI agents can perform mechanical refactors well when the boundaries and invariants are explicit.
- AI agents can synthesize boilerplate, adapters, migrations, and tests when the intended shape is precise.

### Weaknesses

- AI agents have limited working context and can lose important details when reasoning spans too much code.
- AI agents are probabilistic and may produce plausible-looking but incorrect code.
- AI agents can infer intent incorrectly when a program relies on convention, hidden state, or undocumented behavior.
- AI agents are weaker at maintaining long chains of global reasoning without frequent verification.
- AI agents can be brittle around ambiguous syntax, overloaded meanings, and context-sensitive rules.
- AI agents may hallucinate APIs, fields, invariants, or historical facts unless the environment makes truth easy to inspect.
- AI agents can overfit to nearby examples and copy accidental patterns unless the language distinguishes policy from coincidence.
- AI agents need fast, precise feedback to correct mistakes before those mistakes compound.

## Design Consequences

These traits imply the following design principles for Vyr.

- Prefer explicit structure over implicit convention.  If a fact matters to correctness, it should be represented directly in the program or in a checked specification artifact.
- Prefer readable regularity over terse cleverness.  Repetition and verbosity are acceptable when they make structure easier for agents and tools to inspect.
- Keep syntax simple and stable.  A small grammar with few context-sensitive rules reduces parser errors, misread code, and accidental ambiguity.
- Make meaning local where possible.  A module, declaration, or block should carry enough information for an agent to modify it safely without reconstructing the whole program.
- Make global effects explicit.  Imports, capabilities, mutation, I/O, concurrency, resource ownership, and unsafe operations should be visible at the boundary where they matter.
- Treat specifications as first-class program material.  Types, contracts, effects, protocols, schemas, examples, and tests should be close to the code they constrain.
- Design for mechanical verification.  The language should support deterministic parsing, formatting, type checking, linting, test discovery, and semantic validation.
- Design error messages for agents.  Diagnostics should identify the violated rule, the relevant source locations, and the smallest plausible repair.
- Make refactoring a primary workflow.  Names, declarations, module boundaries, and generated artifacts should have stable identities that tools can update safely.
- Separate intent from implementation detail.  The language should make it clear which patterns are required policy and which are incidental code shape.
- Prefer canonical forms.  Formatting, import ordering, generated code, and metadata should have one normal representation to reduce irrelevant diffs.
- Preserve provenance.  Generated code, derived files, migrations, and external bindings should say where they came from and how to regenerate or verify them.
- Optimize for inspectable state.  Build outputs, caches, package metadata, and project configuration should be explicit, versioned, and easy for agents to query.
- Keep the human audit path intact.  Vyr should be comfortable enough for humans to review, but human concision is not allowed to override agent reliability.

The central bet of Vyr is that a language for AI agents should not imitate the habits of human-first languages by default.  It should make software easier to generate, check, revise, and explain under the working conditions of agentic development.
