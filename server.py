from flask import Flask, request
from flask_restful import Api, Resource


import random
import math

# Taking Inputs
lower = 1
 
# Taking Inputs
upper = 10
 
# generating random number between
# the lower and upper
x = random.randint(lower, upper)
print("\n\tYou've only ",
       round(math.log(upper - lower + 1, 2)),
      " chances to guess the integer!\n")
 
# Initializing the number of guesses.
count = 1

 
# for calculation of minimum number of
# guesses depends upon range
"""
while count < math.log(upper - lower + 1, 2):
    count += 1
 
    # taking guessing number as input
    guess = int(input("Guess a number:- "))
 
    # Condition testing
    if x == guess:
        print("Congratulations you did it in ",
              count - 1, " try")
        # Once guessed, loop will break
        break
    elif x > guess:
        print("You guessed too small!")
    elif x < guess:
        print("You Guessed too high!")
"""

 
# If Guessing is more than required guesses,
# shows this output.
if count >= math.log(upper - lower + 1, 2):
    print("\nThe number is %d" % x)
    print("\tBetter Luck Next time!")
# Create a Flask object and an Api object.
app = Flask(__name__)
"""
<div>Guess Number:</div>
<form method="post">
<input type="text" name = "guess"/>
<input type="submit" name = "submit"/>
</form>"""
@app.route("/guess",methods=['POST','GET'])
def newHome():
    if request.method == 'POST':
        guess = request.form['guess']
        if guess == x:
            return "Congratulations!"
        else:
            count+=1
            if(count > 3):
                return "Game Over. The number was: " + x
            return "Try Again :(" + 3-count + "guesses remaining"
            
        return guess
    else:
        return """<h2 style='color:red'>Random Number Generator Game!</h2>
        <div> Number: {x} </div> 
        <div>Guess Number:</div>
        <form method="post">
        <input type="text" name = "guess"/>
        <input type="submit" name = "submit"/>
        </form>
        """.format(x=x)
@app.route('/')
def home():
    return """<h2 style='color:red'>Random Number Generator Game!</h2>
    <div>Guess Number:</div>
    <input type="text" name = "guess"/>
    <input type="submit" name = "submit"
    """
api = Api(app)

# Create some sample data (a list of Product objects).
products = [
    {
        "id": 0,
        "description": "Swansea City shirt",
        "price": 55,
        "unitsInStock": 500
    },
    {
        "id": 1,
        "description": "Cardiff City shirt",
        "price": 1.99,
        "unitsInStock": 20000
    },
    {
        "id": 2,
        "description": "Bugatti Divo",
        "price": 4000000,
        "unitsInStock": 2
    },
    {
        "id": 3,
        "description": "Carving Skis",
        "price": 350,
        "unitsInStock": 75
    },
    {
        "id": 4,
        "description": "Ski Boots",
        "price": 150,
        "unitsInStock": 150
    },
    {
        "id": 5,
        "description": "55in OLED HDTV",
        "price": 1800,
        "unitsInStock": 100
    },
]

# Handy counter, useful for generating a new ID every time the user "inserts" a new product.
nextId = 6

# Define a class that inherits from Resource.
class Product(Resource):

    # Define a method to handle GET requests. 
    #   E.g. GET  /api/Products - Returns all products.
    #   E.g. GET  /api/Products/2 - Returns a single product with specified id, or a 404 error.
    def get(self, id=None):
        if id is None:
            return products, 200
        else:
            for product in products:
                if (id == product["id"]):
                    return product, 200
            return "Product not found", 404
        
    # Define a method to handle POST requests.
    #   E.g. POST /api/Products    
    # We extract the product from the incoming HTTP request body (as JSON).
    # Then we add the product to our list of products.
    # Then we return the product, enriched with its newly generated id.
    def post(self):
        global nextId
        json_data = request.get_json(force=True)           
        product = {
            "id":  nextId, 
            "description": json_data["description"],
            "price": json_data["price"],
            "unitsInStock": json_data["unitsInStock"]
        }
        products.append(product)
        nextId += 1
        return product, 201

    # Define a method to handle PUT requests: 
    #   E.g. PUT /api/Products/2       
    # We extract the updated product state from the incoming HTTP request body (as JSON).
    # Then we find and modify the existing product in our list of products.
    # Then we return the product.
    def put(self, id):
        json_data = request.get_json(force=True)
        for product in products:
            if (id == product["id"]):
                product["description"] = json_data["description"]
                product["price"] = json_data["price"]
                product["unitsInStock"] = json_data["unitsInStock"]
                return product, 200
        return "Product not found", 404

    # Define a method to handle DELETE requests: 
    #   E.g. DELETE /api/Products/2    
    # We find and delete the existing product in our list of products.
    def delete(self, id):
        for index, product in enumerate(products):
            if (id == product["id"]):
                products.pop(index)
                return "Product deleted", 200
        return "Product not found", 404

# Register our Product class against whatever URL patterns we want to support.      
api.add_resource(Product, "/api/Products", "/api/Products/<int:id>", "/api/guess/<int:guess>")

# Start the applictaion.
if __name__ == '__main__':
    app.run(host='0.0.0.0')