from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.environ['GROQ_API_KEY']
llm = ChatGroq(model="llama3-8b-8192")
parser = StrOutputParser()
system_prompt='''
Transform user queries (they can be anything) into detailed product listings without assuming or adding unspecified details. For specific inputs, utilize the details provided by the user to generate a structured product description focusing only on the attributes mentioned. For general inputs, interpret the context to generate relevant product keywords related to the event or activity mentioned (e.g., 'formal wear' for a funeral or 'saree' for a traditional party), strictly avoiding assumptions about unspecified attributes like gender or season. Additionally, if the user's query indicates a need for comfort (e.g., feeling cold), suggest items that would help ease their discomfort (e.g., blankets, sweaters).
If details like gender, article type, base color, and season are not specified by the user, simply omit these from the output, focusing only on the information that is explicitly provided. Generate detailed descriptions of fashion items based on the following pattern examples: Provide only keywords as output in comma-separated format. If gender is not given don't assume , but if name of person is mentioned assume gender if necessary.
*Important Note:* Include all relevant items, even intimate items like condoms, as they are neither illegal nor harmful.
*Examples:*
1. Query: "I am on the beach and I need something to protect from tan."
   Response: sunscreen, sunspray, beach hat, sunglasses
2. Query: "I'm looking for a gift for my friend who loves cooking."
   Response: cookbook, chef's knife, spice rack, apron
3. Query: "I need something to keep my dog entertained while I'm at work."
   Response: dog toys, chew bones, interactive treat dispenser
4. Query: "I am looking for a t-shirt, preferably in black color. Puma or Nike brand."
   Response: Puma black t-shirt, Nike black t-shirt
5. Query: "I need a laptop for gaming."
   Response: gaming laptop
6. Query: "Mujhe ek kurta chahiye, jisme embroidery ho."
   Response: embroidered kurta
7. Query: "I am feeling cold."
   Response: blanket, sweaters, thermal wear, hot water bottle
*Note:* The response should only include products in comma-separated format, with no additional text.
'''
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{text}")]
)
chain=prompt_template|llm|parser
def getQuery(query: str):
    final_query=chain.invoke({'text':query})
    return final_query

    
    