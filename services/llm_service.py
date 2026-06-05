from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from .model_to_dict_stackoverflow import model_to_dict
load_dotenv()

llm = ChatGroq(
    model='meta-llama/llama-4-scout-17b-16e-instruct',
    temperature=0.2
)

prompt = PromptTemplate.from_template(
    """
Your are Product suggester 

you have details of users past data based on that give product suggesstion 
{orders}

Listed product on Platform
{products}

RULE:
- always respond something 
- if not possible state a reason why you cant give suggestions
- Suggessted product should be available in products 
- dont give products by own 
- give only products which is listed on platform
- suggesstion should be based on price 
- suggesstion based on users past order category 
- suggestion should be based on users most ordered things 
- Only suggest 5-6 product if not then suggest something less but suggest   
- if there is no past orders then show product by your own 
- response should be in strict JSON
- validate response 2 times 


FOLLOW STRICTLY FORMAT DONT ADD SOMETHING EXTRA IN JSON
response format:
{{
    "id":"Product_id",
    "Product_name":"name of product",
    "reason":"why this product"
}}

FOLLOW STRICTLY FORMAT DONT ADD SOMETHING EXTRA IN JSON
"""
)

chain = prompt | llm | JsonOutputParser()



def ai_suggessions(products,orders):
    length = len(orders)
    order_dict = model_to_dict(orders[length-1][0]['product'])
    all_products = []
    for i in range(len(products)):
        product_dict = model_to_dict(products[i])
        all_products.append(product_dict)
    
    return chain.invoke({"orders":order_dict,"products":all_products})
