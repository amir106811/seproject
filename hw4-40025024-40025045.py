import csv

class Product:
    def __init__(self, id, name, type, price, available, rating):
        self.id = int(id)
        self.name = name
        self.type = type
        self.price = float(price)
        self.available = bool(int(available))
        self.rating = float(rating)

def load_products(file_path):
    products = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product = Product(**row)
            products[product.id] = product
    return products

def read_wallet(file_path):
    with open(file_path, 'r') as file:
        line = file.readline()
        return float(line.split(':')[1].strip())

def update_wallet(file_path, new_balance):
    with open(file_path, 'w') as file:
        file.write(f"wallet: {new_balance}")

def add_to_cart(products, product_id):
    if not product_id.isdigit():
        raise ValueError("Only enter numbers!")
    
    product_id = int(product_id)
    if product_id not in products:
        raise ValueError("No product found!")
    
    product = products[product_id]
    if not product.available:
        raise ValueError("The product is not available at the moment!")
    
    return product

def checkout(wallet_balance, product):
    if wallet_balance < product.price:
        raise ValueError("Not enough money!")
    
    wallet_balance -= product.price
    print(f"Payment successful! \nProduct: {product.name} \nPrice: {product.price}")
    return wallet_balance

def main():
    products = load_products('products.csv')
    wallet_balance = read_wallet('user_wallet.txt')
    
    while True:
        print("\nEnter the ID of the product to add to your cart (or 'exit' to quit):")
        product_id = input().strip()
        
        if product_id.lower() == 'exit':
            break
        
        try:
            product = add_to_cart(products, product_id)
            print(f"Product: {product.name} \nType: {product.type} \nPrice: {product.price}")
            
            print("\nDo you want to checkout? (yes/no):")
            choice = input().strip().lower()
            
            if choice == 'yes':
                wallet_balance = checkout(wallet_balance, product)
                update_wallet('user_wallet.txt', wallet_balance)
                print(f"Remaining wallet balance: {wallet_balance}")
        
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
