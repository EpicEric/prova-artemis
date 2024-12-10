from datetime import date as dt, timedelta


def reconcile_accounts(
    transactions_1: list[list[str]], transactions_2: list[list[str]]
):
    out_2 = [[*transaction, "MISSING"] for transaction in transactions_2]
    # Create dict for efficient lookups
    transactions_2_map = {}
    for index, transaction in enumerate(transactions_2):
        date = dt.fromisoformat(transaction[0])
        key = (
            date,
            transaction[1],
            transaction[2],
            transaction[3],
        )
        transactions_2_map[key] = index

    out_1 = []
    for transaction in transactions_1:
        date = dt.fromisoformat(transaction[0])
        found = False
        # Check previous date first, then current date, then next date
        for possible_date in [
            date - timedelta(days=1),
            date,
            date + timedelta(days=1),
        ]:
            possible_key = (
                possible_date,
                transaction[1],
                transaction[2],
                transaction[3],
            )
            match = transactions_2_map.get(possible_key)
            if match is not None and out_2[match][4] == "MISSING":
                out_2[match][4] = "FOUND"
                del transactions_2_map[possible_key]
                found = True
                break
        out_1.append([*transaction, "FOUND" if found else "MISSING"])

    return out_1, out_2
