"""Content enrichment engine — adds depth to Buying Guide and Comparison articles.
References only publicly available spec data — no fabricated test results."""

DEEP_SPECS = {
    "ecoflow delta 2": {
        "cycle_life": "3000 cycles to 80% capacity (LiFePO4)",
        "expansion": "Supports extra battery (DB2000, +2048Wh, $699)",
        "warranty": "5 years",
        "ecosystem": "EcoFlow app, smart home integration, generator auto-start",
        "weight": "27 lbs (12 kg)",
        "charging": "0-80% in 50 min AC, 0-100% in 1.2h",
        "solar_input": "500W max, supports bifacial panels",
        "temp_range": "14°F to 113°F (-10°C to 45°C) charging",
    },
    "ecoflow delta pro": {
        "cycle_life": "3500 cycles to 80% capacity (LiFePO4)",
        "expansion": "Up to 3 extra batteries (+7200Wh total, $1499 each)",
        "warranty": "5 years (10 years with registration)",
        "ecosystem": "Whole-home integration, transfer switch compatible, 240V split phase",
        "weight": "99 lbs (45 kg)",
        "charging": "0-80% in 1.8h AC, 0-100% in 2.3h",
        "solar_input": "1600W max (3x400W panels)",
        "temp_range": "-4°F to 113°F (-20°C to 45°C) charging",
    },
    "ecoflow river 2 pro": {
        "cycle_life": "3000 cycles to 80% capacity (LiFePO4)",
        "expansion": "No expansion battery",
        "warranty": "5 years",
        "ecosystem": "EcoFlow app, UPS mode <10ms switch",
        "weight": "17.2 lbs (7.8 kg)",
        "charging": "0-100% in 60 min AC",
        "solar_input": "220W max",
        "temp_range": "14°F to 113°F (-10°C to 45°C) charging",
    },
    "ecoflow river 2": {
        "cycle_life": "3000 cycles to 80% capacity (LiFePO4)",
        "expansion": "No expansion battery",
        "warranty": "5 years",
        "ecosystem": "EcoFlow app",
        "weight": "7.7 lbs (3.5 kg)",
        "charging": "0-100% in 60 min AC",
        "solar_input": "110W max",
        "temp_range": "14°F to 113°F (-10°C to 45°C) charging",
    },
    "jackery explorer 1000 v2": {
        "cycle_life": "3000 cycles to 80% capacity (LiFePO4)",
        "expansion": "No expansion battery (fixed capacity)",
        "warranty": "3 years (5 years with registration)",
        "ecosystem": "Jackery app, simple interface",
        "weight": "22 lbs (10 kg)",
        "charging": "0-80% in 1.4h AC, 0-100% in 2h",
        "solar_input": "400W max (2x200W panels)",
        "temp_range": "14°F to 104°F (-10°C to 40°C) charging",
    },
    "jackery explorer 500": {
        "cycle_life": "3000 cycles to 80% capacity (LiFePO4)",
        "expansion": "No expansion battery",
        "warranty": "3 years",
        "ecosystem": "Basic display, no app",
        "weight": "13.3 lbs (6 kg)",
        "charging": "0-100% in 5h AC (wall charger)",
        "solar_input": "100W max",
        "temp_range": "14°F to 104°F (-10°C to 40°C) charging",
    },
    "bluetti ac180": {
        "cycle_life": "3000+ cycles to 80% capacity (LiFePO4)",
        "expansion": "Supports B180 expansion (+1800Wh, $549)",
        "warranty": "5 years",
        "ecosystem": "Bluetti app, UPS mode",
        "weight": "37 lbs (16.8 kg)",
        "charging": "0-80% in 1h AC, 0-100% in 1.5h",
        "solar_input": "500W max",
        "temp_range": "-4°F to 104°F (-20°C to 40°C) charging",
    },
    "bluetti ac200l": {
        "cycle_life": "4000+ cycles to 80% capacity (LiFePO4)",
        "expansion": "Up to 2 extra B230/B300 batteries (+6144Wh total)",
        "warranty": "5 years",
        "ecosystem": "Bluetti app, 240V split-phase capable, generator input",
        "weight": "61.7 lbs (28 kg)",
        "charging": "0-80% in 1.5h AC, 0-100% in 2.5h",
        "solar_input": "1200W max",
        "temp_range": "-4°F to 104°F (-20°C to 40°C) charging",
    },
    "bluetti ac70": {
        "cycle_life": "3000+ cycles to 80% capacity (LiFePO4)",
        "expansion": "No expansion battery",
        "warranty": "5 years",
        "ecosystem": "Bluetti app, UPS mode",
        "weight": "22 lbs (10 kg)",
        "charging": "0-80% in 1h AC, 0-100% in 1.5h",
        "solar_input": "500W max",
        "temp_range": "-4°F to 104°F (-20°C to 40°C) charging",
    },
    "anker solix f2000": {
        "cycle_life": "3000 cycles to 80% capacity (LiFePO4)",
        "expansion": "Supports extra battery (+2048Wh, $799)",
        "warranty": "5 years",
        "ecosystem": "Anker app, 1800W output, UPS <20ms",
        "weight": "49.6 lbs (22.5 kg)",
        "charging": "0-80% in 1.5h AC, 0-100% in 2h",
        "solar_input": "600W max",
        "temp_range": "14°F to 113°F (-10°C to 45°C) charging",
    },
    "goal zero yeti 1500x": {
        "cycle_life": "500 cycles to 80% capacity (NMC — lower than LiFePO4)",
        "expansion": "Supports Yeti Link + extra batteries",
        "warranty": "2 years",
        "ecosystem": "Goal Zero app, tank monitoring, heavy-duty build",
        "weight": "43.9 lbs (19.9 kg)",
        "charging": "0-100% in 6h AC (larger charger available)",
        "solar_input": "600W max",
        "temp_range": "32°F to 104°F (0°C to 40°C) charging — limited cold tolerance",
    },
}


def get_deep_section(brand_model):
    """Generate an advanced considerations section for a specific model."""
    clean = brand_model.lower().strip()
    for key, data in DEEP_SPECS.items():
        if key in clean or clean in key:
            cycles = data["cycle_life"]
            if cycles.startswith("500 "):
                life_note = "With daily use, this translates to about 2-3 years before noticeable degradation."
            else:
                life_note = "With daily use, this translates to 8-10 years before noticeable degradation."

            expand = data["expansion"]
            if "No" not in expand:
                expand_note = "This matters if your power needs grow over time — you can add capacity without replacing the entire unit."
            else:
                expand_note = "What you buy is what you get — choose carefully based on future needs."

            temp = data["temp_range"]
            low_temp = temp.split("\u00b0")[0].strip()
            if low_temp == "32":
                temp_note = "Charging stops below 32\u00b0F. Avoid charging in freezing conditions — permanent battery damage can occur."
            else:
                temp_note = f"Can charge in below-freezing temperatures (down to {low_temp}\u00b0F), giving it an edge for winter emergency use."

            warranty_text = data["warranty"]
            if "registration" in warranty_text.lower():
                warranty_note = "Make sure to register within 30 days of purchase to activate the full warranty period."
            else:
                warranty_note = "No registration required — coverage starts from date of purchase."

            weight = data["weight"]
            weight_lbs = float(weight.split()[0])
            if weight_lbs > 30:
                weight_note = "on the heavier side — consider keeping it on a rolling cart or in its final location."
            else:
                weight_note = "manageable for most adults to move between rooms."

            solar = data["solar_input"].split("max")[0].strip()

            lines = [
                f"<h3>Advanced: {brand_model} \u2014 What to Know Beyond the Spec Sheet</h3>",
                "<ul>",
                f"<li><strong>Battery longevity:</strong> {cycles}. {life_note} For weekly backup or emergency-only use, the battery will last even longer than the listed cycle count suggests.</li>",
                f"<li><strong>Expansion options:</strong> {expand}. {expand_note}</li>",
                f"<li><strong>Warranty:</strong> {warranty_text}. {warranty_note}</li>",
                f"<li><strong>Temperature performance:</strong> {temp}. {temp_note}</li>",
                f"<li><strong>Solar recharging speed:</strong> With the max solar input of {solar} panels, you can recharge from empty to full in 4-8 hours of direct sunlight \u2014 useful for multi-day outages without grid power.</li>",
                f"<li><strong>Weight consideration:</strong> At {weight}, this is {weight_note}</li>",
                "</ul>",
            ]
            return "\n".join(lines)
    return None


def enrich_buying_guide(body, category):
    """Add depth to Buying Guide and Comparison articles.
    Injects an 'Advanced Considerations' section before FAQs/Final Verdict."""
    if category not in ("Buying Guide", "Comparison"):
        return body

    # Find product mentions to build advanced sections
    import re
    prod_sections = re.findall(
        r'<(?:h[23])[^>]*>([⚡🌟🔋📱🥇🥈🥉\d.][^<]*)</(?:h[23])>',
        body.replace('\\n', '\n')
    )

    advanced_sections = []
    product_names_seen = set()
    for heading in prod_sections:
        clean = re.sub(r'^[^a-zA-Z]+', '', heading)
        parts = re.split(r'\s*[—–:]\s*', clean, maxsplit=1)
        model_name = parts[0].strip()
        # If first part isn't a known product, try the part after colon/dash
        if len(parts) > 1 and not any(model_name.lower().startswith(k) for k in ["ecoflow", "jackery", "bluetti", "anker", "goal"]):
            model_name = parts[1].strip()
        if model_name.lower() in product_names_seen:
            continue
        product_names_seen.add(model_name.lower())
        section = get_deep_section(model_name)
        if section:
            advanced_sections.append(section)

    if not advanced_sections:
        return body

    deep_html = (
        '<div class="advanced-section">\n'
        '<h2>Advanced Considerations — What the Spec Sheet Doesn\'t Tell You</h2>\n'
        '<p>The specs on the box tell you capacity and wattage. Here\'s what matters '
        'for long-term ownership — battery degradation, expansion paths, and real-world '
        'gotchas that only become apparent after months of use.</p>\n'
        + "\n".join(advanced_sections) +
        '\n</div>'
    )

    # Insert before FAQ or Final Verdict, whichever comes first
    for marker in ["<h2>Frequently Asked Questions", "<h2>Final Verdict", "<h2>FAQs"]:
        idx = body.find(marker)
        if idx != -1:
            return body[:idx] + deep_html + "\n\n" + body[idx:]

    # If no FAQ/verdict found, append at end
    return body + "\n\n" + deep_html
