import pandas as pd
from json import loads


url = "https://maven-datasets.s3.us-east-1.amazonaws.com/Data+Drills/sales_orders.csv"
# read data
data = pd.read_csv(url)

# extract a value from the JSON column, and inspect
example = data.loc[0, "line_items"]
print(example)

# convert to dict
example = eval(example)[0]
print(type(example), example)

# explore the example dict
print(example.keys())

print(type(example["product"]), example["product"])
print(example["product"].keys())

# attempt to flatten json column
flat = pd.json_normalize(
    data=data
)

print(flat.head())

""" the above approach was wrong, because json_normalize accepts a json object,
not a full data frame"""

# retry with a different approach
data = pd.read_csv(url)
print(f"Data shape {data.shape}")

data["line_items"] = data["line_items"].apply(loads)

print(data.head())
print(f"data shape {data.shape}")

# reshape for one product per line
data = data.explode(column="line_items")

# now we can use pd normalize
line_items = pd.json_normalize(
    data=data["line_items"]
)

# preview the data
line_items.head()

# rename the columns
line_items.columns = ["quantity", "product_name", "product_price"]
line_items.head()


# Now join back with the original data
data.reset_index(inplace=True)

final_table = pd.concat(
    objs=[data, line_items],
    axis=1
)

assert final_table.shape[0] == data.shape[0]

# now calculate online sales total

final_table["total"] = final_table["quantity"] * final_table["product_price"]

solution = round(
    final_table[final_table["fulfillment"] == "Online"]["total"]
    .sum()
)