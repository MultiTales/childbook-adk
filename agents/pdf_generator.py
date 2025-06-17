import textwrap
from fpdf import FPDF
from PIL import Image


def text_to_pdf(image_path, callback_context):
    text = callback_context['edited']
    pdf = FPDF()

    # 添加一页
    pdf.add_page()
    text_after = textwrap.fill(text, 80)

    
    pdf.add_font("fireflysung", "", "./fireflysung.ttf", uni=True)
    pdf.set_font("fireflysung", "", 14)
    # pdf.set_font("Arial", size = 15)
    width = pdf.get_string_width(text_after.split("\n")[0])
    # 计算图片的目标宽度（取标题宽度和指定百分比的最小值）

    page_width = pdf.w - 2 * pdf.l_margin
    target_width = min(width, page_width * 80 / 100)
    try:
        # 打开图片并获取尺寸
        img = Image.open(image_path)
        width_px, height_px = img.size

        # 计算图片在PDF中的高度（保持比例）
        # 1px = 0.264583mm，但FPDF直接使用px尺寸，所以无需转换
        width_mm = target_width
        height_mm = height_px * width_mm / width_px

        # 计算图片的居中位置
        x_pos = (page_width - width_mm) / 2 + pdf.l_margin
        y_pos = 30  

        # 添加图片到PDF
        pdf.image(image_path, x=x_pos, y=y_pos, w=width_mm, h=height_mm)
        pdf.set_y(y_pos + height_mm + 20)

    except Exception as e:
        print(f"错误: {e}")
    # 添加文字
    pdf.multi_cell(200, 10, txt=text_after)

    # 保存文件
    pdf.output('story.pdf')


def remove_non_latin(text):
    # 移除无法用Latin-1编码的字
    return text.encode("latin-1", "ignore").decode("latin-1")


class ImageCreatorAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="pdf_generator",
            description="Generate a PDF file including image and story",
            instruction="""
                You are PDF Creater. Your job is to get the lastest story that is creeated by other model,
                and find a recently saved image, then save them into a PDF file.
                """,
            tools=[text_to_pdf],
        )
