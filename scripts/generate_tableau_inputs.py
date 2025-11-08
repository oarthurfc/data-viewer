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

def build_q3_csvs():
    """
    RQ3: Experience profile of contributors.

    Gera dois CSVs:
    - RQ3_experience_levels_distribution.csv: resumo por nível de experiência.
    - RQ3_contributors_experience.csv: detalhado por contribuidor (para histogramas, boxplots, etc.).
    """
    q3_path = DATA_DIR / "seventh-step" / "Q3_experience_profile.json"
    with q3_path.open(encoding="utf-8") as f:
        q3 = json.load(f)

    # 1) Resumo por nível
    levels_counts = q3.get("experience_levels", {})
    levels_pct = q3.get("experience_levels_percentage", {})

    level_rows = []
    for level, count in levels_counts.items():
        pct = levels_pct.get(level, 0.0)
        level_rows.append(
            {
                "experience_level": level,
                "contributors_count": count,
                "contributors_percentage_total": round(pct, 2),
            }
        )

    # Ordena por contagem desc
    level_rows.sort(key=lambda r: r["contributors_count"], reverse=True)

    out_summary = TABLEAU_DIR / "RQ3_experience_levels_distribution.csv"
    with out_summary.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "experience_level",
                "contributors_count",
                "contributors_percentage_total",
            ],
        )
        writer.writeheader()
        writer.writerows(level_rows)

    print(f"Generated {out_summary}")

    # 2) Detalhado por contribuidor
    contributors = q3.get("contributors", [])

    out_contributors = TABLEAU_DIR / "RQ3_contributors_experience.csv"
    with out_contributors.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "login",
            "experience_level",
            "experience_score",
            "span_months",
            "active_months",
            "total_prs_created",
            "total_prs_reviewed",
            "total_issues_created",
            "total_volume",
            "roles",
            "diversity_score",
            "span_normalized",
            "regularity",
            "volume_normalized",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for c in contributors:
            writer.writerow(
                {
                    "login": c.get("login"),
                    "experience_level": c.get("experience_level"),
                    "experience_score": c.get("experience_score"),
                    "span_months": c.get("span_months"),
                    "active_months": c.get("active_months"),
                    "total_prs_created": c.get("total_prs_created"),
                    "total_prs_reviewed": c.get("total_prs_reviewed"),
                    "total_issues_created": c.get("total_issues_created"),
                    "total_volume": c.get("total_volume"),
                    "roles": ",".join(c.get("roles", [])),
                    "diversity_score": c.get("diversity_score"),
                    "span_normalized": c.get("span_normalized"),
                    "regularity": c.get("regularity"),
                    "volume_normalized": c.get("volume_normalized"),
                }
            )

    print(f"Generated {out_contributors}")

def build_q4_csv():
    """
    RQ4: Effect of experience on PR approval.
    Gera um CSV com métricas por nível de experiência.
    """
    q4_path = DATA_DIR / "seventh-step" / "Q4_experience_approval_effect.json"
    with q4_path.open(encoding="utf-8") as f:
        q4 = json.load(f)

    rows = []
    for level, stats in q4.items():
        rows.append(
            {
                "experience_level": level,
                "total_prs": stats.get("total_prs", 0),
                "approved_prs": stats.get("approved_prs", 0),
                "approval_rate": stats.get("approval_rate", 0.0),
                "approval_percentage": round(
                    stats.get("approval_percentage", 0.0), 2
                ),
                "contributors_count": stats.get("contributors_count", 0),
            }
        )

    # Mantém a ordem lógica dos níveis, se existirem
    order = {"Initial": 0, "Intermediate": 1, "Advanced": 2}
    rows.sort(key=lambda r: order.get(r["experience_level"], 99))

    out_path = TABLEAU_DIR / "RQ4_experience_approval_effect.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "experience_level",
                "total_prs",
                "approved_prs",
                "approval_rate",
                "approval_percentage",
                "contributors_count",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out_path}")

def build_q5_csv():
    """
    RQ5: Relationship between experience level and contribution frequency.
    Gera um CSV com estatísticas por nível de experiência.
    """
    q5_path = DATA_DIR / "seventh-step" / "Q5_experience_frequency_correlation.json"
    with q5_path.open(encoding="utf-8") as f:
        q5 = json.load(f)

    rows = []
    for level, stats in q5.items():
        total_prs_stats = stats.get("total_prs_stats", {})
        interval_stats = stats.get("avg_interval_stats", {})

        rows.append(
            {
                "experience_level": level,
                "contributors_count": stats.get("contributors_count", 0),
                "total_prs_sum": total_prs_stats.get("sum", 0),
                "total_prs_mean": total_prs_stats.get("mean", 0.0),
                "total_prs_median": total_prs_stats.get("median", 0.0),
                "avg_interval_mean_days": interval_stats.get("mean_days", 0.0),
                "avg_interval_median_days": interval_stats.get("median_days", 0.0),
                "contributors_with_intervals": interval_stats.get(
                    "contributors_with_intervals", 0
                ),
            }
        )

    order = {"Initial": 0, "Intermediate": 1, "Advanced": 2}
    rows.sort(key=lambda r: order.get(r["experience_level"], 99))

    out_path = TABLEAU_DIR / "RQ5_experience_frequency_correlation.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "experience_level",
                "contributors_count",
                "total_prs_sum",
                "total_prs_mean",
                "total_prs_median",
                "avg_interval_mean_days",
                "avg_interval_median_days",
                "contributors_with_intervals",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out_path}")

def main():
    ensure_output_dir()
    build_q1_csv()
    build_q2_csv()
    build_q3_csvs()
    build_q4_csv()
    build_q5_csv()


if __name__ == "__main__":
    main()
#python -m scripts.generate_tableau_inputs