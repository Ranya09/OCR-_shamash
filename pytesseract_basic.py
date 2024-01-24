import pytesseract as pyt
import cv2
from tkinter import Tk, filedialog

# Configurer Tesseract
pyt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def upload_image():
    Tk().withdraw()  # hide the main window
    file_path = filedialog.askopenfilename(title="Select an image file",
                                           filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.pdf")])
    return file_path

def calculate_block_size(text, num_lines):
    total_chars = len(text.replace('\n', ''))
    return max(total_chars // num_lines, 1)

def split_into_blocks(text, block_size):
    blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
    # Fusionner les blocs si la dernière ligne est coupée au milieu d'un mot
    i = 0
    while i < len(blocks):
        if not blocks[i].endswith(' '):
            # Fusionner avec le bloc suivant jusqu'à ce que la dernière ligne se termine par un espace
            while i + 1 < len(blocks) and not blocks[i + 1].startswith(' '):
                blocks[i] += blocks[i + 1]
                blocks.pop(i + 1)
        i += 1
    return blocks

# Charger l'image de la facture en utilisant la fonction d'upload
img_path = upload_image()
img = cv2.imread(img_path)

# Convertir l'image en texte
full_text = pyt.image_to_string(img)

# Obtenir le nombre approximatif de lignes dans l'image
num_lines = full_text.count('\n') + 1

# Calculer dynamiquement la taille du bloc en fonction de la longueur moyenne des lignes
block_size = calculate_block_size(full_text, num_lines)

# Diviser le texte en blocs
blocks = split_into_blocks(full_text, block_size)

# Afficher et écrire les blocs dans un fichier
with open("facture_texte.txt", "a") as f:
    for i, block in enumerate(blocks):
        block = block.strip()
        if block:  # Éviter d'ajouter des blocs vides
            print(f"Block {i + 1}:", block)
            f.write(f"Block {i + 1}:\n{block}\n")
