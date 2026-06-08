# SHOP INVENTORY MANAGEMENT SYSTEM
# Using Product and Sales Dictionaries
products = {
    "Pen": 100,
    "Book": 50,
    "Pencil": 80,
    "Eraser": 40,
    "Notebook": 30
}

# Sales Dictionary (5 Records)
sales = {
    "Pen": 20,
    "Book": 10,
    "Pencil": 15,
    "Eraser": 5,
    "Notebook": 8
}

while True:
    print("\n=================================")
    print("      SHOP INVENTORY SYSTEM")
    print("=================================")
    print("1. Display Product Stock")
    print("2. Display Sales Record")
    print("3. Add New Product")
    print("4. Update Product Stock")
    print("5. Sell Product")
    print("6. Search Product")
    print("=================================")

    choice = int(input("Enter your choice: "))

    # Display Product Stock
    if choice == 1:
        print("\nPRODUCT STOCK DETAILS")
        print("----------------------")
        for product, stock in products.items():
            print(product, ":", stock)

    # Display Sales Record
    elif choice == 2:
        print("\nSALES RECORD")
        print("----------------------")
        for product, sold in sales.items():
            print(product, ":", sold)

    # Add New Product
    elif choice == 3:
        pname = input("Enter Product Name: ")
        qty = int(input("Enter Stock Quantity: "))

        if pname in products:
            print("Product already exists!")
        else:
            products[pname] = qty
            sales[pname] = 0
            print("Product Added Successfully.")

    # Update Product Stock
    elif choice == 4:
        pname = input("Enter Product Name: ")
        if pname in products:
            qty = int(input("Enter New Stock Quantity: "))
            products[pname] = qty
            print("Stock Updated Successfully.")
        else:
            print("Product Not Found!")
    # Sell Product
    elif choice == 5:
        pname = input("Enter Product Name: ")
        if pname in products:
            qty = int(input("Enter Quantity to Sell: "))

            if qty <= products[pname]:
                products[pname] -= qty
                sales[pname] += qty

                print("Product Sold Successfully.")
                print("Remaining Stock =", products[pname])
            else:
                print("Insufficient Stock!")
        else:
            print("Product Not Available!")

    # Search Product
    elif choice == 6:
        pname = input("Enter Product Name to Search: ")

        if pname in products:
            print("\nProduct Found")
            print("Stock Available :", products[pname])
            print("Total Sold      :", sales[pname])
        else:
            print("Product Not Found!")