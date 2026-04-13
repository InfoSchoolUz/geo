def preprocess(data):
    for c in data:
        pop = c.get("population") or 0
        area = c.get("area") or 0
        density = pop / area if area else 0

        c["density"] = density

        if density > 300:
            c["insight"] = "⚠️ Overpopulated"
        elif density < 50:
            c["insight"] = "🌱 Sparse"
        else:
            c["insight"] = "✅ Balanced"

    return data
