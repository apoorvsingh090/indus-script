# Outreach template — external epigrapher/linguist reviewer

Planner §5 Phase 0 asks for at least one external epigrapher or linguist as
a reviewer. This template is for that ask. Keep it short, honest about what
we do and do not claim, and link the two documents any reviewer must read
first. Do not promise authorship, payment, or endorsement without agreement.

---

Subject: Requesting skeptical review of a verification-first Indus script repo

Dear Prof. / Dr. <name>,

We maintain a small public repository (github.com/apoorvsingh090/indus-script)
that tests claims about the Indus script under a strict reproduction
protocol: every claim ships its data pipeline, a readable checker, a frozen
baseline, and pre-registered thresholds; nothing is counted until two
independent skeptics rebuild it from raw inputs. We explicitly do NOT claim
the script is deciphered, and we treat machine-produced readings as
hypotheses to be scored, never as evidence.

Recent results include: replications of Rao et al. (2009) structural entropy
and Adhikari-style positional/n-gram findings on a public corpus; a
sign-code concordance (Mahadevan/Parpola/Wells) with contested cases
listed; and a calibration ladder showing which methods recover known
answers at Indus-scale data sizes — including confirmed negatives (e.g.
substitution-key recovery from an equal-size reference fails as configured;
report + mechanism published).

What we would value from you (a few hours, asynchronous, any medium):
- a look at `READ_BEFORE_CITING.md` and `TROPHY_CASE.md` (one sitting);
- an opinion on whether our L0 corpus/concordance handling (dedup,
  completeness, contested sign splits) matches epigraphic practice;
- any structural claim you consider worth testing that we have missed,
  or any of ours you consider mis-stated. Public comments via GitHub
  Discussions are ideal, but private email is fine too.

We will credit reviews in the repo (as detailed as you permit) and will
not cite your name as endorsement of any result — only as review.

Thank you for considering it.

<sender>

---

Before sending: adapt the "recent results" paragraph to the current
TROPHY_CASE.md; never send numbers not yet skeptic-verified. If the
reviewer's work is among what we replicated or critiqued (e.g. Rao 2009,
Nair 2026), say so explicitly in the email and offer to relay any reply
they want on record.
