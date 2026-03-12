from src.week1.jaimil_db_utilities import execute

def run():
    execute(
        "UPDATE production_data SET age = -5 "
        "WHERE id IN (SELECT id FROM production_data ORDER BY RANDOM() LIMIT 5);"
    )

    execute(
        "UPDATE production_data SET hours_per_week = 200 "
        "WHERE id IN (SELECT id FROM production_data ORDER BY RANDOM() LIMIT 5);"
    )

    execute(
        "UPDATE production_data SET education_num = NULL "
        "WHERE id IN (SELECT id FROM production_data ORDER BY RANDOM() LIMIT 5);"
    )

    execute(
        "UPDATE production_data SET capital_gain = 999999 "
        "WHERE id IN (SELECT id FROM production_data ORDER BY RANDOM() LIMIT 5);"
    )

    print("Corruption injected into production_data.")

if __name__ == "__main__":
    run()