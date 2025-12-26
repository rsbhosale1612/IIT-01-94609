import pandas as pd

df=pd.read_csv("C:\genai\day_2\products.csv")

print(df)
print("\nEach row in clean format:")
for index, row in df.iterrows():
    print(f"ID: {row['product_id']}, Name: {row['product_name']}, Price: {row['price']}, Category: {row['category']}, Qty: {row['quantity']}")

print("Total number of rows : ",len(df))
print("Total number of products priced above 500 : \n",df[df['price']>500])
print("Average price of all products : \n",df['price'].mean())
cat = input("Enter category: ")
print("List all products belonging to a specific category (user input) : \n", df[df['category'].str.lower() == cat.lower()])
print("Total quantity of all items in stock : ", df['quantity'].sum())