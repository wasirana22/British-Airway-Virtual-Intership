import pandas as pd

file_path = 'British Airways Summer Schedule Dataset - Forage Data Science Task 1.xlsx'
sheet_name = 'british_airways_schedule_summer'
df = pd.read_excel(file_path, sheet_name=sheet_name)

df["TOTAL_ELIGIBLE_PAX"] = df["TIER1_ELIGIBLE_PAX"] + df["TIER2_ELIGIBLE_PAX"] + df["TIER3_ELIGIBLE_PAX"]


df = df[df["TOTAL_ELIGIBLE_PAX"] > 0].copy()

df["TIER1_PERCENT"] = (df["TIER1_ELIGIBLE_PAX"] / df["TOTAL_ELIGIBLE_PAX"]) * 100
df["TIER2_PERCENT"] = (df["TIER2_ELIGIBLE_PAX"] / df["TOTAL_ELIGIBLE_PAX"]) * 100
df["TIER3_PERCENT"] = (df["TIER3_ELIGIBLE_PAX"] / df["TOTAL_ELIGIBLE_PAX"]) * 100


bins = [0, 10, 30, 60, 100]
labels = ["0-10%", "10-30%", "30-60%", "60-100%"]

df["TIER1_GROUP"] = pd.cut(df["TIER1_PERCENT"], bins=bins, labels=labels, include_lowest=True)
df["TIER2_GROUP"] = pd.cut(df["TIER2_PERCENT"], bins=bins, labels=labels, include_lowest=True)
df["TIER3_GROUP"] = pd.cut(df["TIER3_PERCENT"], bins=bins, labels=labels, include_lowest=True)


lookup_table = {
    "TIER1": df.groupby("TIER1_GROUP")["TIER1_ELIGIBLE_PAX"].sum(),
    "TIER2": df.groupby("TIER2_GROUP")["TIER2_ELIGIBLE_PAX"].sum(),
    "TIER3": df.groupby("TIER3_GROUP")["TIER3_ELIGIBLE_PAX"].sum()
}


lookup_df = pd.DataFrame(lookup_table).fillna(0).astype(int)


print("Lounge Eligibility Lookup Table:")
print(lookup_df)


lookup_df.to_excel("lounge_eligibility_lookup_table.xlsx")
