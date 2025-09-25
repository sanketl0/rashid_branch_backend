import os
from pathlib import Path
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from io import BytesIO
def save_attach_file(file_data, output_path):

            with open(output_path, 'wb+') as destination:
                for chunk in file_data.chunks():
                    destination.write(chunk)
            pth = os.path.join(Path(__file__).parent, output_path)
            print('file is here', pth)
            return pth
            
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    current_time = datetime.datetime.now().timestamp()
    pdf_path = 'media/mypdf_{}.pdf'.format(current_time)
    with open(pdf_path, 'wb+') as output:
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
    return pdf_path

