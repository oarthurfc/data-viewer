import json
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TABLEAU_DIR = DATA_DIR / "tableau"


def ensure_output_dir():
    TABLEAU_DIR.mkdir(exist_ok=True)


def build_q1_csv():
    """
    RQ1: Geographical distribution of contributors.
    Gera um CSV com país, contagem e % sobre o total de contribuidores.
    """
    q1_path = DATA_DIR / "seventh-step" / "Q1_geographical_distribution.json"
    with q1_path.open(encoding="utf-8") as f:
        q1 = json.load(f)

    total = q1.get("total_contributors", 0)
    countries = q1.get("countries", {})

    rows = []
    for country, count in countries.items():
        if country == "Unknown":
            continue

        percentage = (count / total * 100) if total else 0.0
        rows.append({
            "country": country,
            "contributors_count": count,
            "contributors_percentage_total": round(percentage, 2)
        })

    # Ordena do maior para o menor
    rows.sort(key=lambda r: r["contributors_count"], reverse=True)

    out_path = TABLEAU_DIR / "RQ1_geographical_distribution.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["country", "contributors_count", "contributors_percentage_total"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out_path}")


def build_q2_csv():
    """
    RQ2: Professional affiliation.
    Gera um CSV com empresa, contagem, %, e uma categoria (Company/Organization x Independent/Unknown).
    """
    q2_path = DATA_DIR / "seventh-step" / "Q2_professional_affiliation.json"
    with q2_path.open(encoding="utf-8") as f:
        q2 = json.load(f)

    total = q2.get("total_contributors", 0)
    companies = q2.get("companies", {})

    rows = []
    for company, count in companies.items():
        name_lower = company.lower()
        if "independent" in name_lower or "unknown" in name_lower:
            category = "Independent/Unknown"
        else:
            category = "Company/Organization"

        percentage = (count / total * 100) if total else 0.0

        rows.append({
            "company": company,
            "contributors_count": count,
            "contributors_percentage_total": round(percentage, 2),
            "affiliation_category": category
        })

    # Ordena do maior para o menor
    rows.sort(key=lambda r: r["contributors_count"], reverse=True)

    out_path = TABLEAU_DIR / "RQ2_professional_affiliation.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "company",
                "contributors_count",
                "contributors_percentage_total",
                "affiliation_category"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out_path}")


def main():
    ensure_output_dir()
    build_q1_csv()
    build_q2_csv()


if __name__ == "__main__":
    main()
#python -m scripts.generate_tableau_inputs