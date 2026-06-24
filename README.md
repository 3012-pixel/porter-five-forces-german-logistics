# Porter's Five Forces + Value Chain Analysis
## German Road Freight & Logistics Industry

A quantified strategic analysis of the German logistics sector using Porter's Five Forces and the Value Chain framework — with Python-generated visualisations and a full written analysis.

---

## Why This Industry

I worked at Spirka Technologies (logistics and supply chain operations) and wanted to apply strategic frameworks to a sector I'd seen from the inside. German road freight is also an interesting case right now: it has structural tension on multiple fronts simultaneously — driver shortages, digital disruption, CO₂ regulation, modal shift pressure.

The scoring is my own assessment based on public industry reports (BGL, Destatis, Fraunhofer ISI, EU Commission transport statistics) — full citations are in `analysis.md`.

---

## What's Included

| File | Description |
|---|---|
| `analysis.py` | Python script generating all three charts |
| `analysis.md` | Full written analysis (~2,500 words) with citations |
| `outputs/five_forces_radar.png` | Radar chart of all five forces (scored 1–10) |
| `outputs/forces_breakdown.png` | Sub-score breakdown for each force |
| `outputs/value_chain.png` | Value chain comparison: fleet operator vs digital forwarder |

---

## Five Forces Summary

| Force | Score (/10) | Level |
|---|---|---|
| Competitive Rivalry | 8.5 | 🔴 High |
| Buyer Power | 7.5 | 🔴 High |
| Supplier Power | 6.5 | 🟠 Moderate-High |
| Threat of Substitutes | 5.5 | 🟡 Moderate |
| Threat of New Entrants | 5.0 | 🟡 Moderate |

**Overall: Structurally challenging industry.** High rivalry + high buyer power squeeze margins from both sides. Supplier power (driven by the driver shortage) adds cost pressure from above. Viable as a business, but competitive advantage needs to be built deliberately — scale, specialisation, or digital capability.

---

## Value Chain: The Key Contrast

The analysis compares two business models competing in the same industry:
- **Large Fleet Operator** (asset-heavy, owns trucks, employs drivers)
- **Digital Freight Forwarder** (asset-light, aggregates subcontractors, platform-based)

The most interesting finding: digital forwarders have a clear technology and customer-facing advantage, but they depend entirely on subcontractor execution quality. Fleet operators have the operational depth but are losing the technology and sales efficiency battle.

---

## Sample Charts

### Five Forces Radar
![Five Forces Radar](outputs/five_forces_radar.png)

### Value Chain Comparison
![Value Chain](outputs/value_chain.png)

### Sub-Score Breakdown
![Forces Breakdown](outputs/forces_breakdown.png)

---

## Quick Start

```bash
pip install matplotlib numpy
python analysis.py
```

Charts are saved to `outputs/`. Read the full written analysis in `analysis.md`.

---

## Skills Used
`Python` · `Matplotlib` · `Porter's Five Forces` · `Value Chain Analysis` · `Industry Research` · `Strategic Frameworks` · `German Logistics Sector`
