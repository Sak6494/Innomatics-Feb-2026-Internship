from fastapi import FastAPI,Query

 

app = FastAPI()

 

# ── Temporary data — acting as our database for now ──────────

products = [

    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },

    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },

    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },

    {'id': 5, 'name': 'Laptop Stand ',     'price':  300, 'category': 'Electronics',  'in_stock': True },
    {'id': 6, 'name': 'Mechanical Keyboard',     'price':  1270, 'category': 'Electronics',  'in_stock': True },
    {'id': 7, 'name': 'Webcam',     'price':  2000, 'category': 'Electronics',  'in_stock': False}

    
    

]

 

# ── Endpoint 0 — Home ────────────────────────────────────────

@app.get('/')

def home():

    return {'message': 'Welcome to our E-commerce API'}

 

# ── Endpoint 1 — Return all products ──────────────────────────

# @app.get('/products')

# def get_all_products():

#     return {'products': products, 'total': len(products)}

# @app.get('/products/filter')

# def filter_products(

#     category:  str  = Query(None, description='Electronics or Stationery'),

#     max_price: int  = Query(None, description='Maximum price'),

#     in_stock:  bool = Query(None, description='True = in stock only')

# ):

#     result = products          # start with all products

 

#     if category:

#         result = [p for p in result if p['category'] == category]

 

#     if max_price:

#         result = [p for p in result if p['price'] <= max_price]

 

#     if in_stock is not None:

#         result = [p for p in result if p['in_stock'] == in_stock]

 

#     return {'filtered_products': result, 'count': len(result)}






 


#------Endpoint 3-Return only electronic products--
@app.get('/products/category/{category_name}')
def category(category_name:str):
    result =[p for p in products if p["category"]==category_name] 
    if not result:
             return {"error": "No products found in this category"}


    return {"category": category_name, "products": result, "total": len(result)}





#------Endpoint 4-Return only available products--
@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p.get("in_stock") is True]
    return {
        "in_stock_products": available,
        "count": len(available)
    }
#------Endpoint 5-Return summary of products products--
@app.get("/store/summary") 
def store_summary(): 
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count 
    categories = list(set([p["category"] for p in products])) 
    return { "store_name": "My E-commerce Store", "total_products": len(products), "in_stock": in_stock_count, "out_of_stock": out_stock_count, "categories": categories, }



#------Endpoint 6-Return  products Name--
@app.get("/products/search/{keyword}") 
def search_products(keyword: str): 
    results = [ p for p in products if keyword.lower() in p["name"].lower() ] 
    if not results: 
        return {"message": "No products matched your search"} 
    return {"keyword": keyword, "results": results, "total_matches": len(results)}



# ── Endpoint 2 — Return one product by its ID ──────────────────

# @app.get('/products/{product_id}')

# def get_product(product_id: int):

#     for product in products:

#         if product['id'] == product_id:

#             return {'product': product}

#     return {'error': 'Product not found'}


#Assigment 2
#-------Endpoint:/products/filter---
@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description='Electronics or Stationery'),
    min_price: int = Query(None, description='Minimum price'),
    max_price: int = Query(None, description='Maximum price'),
    in_stock: bool = Query(None, description='True = in stock only')
):

    result = products

    if category:
        result = [p for p in result if p['category'] == category]

    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]

    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {"filtered_products": result, "count": len(result)}
#----Endpoint:/products/{product_id}/price---
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }
    
    return {"error": "Product not found"}


from pydantic import BaseModel, Field
from typing import Optional
feedback = []
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }

@app.get("/products/summary")
def product_summary():
    in_stock   = [p for p in products if     p["in_stock"]]
    out_stock  = [p for p in products if not p["in_stock"]]
    expensive  = max(products, key=lambda p: p["price"])
    cheapest   = min(products, key=lambda p: p["price"])
    categories = list(set(p["category"] for p in products))
    return {
        "total_products":     len(products),
        "in_stock_count":     len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive":     {"name": expensive["name"], "price": expensive["price"]},
        "cheapest":           {"name": cheapest["name"],  "price": cheapest["price"]},
        "categories":         categories,
    }