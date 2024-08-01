import torch
import clip
from PIL import Image
# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
# Detailed and descriptive list of items
detailed_items = [
    'Shirts', 'Tshirts', 'Jeans', 'Trousers', 'Track Pants', 'Shorts', 'Skirts', 'Dresses', 'Sarees', 'Kurtas', 'Lehenga Choli', 
    'Salwar Kameez', 'Dupatta', 'Tops', 'Sweatshirts', 'Hoodies', 'Blazers', 'Suits', 'Jackets', 'Coats', 'Loungewear', 'Nightwear', 
    'Bras', 'Briefs', 'Boxers', 'Panties', 'Innerwear Vests', 'Camisoles', 'Shapewear', 'Footwear', 'Casual Shoes', 'Sports Shoes', 
    'Formal Shoes', 'Sandals', 'Slippers', 'Boots', 'Heels', 'Flip Flops', 'Socks', 'Belts', 'Watches', 'Sunglasses', 'Bags', 
    'Handbags', 'Backpacks', 'Wallets', 'Clutches', 'Jewellery', 'Earrings', 'Necklaces', 'Bracelets', 'Rings', 'Accessories', 
    'Scarves', 'Ties', 'Hats', 'Caps', 'Gloves', 'Perfumes', 'Deodorants', 'Makeup', 'Lipstick', 'Foundation', 'Eyeliner', 
    'Mascara', 'Nail Polish', 'Face Cream', 'Body Lotion', 'Hair Care', 'Skin Care', 'Sportswear', 'Athletic Wear', 'Swimwear', 
    'Ethnic Wear', 'Formal Wear', 'Casual Wear'
]
# Other attributes
color = ['Navy Blue', 'Blue', 'Silver', 'Black', 'Grey', 'Green', 'Purple', 'White', 'Beige', 'Brown', 'Bronze',
         'Teal', 'Copper', 'Pink', 'Off White', 'Maroon', 'Red', 'Khaki', 'Orange', 'Coffee Brown', 'Yellow',
         'Charcoal', 'Gold', 'Steel', 'Tan', 'Multi', 'Magenta', 'Lavender', 'Sea Green', 'Cream', 'Peach', 'Olive',
         'Skin', 'Burgundy', 'Grey Melange', 'Rust', 'Rose', 'Lime Green', 'Mauve', 'Turquoise Blue', 'Metallic',
         'Mustard', 'Taupe', 'Nude', 'Mushroom Brown', 'Unknown', 'Fluorescent Green']
brand = ['Dior', 'Versace', 'Ugg', 'Puma', "Levi's", 'Nike', 'Dolce & Gabbana', 'Vans', 'Skechers', 
         'Converse', 'Citizen', 'Calvin Klein', 'Swarovski', 'Tommy Hilfiger', 'Timberland', 'Aldo', 
         'Armani', 'Hugo Boss', 'Zara', 'Adidas', 'Oakley', 'Guess', 'Reebok', 'Ralph Lauren', 
         'Clarks', 'Crocs', 'Fossil', 'Burberry', 'ASICS', 'Bata', 'Valentino', 'Salomon', 
         'New Balance', 'Ray-Ban', 'Casio', 'Unknown']
gender = ['Men', 'Women', 'Boy', 'Girl', 'Unisex']
lists = [color, brand, detailed_items, gender]
def getImageCaptions(path):
    # Input for the image file path
    image_path = path
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    # Preprocess the image
    image_input = preprocess(image).unsqueeze(0).to(device)
    best_descriptions = []
    for text_descriptions in lists:
        # Tokenize the text descriptions
        text_inputs = clip.tokenize(text_descriptions).to(device)
        # Calculate feature vectors
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            text_features = model.encode_text(text_inputs)
        # Normalize the feature vectors
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        # Calculate the similarity between the image and each description
        similarity = (image_features @ text_features.T).squeeze(0)
        # Get the most similar description
        best_description_index = similarity.argmax().item()
        best_description = text_descriptions[best_description_index]
        best_descriptions.append(best_description)
    # Create the final description string
    final_description = f"{best_descriptions[0]} {best_descriptions[1]} {best_descriptions[2]} for {best_descriptions[3]}"
    return final_description

