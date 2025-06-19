# ==================== Product Classes ====================
class Product:
    def __init__(self, product_id, name, price, quantity_available):
        # Base product initialization
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_available = quantity_available

    # Read-only properties for encapsulation
    @property
    def product_id(self): return self._product_id

    @property
    def name(self): return self._name

    @property
    def price(self): return self._price

    @property
    def quantity_available(self): return self._quantity_available

    # Set quantity with validation
    @quantity_available.setter
    def quantity_available(self, value):
        if value >= 0:
            self._quantity_available = value

    # Reduce stock if enough quantity is available
    def decrease_quantity(self, amount):
        if 0 < amount <= self._quantity_available:
            self._quantity_available -= amount
            return True
        return False

    # Increase stock
    def increase_quantity(self, amount):
        if amount > 0:
            self._quantity_available += amount

    # Display basic product info
    def display_details(self):
        return f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, Stock: {self.quantity_available}"

# Subclass for physical products with weight
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, weight):
        super().__init__(product_id, name, price, quantity_available)
        self._weight = weight

    def display_details(self):
        return (
            f"[Physical] ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, "
            f"Stock: {self.quantity_available}, Weight: {self._weight}kg"
        )

# Subclass for digital products with download link
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, download_link):
        super().__init__(product_id, name, price, quantity_available)
        self._download_link = download_link

    def display_details(self):
        return f"[Digital] ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, Download Link: {self._download_link}"

# ==================== Cart Item Class ====================
class CartItem:
    def __init__(self, product, quantity):
        self._product = product
        self._quantity = quantity

    @property
    def product(self): return self._product

    @property
    def quantity(self): return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value >= 0:
            self._quantity = value

    # Calculate total price for this cart item
    def calculate_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return (
            f"Item: {self.product.name}, Quantity: {self.quantity}, "
            f"Price: ${self.product.price}, Subtotal: ${self.calculate_subtotal():.2f}"
        )

# ==================== Shopping Cart Class ====================
class ShoppingCart:
    TAX_RATE = 0.08  # 8% tax rate

    def __init__(self):
        self._items = {}  # key: product_id, value: CartItem
        self.catalog = self._create_sample_catalog()

    # Hardcoded catalog with 10 products
    def _create_sample_catalog(self):
        return {
            "P001": PhysicalProduct("P001", "Laptop", 999.99, 10, 2.5),
            "P002": PhysicalProduct("P002", "Smartphone", 499.99, 20, 0.3),
            "P003": PhysicalProduct("P003", "Headphones", 89.99, 15, 0.2),
            "P004": PhysicalProduct("P004", "Keyboard", 49.99, 30, 0.8),
            "P005": PhysicalProduct("P005", "Monitor", 179.99, 12, 4.0),
            "D001": DigitalProduct("D001", "Antivirus Software", 29.99, 100, "https://download.com/antivirus"),
            "D002": DigitalProduct("D002", "Photo Editor", 59.99, 100, "https://download.com/photoeditor"),
            "D003": DigitalProduct("D003", "Music Album", 9.99, 200, "https://download.com/music"),
            "D004": DigitalProduct("D004", "E-book", 14.99, 150, "https://download.com/ebook"),
            "D005": DigitalProduct("D005", "Online Course", 199.99, 50, "https://download.com/course")
        }

    # Add a product to cart
    def add_item(self, product_id, quantity):
        product = self.catalog.get(product_id)
        if not product:
            print(f"❌ Product ID '{product_id}' not found.")
            return False
        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return False
        if not product.decrease_quantity(quantity):
            print(f"❌ Not enough stock. Available: {product.quantity_available}")
            return False

        if product_id in self._items:
            self._items[product_id].quantity += quantity
        else:
            self._items[product_id] = CartItem(product, quantity)
            print(f"✅ {quantity} x '{product.name}' added to cart.")

        return True

    # Remove a product from the cart
    def remove_item(self, product_id):
        if product_id in self._items:
            product = self._items[product_id].product
            product.increase_quantity(self._items[product_id].quantity)
            del self._items[product_id]
            print(f"🗑️ Removed '{product.name}' from cart.")
            return True
        return False

    # Change quantity of a product in the cart
    def update_quantity(self, product_id, new_quantity):
        if product_id in self._items:
            item = self._items[product_id]
            product = item.product
            diff = new_quantity - item.quantity
            if diff > 0:
                if not product.decrease_quantity(diff):
                    print("❌ Not enough stock.")
                    return False
            else:
                product.increase_quantity(-diff)
            item.quantity = new_quantity
            print(f"🔁 Updated '{product.name}' to quantity {new_quantity}.")
            return True
        print("❌ Item not found in cart.")
        return False

    # Cart totals
    def get_total(self):
        return sum(item.calculate_subtotal() for item in self._items.values())

    def get_tax(self):
        return self.get_total() * self.TAX_RATE

    def get_grand_total(self):
        return self.get_total() + self.get_tax()

    # Empty all cart items
    def empty_cart(self):
        for item in list(self._items.values()):
            item.product.increase_quantity(item.quantity)
        self._items.clear()
        print("🧹 Cart emptied.")

    # Display contents of cart
    def display_cart(self):
        print("\n🛒 --- Shopping Cart ---")
        if not self._items:
            print("Cart is empty.")
        for item in self._items.values():
            print(item)
        print(f"Subtotal: ${self.get_total():.2f}")
        print(f"Tax (8%): ${self.get_tax():.2f}")
        print(f"Total: ${self.get_grand_total():.2f}\n")

    # Print available products by type
    def display_products(self):
        print("\n📦 --- Physical Products ---")
        for product in self.catalog.values():
            if isinstance(product, PhysicalProduct):
                print(product.display_details())
        print("\n💻 --- Digital Products ---")
        for product in self.catalog.values():
            if isinstance(product, DigitalProduct):
                print(product.display_details())
        print("")

    # Search for products
    def search_products(self, keyword):
        print(f"\n🔍 Search Results for '{keyword}':")
        found = False
        for product in self.catalog.values():
            if keyword.lower() in product.name.lower():
                print(product.display_details())
                found = True
        if not found:
            print("No products found.")

    # Print final checkout summary
    def checkout(self):
        print("\n🧾 --- Checkout Summary ---")
        if not self._items:
            print("Cart is empty. Nothing to checkout.")
            return
        for item in self._items.values():
            print(item)
        print(f"Subtotal: ${self.get_total():.2f}")
        print(f"Tax: ${self.get_tax():.2f}")
        print(f"Grand Total: ${self.get_grand_total():.2f}")
        print("✅ Thank you for your purchase!")
        self._items.clear()

# ==================== Console Interface ====================
def main():
    cart = ShoppingCart()
    while True:
        print("""
1. View All Products
2. Search Product by Name
3. Add to Cart
4. View Cart
5. Update Quantity
6. Remove Item
7. Empty Cart
8. Checkout
9. Exit
        """)
        choice = input("Select an option: ")
        if choice == '1':
            cart.display_products()
        elif choice == '2':
            keyword = input("Enter keyword to search: ")
            cart.search_products(keyword)
        elif choice == '3':
            pid = input("Enter product ID: ")
            try:
                qty = int(input("Enter quantity: "))
                if not cart.add_item(pid, qty):
                    print("❌ Failed to add item.")
            except ValueError:
                print("❌ Invalid quantity.")
        elif choice == '4':
            cart.display_cart()
        elif choice == '5':
            pid = input("Enter product ID to update: ")
            try:
                qty = int(input("Enter new quantity: "))
                if not cart.update_quantity(pid, qty):
                    print("❌ Update failed.")
            except ValueError:
                print("❌ Invalid quantity.")
        elif choice == '6':
            pid = input("Enter product ID to remove: ")
            if not cart.remove_item(pid):
                print("❌ Product not found in cart.")
        elif choice == '7':
            cart.empty_cart()
        elif choice == '8':
            cart.checkout()
        elif choice == '9':
            print("👋 Thank you! Exiting...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == '__main__':
    main()
