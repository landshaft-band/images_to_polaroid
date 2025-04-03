from PIL import Image
import os
import math

# Настройки размера
A4_WIDTH_MM, A4_HEIGHT_MM = 210, 297  # размеры листа A4 в мм
DPI = 300  # качество печати (точек на дюйм)
MM_TO_PX = DPI / 25.4  # перевод мм в пиксели

A4_WIDTH_PX = int(A4_WIDTH_MM * MM_TO_PX)
A4_HEIGHT_PX = int(A4_HEIGHT_MM * MM_TO_PX)

IMG_SIZE_MM = 80  # размер фотографии (8см)
IMG_SIZE_PX = int(IMG_SIZE_MM * MM_TO_PX)

MARGIN_MM = 15  # отступы (2 см)
MARGIN_PX = int(MARGIN_MM * MM_TO_PX)

# Загружаем фотографии
input_folder = "photos"  # Папка с фото
output_folder = "output"  # Папка для листов
os.makedirs(output_folder, exist_ok=True)

image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png','.JPG', '.PNG'))]
image_files.sort()
num_images = len(image_files)

# Размещаем по 6 фото на листе
photos_per_page = 6
rows, cols = 3, 2  # 3 ряда по 2 фото

total_pages = math.ceil(num_images / photos_per_page)  # Общее количество страниц

for page_num in range(total_pages):
    page = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")

    for photo_num in range(photos_per_page):
        # Вычисляем номер фото, которое нужно добавить на текущую страницу
        index = page_num * photos_per_page + photo_num

        if index >= num_images:
            break

        img_path = os.path.join(input_folder, image_files[index])
        img = Image.open(img_path).convert("RGB")
        img = img.resize((IMG_SIZE_PX, IMG_SIZE_PX), Image.LANCZOS)

        row, col = divmod(photo_num, cols)
        x_offset = MARGIN_PX + col * (IMG_SIZE_PX + MARGIN_PX)
        y_offset = MARGIN_PX + row * (IMG_SIZE_PX + MARGIN_PX)

        page.paste(img, (x_offset, y_offset))

    page.save(os.path.join(output_folder, f"page_{page_num + 1}.jpg"), quality=95)

print(f"Создано {total_pages} листов в папке '{output_folder}'")
