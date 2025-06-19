import textwrap
from fpdf import FPDF
from PIL import Image
import io
def text_to_pdf(image_bytes, text):
    
    pdf = FPDF()

    # add a page
    pdf.add_page()
    text_after = textwrap.fill(text, 80)

    
    pdf.add_font("fireflysung", "", "./fireflysung.ttf", uni=True)
    pdf.set_font("fireflysung", "", 14)
    # pdf.set_font("Arial", size = 15)
    width = pdf.get_string_width(text_after.split("\n")[0])
    # cal the width

    page_width = pdf.w - 2 * pdf.l_margin
    target_width = min(width, page_width * 80 / 100)
    try:
        # open image and get its size
        img = Image.open(io.BytesIO(image_bytes))
        width_px, height_px = img.size

        # cal the height of the image in pdf file
       
        width_mm = target_width
        height_mm = height_px * width_mm / width_px

        # cal the middle position
        x_pos = (page_width - width_mm) / 2 + pdf.l_margin
        y_pos = 30  

        # add image to PDF
        pdf.image(img, x=x_pos, y=y_pos, w=width_mm, h=height_mm)
        pdf.set_y(y_pos + height_mm + 20)

    except Exception as e:
        print(f"错误: {e}")
    # add text
    pdf.multi_cell(200, 10, txt=text_after)

    # save file
    pdf.output('story.pdf')


def remove_non_latin(text):
    # remove words which can not be encoded by Latin-1
    return text.encode("latin-1", "ignore").decode("latin-1")
