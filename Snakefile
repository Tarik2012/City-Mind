rule all:
    input:
        "data/places_no_social_clean.csv",
        "data/places_imputed_full_clean.csv",
        "tests/.pytest_passed"

rule wrangling:
    input:
        "data/places_county_2024.csv"
    output:
        "data/places_no_social_clean.csv",
        "data/places_imputed_full_clean.csv"
    shell:
        "python scripts/wrangling_final.py"

rule test:
    input:
        "data/places_no_social_clean.csv",
        "data/places_imputed_full_clean.csv"
    output:
        "tests/.pytest_passed"
    shell:
        "pytest -v && echo 'ok' > {output}"
