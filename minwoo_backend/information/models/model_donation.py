import logging
import os
import io

from django.db import models
from django.core.files import File
from django.conf import settings
from django.utils.datetime_safe import datetime
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas

logger = logging.getLogger('logger')


class Donation(models.Model):
    donation_type = models.CharField(max_length=255, blank=False, verbose_name='기부종류')
    price = models.IntegerField(verbose_name='기부금')
    period = models.IntegerField(verbose_name='기부 주기')
    user_name = models.CharField(max_length=255, blank=False, verbose_name='회원명')
    birthday = models.DateField(verbose_name='생년월일')
    phone = models.CharField(max_length=255, blank=False, verbose_name='휴대폰번호')
    email = models.CharField(max_length=255, blank=False, verbose_name='이메일')
    bank_account = models.CharField(max_length=255, blank=False, verbose_name='은행계좌')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='주소')
    memo = models.CharField(max_length=255, blank=True, null=True, verbose_name='기타 메모')
    is_checked = models.BooleanField(default=False, verbose_name='연락 여부', help_text='후원신청 확인후 회원에게 연락했으면 체크해주세요. 후원 신청에 대해 빠짐없이 연락하기 위한 용도입니다.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='신청일')

    class Meta:
        verbose_name_plural = '후원금 신청내역 관리'
        verbose_name = '후원금 신청내역 관리'

    def draw_result(self, donation_info_stream, page_num):
        if page_num == 0:
            donation_info_canvas = canvas.Canvas(donation_info_stream)
            donation_info_canvas.setFontSize(10)
            donation_info_canvas.drawString(189, 774, str(datetime.now().year))
            donation_info_canvas.save()

    def generate_document(self):
        with open(os.path.join(settings.STATIC_DIR, 'assets', 'application_template.pdf'), 'rb') as f:
            application_template_reader = PdfFileReader(f)
            application_writer = PdfFileWriter()
            for page_num in range(application_template_reader.getNumPages()):
                page = application_template_reader.getPage(page_num)
                donation_info_stream = io.BytesIO()
                self.draw_result(donation_info_stream, page_num)
                if donation_info_stream.getvalue():
                    donation_info_page_reader = PdfFileReader(donation_info_stream)
                    donation_info_page = donation_info_page_reader.getPage(0)
                    page.mergePage(donation_info_page)
                application_writer.addPage(page)

            application_file_stream = io.BytesIO()
            application_writer.write(application_file_stream)
            application_file_name = f'민우회 후원신청서_{self.user_name}.pdf'

        return File(file=application_file_stream, name=application_file_name)
