import pandas as pd

df = pd.read_csv("week.csv")
print(df)

df['sell_indicator'] = 0
df['buy_indicator'] = 0

running_buy = 0
running_sell = 0

# Loop through the DataFrame rows using iterrows()
for index, row in df.iterrows():
    # Skip the first row as there is no previous row to compare
    if index == 0:
        continue

    # Apply your custom logic here
    net = row['Close'] - row['Open']

    if (net >= 0) and (net > running_buy):
        df.at[index, 'buy_indicator'] = 1
        running_buy = net
        running_sell = 0
    if (net < 0) and (net < running_sell):
        df.at[index, 'sell_indicator'] = 1
        running_sell = net
        running_buy = 0

df.to_csv("week.csv", index=False)