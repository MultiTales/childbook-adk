import textwrap
from fpdf import FPDF
from PIL import Image
import io
def text_to_pdf(image_bytes, text):
    print("开始创建pdf")
    pdf = FPDF()

    # add a page
    pdf.add_page()
    text_after = textwrap.fill(text, 80)

    
    pdf.add_font("fireflysung", "", "./fireflysung.ttf", uni=True)
    pdf.set_font("fireflysung", "", 14)

    page_width = pdf.w - 2 * pdf.l_margin
    target_width = page_width * 80 / 100
    # try:
    # open image and get its size
    data = io.BytesIO(image_bytes)

    img = Image.open(data)
    width_px, height_px = img.size

    # cal the height of the image in pdf file
    
    width_mm = target_width
    height_mm = height_px * width_mm / width_px

    # cal the middle position
    x_pos = (page_width - width_mm) / 2 + pdf.l_margin
    y_pos = 30  
    # add image to PDF
    pdf.image(data, x=x_pos, y=y_pos, w=width_mm, h=height_mm)
    pdf.set_y(y_pos + height_mm + 20)

    # except Exception as e:
    #     print(f"错误: {e}")
    # add text
    pdf.multi_cell(200, 10, text=text_after)

    # save file
    pdf.output('story.pdf')

    return pdf.output(dest='S')


def remove_non_latin(text):
    # remove words which can not be encoded by Latin-1
    return text.encode("latin-1", "ignore").decode("latin-1")


# with open("./output-image-adk-1c4da299-cf7d-4feb-9117-02ff48ba5e25.png", "rb") as f:
#     image_bytes = f.read()
# # print(str(image_bytes))
# text_to_pdf(image_bytes=image_bytes, text="asdsdfajsflaksjfjkasjfasjfkaskjfajskfjkasjkfkjasfkjajksfkjaskjf")