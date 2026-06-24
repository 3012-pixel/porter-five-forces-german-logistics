"""
Porter's Five Forces + Value Chain Analysis
German Road Freight & Logistics Industry
------------------------------------------
Author: Kumar Aditya
Purpose: Quantified strategic analysis using Porter's Five Forces and
         the Value Chain framework, applied to German road freight.

I chose German logistics for a few reasons:
  1. I worked at Spirka Technologies (logistics/supply chain) so I have
     a feel for the operational side
  2. It's a sector with real structural tension right now — driver
     shortage, fuel costs, digitalisation pressure, rail/road modal shift
  3. There's decent public data from Destatis, BGL, and the Fraunhofer ISI

The scoring is my own assessment based on industry reports, not a survey.
Sources are cited in the analysis.md file.

Outputs:
    outputs/five_forces_radar.png
    outputs/value_chain.png
    outputs/forces_breakdown.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

os.makedirs("outputs", exist_ok=True)

# ── Five Forces Scoring ────────────────────────────────────────────────────────
# Each force is scored 1–10 where 10 = highest threat / most intense
# Subscores show how I arrived at the overall score

FIVE_FORCES = {
    "Competitive Rivalry": {
        "score": 8.5,
        "direction": "HIGH THREAT",
        "color": "#e74c3c",
        "sub_scores": {
            "Number of competitors": 9,       # ~40,000 licensed hauliers in Germany
            "Industry concentration": 4,       # top 10 players hold ~25% — fragmented
            "Price competition intensity": 9,  # freight rates are nearly commoditised
            "Capacity overcapacity risk": 7,
            "Switching costs for customers": 3, # very low — spot market is liquid
        },
        "key_insight": (
            "German road freight is structurally fragmented (~40,000 licensed hauliers). "
            "Spot market pricing via digital platforms (Timocom, Transporeon) has "
            "commoditised rates. Incumbents compete mainly on reliability and relationship, "
            "but differentiation is hard to sustain."
        )
    },
    "Threat of New Entrants": {
        "score": 5.0,
        "direction": "MODERATE THREAT",
        "color": "#f39c12",
        "sub_scores": {
            "Capital requirements": 6,         # trucks are expensive, but leaseable
            "Regulatory barriers (GüKG, EU)": 7,  # carrier licence, cabotage rules
            "Economies of scale needed": 5,
            "Brand/relationship advantages": 4,
            "Digital platform disruption risk": 6,  # Sennder, Instafreight lowering barriers
        },
        "key_insight": (
            "Traditional barriers (fleet investment, carrier licence) are real but "
            "digital freight forwarders (Sennder, Instafreight) have entered with "
            "asset-light models. The real risk is platform players disintermediating "
            "traditional hauliers rather than a flood of new physical operators."
        )
    },
    "Bargaining Power of Buyers": {
        "score": 7.5,
        "direction": "HIGH THREAT",
        "color": "#e74c3c",
        "sub_scores": {
            "Buyer concentration": 7,           # automotive/retail buyers are large
            "Volume leverage": 8,
            "Switching costs": 3,               # spot market = very easy to switch
            "Price sensitivity": 9,
            "Backward integration risk": 4,     # some large retailers run own fleets
        },
        "key_insight": (
            "Large shippers (automotive OEMs, retailers, chemical companies) have "
            "significant rate leverage, especially on spot markets. Contract logistics "
            "provides slightly more stability but multi-year tenders are highly competitive. "
            "Logistics managers are under constant pressure to reduce freight cost per unit."
        )
    },
    "Bargaining Power of Suppliers": {
        "score": 6.5,
        "direction": "MODERATE-HIGH",
        "color": "#e67e22",
        "sub_scores": {
            "Truck manufacturer concentration": 5,  # Daimler, MAN, Volvo oligopoly
            "Driver shortage severity": 9,          # ~80,000 driver shortage in Germany (BGL 2023)
            "Fuel cost dependency": 8,
            "Tyre/parts supplier power": 4,
            "Alternative fuel infrastructure": 6,   # LNG/hydrogen still limited
        },
        "key_insight": (
            "The driver shortage is the single biggest supply-side constraint — "
            "BGL estimates ~80,000 unfilled driver positions in Germany as of 2023, "
            "and demographic trends will worsen this. Fuel costs (typically 28–35% "
            "of operating cost) remain exposed to oil price volatility despite some "
            "fuel surcharge clauses."
        )
    },
    "Threat of Substitutes": {
        "score": 5.5,
        "direction": "MODERATE THREAT",
        "color": "#f39c12",
        "sub_scores": {
            "Rail freight competitiveness": 6,   # improving but reliability issues
            "Inland waterway viability": 4,      # Rhine corridor significant
            "Pipeline substitution": 3,          # limited to bulk chemicals/oil
            "Short-sea shipping": 5,
            "Last-mile drone/autonomous risk": 4, # still early
        },
        "key_insight": (
            "Rail modal shift is the main substitution threat — DB Cargo and private "
            "operators are improving, and EU policy actively promotes rail. However, "
            "German rail freight suffered from reliability problems (network congestion, "
            "strikes) in 2022–2024. For time-sensitive or short-haul loads (<200km) "
            "road remains hard to replace."
        )
    },
}

# Value chain activities with scores for two profiles
# Score 1–5: how strong/differentiated is this activity?
VALUE_CHAIN = {
    "Primary Activities": {
        "Inbound Logistics\n(Fleet, Routing)": {
            "large_fleet_operator": 4,
            "digital_freight_forwarder": 2,
            "description": "Fleet management, route optimisation, driver scheduling. Where physical operators have a clear edge."
        },
        "Operations\n(Pickup & Delivery)": {
            "large_fleet_operator": 4,
            "digital_freight_forwarder": 3,
            "description": "Load execution, documentation, tracking. Increasingly standardised via TMS platforms."
        },
        "Outbound Logistics\n(Customer Delivery)": {
            "large_fleet_operator": 4,
            "digital_freight_forwarder": 3,
            "description": "On-time delivery, customer communication, proof of delivery."
        },
        "Marketing & Sales\n(Capacity Selling)": {
            "large_fleet_operator": 3,
            "digital_freight_forwarder": 5,
            "description": "Rate negotiation, customer acquisition, spot market access. Digital forwarders dominate here."
        },
        "Service\n(Claims & Support)": {
            "large_fleet_operator": 3,
            "digital_freight_forwarder": 4,
            "description": "Claim handling, tracking transparency, customer portal."
        },
    },
    "Support Activities": {
        "Firm Infrastructure\n(Admin, Finance)": {
            "large_fleet_operator": 3,
            "digital_freight_forwarder": 4,
            "description": "Compliance, accounting, legal, HR."
        },
        "HR Management\n(Driver Recruitment)": {
            "large_fleet_operator": 2,
            "digital_freight_forwarder": 5,
            "description": "The biggest operational challenge for fleet operators. Digital models largely avoid it."
        },
        "Technology\n(TMS, Tracking, Data)": {
            "large_fleet_operator": 3,
            "digital_freight_forwarder": 5,
            "description": "Where digital entrants have invested most heavily. Telematics, live tracking, automated pricing."
        },
        "Procurement\n(Fuel, Fleet, Carriers)": {
            "large_fleet_operator": 4,
            "digital_freight_forwarder": 3,
            "description": "Fleet procurement, fuel hedging, subcontractor management."
        },
    }
}


def generate_radar_chart():
    """Five Forces radar chart."""
    labels = list(FIVE_FORCES.keys())
    scores = [FIVE_FORCES[f]["score"] for f in labels]
    colors_list = [FIVE_FORCES[f]["color"] for f in labels]

    scores_plot = scores + [scores[0]]
    N = len(labels)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles_plot = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#fafafa')
    ax.set_facecolor('#fafafa')

    for level in [2, 4, 6, 8, 10]:
        ax.plot(angles_plot, [level] * (N + 1), color='#cccccc',
                linewidth=0.5, linestyle='--')

    ax.fill(angles_plot, scores_plot, color='#2980b9', alpha=0.20)
    ax.plot(angles_plot, scores_plot, color='#2980b9', linewidth=2.5)

    # plot individual score dots coloured by severity
    for angle, score, color in zip(angles, scores, colors_list):
        ax.plot(angle, score, 'o', color=color, markersize=12, zorder=5)

    ax.set_xticks(angles)
    short_labels = [
        "Competitive\nRivalry",
        "Threat of\nNew Entrants",
        "Buyer\nPower",
        "Supplier\nPower",
        "Threat of\nSubstitutes"
    ]
    ax.set_xticklabels(short_labels, size=10, color='#333333')
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], size=8, color='#888888')
    ax.set_ylim(0, 10)
    ax.set_title(
        "Porter's Five Forces\nGerman Road Freight & Logistics Industry",
        size=13, fontweight='bold', pad=30, color='#222222'
    )

    legend_items = [
        mpatches.Patch(color='#e74c3c', label='High Threat (7–10)'),
        mpatches.Patch(color='#e67e22', label='Moderate-High (5–7)'),
        mpatches.Patch(color='#f39c12', label='Moderate (4–6)'),
    ]
    ax.legend(handles=legend_items, loc='upper right',
              bbox_to_anchor=(1.35, 1.15), fontsize=9)

    plt.tight_layout()
    plt.savefig("outputs/five_forces_radar.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: outputs/five_forces_radar.png")


def generate_forces_breakdown():
    """Horizontal bar chart of sub-scores for each force."""
    fig, axes = plt.subplots(1, 5, figsize=(20, 7), sharey=False)
    fig.patch.set_facecolor('#f8f9fa')

    for ax, (force_name, force_data) in zip(axes, FIVE_FORCES.items()):
        sub_labels = list(force_data["sub_scores"].keys())
        sub_vals   = list(force_data["sub_scores"].values())
        color      = force_data["color"]

        bars = ax.barh(range(len(sub_labels)), sub_vals,
                       color=color, alpha=0.75, edgecolor='white')
        ax.set_xlim(0, 10.5)
        ax.set_yticks(range(len(sub_labels)))
        ax.set_yticklabels(sub_labels, fontsize=7.5)
        ax.set_xlabel("Score (1–10)")
        ax.set_title(f"{force_name}\n({force_data['direction']})",
                     fontsize=9, fontweight='bold', color=color)
        ax.axvline(x=force_data["score"], color='#333333',
                   linestyle='--', linewidth=1.5, label=f"Overall: {force_data['score']}")
        ax.legend(fontsize=7)
        ax.set_facecolor('#ffffff')
        ax.grid(axis='x', alpha=0.2)

    plt.suptitle("Five Forces — Sub-Score Breakdown\nGerman Road Freight & Logistics",
                 fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig("outputs/forces_breakdown.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: outputs/forces_breakdown.png")


def generate_value_chain():
    """
    Value chain comparison: large fleet operator vs digital freight forwarder.
    Shows where each business model is strong or weak.
    """
    all_activities = {}
    for category, activities in VALUE_CHAIN.items():
        for act_name, act_data in activities.items():
            all_activities[act_name] = {**act_data, "category": category}

    names      = list(all_activities.keys())
    lfo_scores = [all_activities[n]["large_fleet_operator"] for n in names]
    dff_scores = [all_activities[n]["digital_freight_forwarder"] for n in names]
    categories = [all_activities[n]["category"] for n in names]

    # Separate primary and support
    primary_idx = [i for i, n in enumerate(names) if all_activities[n]["category"] == "Primary Activities"]
    support_idx = [i for i, n in enumerate(names) if all_activities[n]["category"] == "Support Activities"]

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#ffffff')

    x = np.arange(len(names))
    width = 0.35

    bars1 = ax.bar(x - width/2, lfo_scores, width, label='Large Fleet Operator',
                   color='#2980b9', alpha=0.85, edgecolor='white')
    bars2 = ax.bar(x + width/2, dff_scores, width, label='Digital Freight Forwarder',
                   color='#e67e22', alpha=0.85, edgecolor='white')

    # vertical separator between primary and support
    ax.axvline(x=len(primary_idx) - 0.5, color='#cccccc', linestyle='--', linewidth=1.5)
    ax.text(len(primary_idx) - 0.5, 5.35, 'Support →', fontsize=8,
            color='#888888', ha='center')

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8, rotation=20, ha='right')
    ax.set_ylim(0, 5.8)
    ax.set_ylabel("Capability Strength (1–5)")
    ax.set_title("Value Chain Comparison: Fleet Operator vs Digital Freight Forwarder\nGerman Logistics Industry",
                 fontweight='bold', pad=12)

    # annotate category labels
    primary_mid = np.mean([i for i in range(len(primary_idx))])
    support_mid = np.mean([len(primary_idx) + i for i in range(len(support_idx))])
    ax.text(primary_mid, 5.5, '◀  Primary Activities  ▶',
            ha='center', fontsize=9, color='#555555', style='italic')
    ax.text(support_mid, 5.5, '◀  Support Activities  ▶',
            ha='center', fontsize=9, color='#555555', style='italic')

    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.25)

    plt.tight_layout()
    plt.savefig("outputs/value_chain.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: outputs/value_chain.png")


if __name__ == "__main__":
    print("\nGenerating Porter's Five Forces + Value Chain analysis charts...\n")
    generate_radar_chart()
    generate_forces_breakdown()
    generate_value_chain()
    print("\nDone. Open outputs/ for the charts, and see analysis.md for the written analysis.\n")
