import logging
import os
import io

from django.db import models
from django.core.files import File
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.datetime_safe import datetime
from django.urls import reverse
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

logger = logging.getLogger('logger')


class Donation(models.Model):
    DONATION_TYPE_REGULAR = '정기후원'
    DONATION_TYPE_TEMPORARY = '일시후원'
    DONATION_TYPES = (
        (DONATION_TYPE_REGULAR, DONATION_TYPE_REGULAR),
        (DONATION_TYPE_TEMPORARY, DONATION_TYPE_TEMPORARY),
    )
    MOTIVATION_SUGGESTION = '권유'
    MOTIVATION_SNS = 'SNS(트위터, 페이스북 등)'
    MOTIVATION_PRESS = '언론'
    MOTIVATION_CAMPAIGN = '캠패인/행사'
    MOTIVATION_ACTIVITY = '회원활동관심'
    MOTIVATION_PLAN = '기획단활동'
    MOTIVATION_EDUCATION = '교육'
    MOTIVATION_CONSULTING = '상담'
    MOTIVATION_ETC = '기타'
    MOTIVATION_TYPES = (
        (MOTIVATION_SUGGESTION, MOTIVATION_SUGGESTION),
        (MOTIVATION_SNS, MOTIVATION_SNS),
        (MOTIVATION_PRESS, MOTIVATION_PRESS),
        (MOTIVATION_CAMPAIGN, MOTIVATION_CAMPAIGN),
        (MOTIVATION_ACTIVITY, MOTIVATION_ACTIVITY),
        (MOTIVATION_PLAN, MOTIVATION_PLAN),
        (MOTIVATION_EDUCATION, MOTIVATION_EDUCATION),
        (MOTIVATION_CONSULTING, MOTIVATION_CONSULTING),
        (MOTIVATION_ETC, MOTIVATION_ETC),
    )

    donation_type = models.CharField(max_length=255, choices=DONATION_TYPES, verbose_name='기부종류')
    price = models.IntegerField(verbose_name='기부금')
    applicant_name = models.CharField(max_length=255, verbose_name='신청인')
    applicant_birthday = models.CharField(max_length=255, verbose_name='신청인 생년월일')
    applicant_phone = models.CharField(max_length=255, verbose_name='신청인 휴대폰번호')
    account_holder_name = models.CharField(max_length=255, verbose_name='예금주')
    account_holder_birthday = models.CharField(max_length=255, verbose_name='예금주 생년월일 혹은 사업자등록번호)')
    account_holder_phone = models.CharField(max_length=255, verbose_name='에금주 휴대폰번호')
    email = models.CharField(max_length=255, verbose_name='이메일')
    bank_name = models.CharField(max_length=255, verbose_name='은행명')
    account_number = models.CharField(max_length=255, verbose_name='계좌번호')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='주소')
    memo = models.CharField(max_length=255, blank=True, null=True, verbose_name='기타 메모')
    resident_registration_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='주민등록번호')
    image_signature = models.ImageField(max_length=2048)
    agree_receipt = models.BooleanField(default=False, verbose_name='기부금 영수증 동의')
    agree_unique = models.BooleanField(default=False, verbose_name='고유식별정보 동의')
    agree_personal = models.BooleanField(default=False, verbose_name='개인정보수집 동의')
    agree_offer = models.BooleanField(default=False, verbose_name='개인정보 3자제공 동의')
    agree_newsletter = models.BooleanField(default=False, verbose_name='소식지 수령 동의')
    agree_email = models.BooleanField(default=False, verbose_name='이메일 수신 동의')
    motivation = models.CharField(max_length=255, default=MOTIVATION_ETC, choices=MOTIVATION_TYPES, verbose_name='가입동기')
    is_checked = models.BooleanField(default=False, verbose_name='연락 여부', help_text='후원신청 확인후 회원에게 연락했으면 체크해주세요. 후원 신청에 대해 빠짐없이 연락하기 위한 용도입니다.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='신청일')

    class Meta:
        verbose_name_plural = '후원금 신청내역 관리'
        verbose_name = '후원금 신청내역 관리'

    def _draw_result(self, donation_info_stream, information):
        pdfmetrics.registerFont(TTFont('NanumGothic', os.path.join(settings.STATIC_DIR, 'assets', 'fonts', 'NanumGothic.ttf')))
        pdfmetrics.registerFont(TTFont('NanumGothicBold', os.path.join(settings.STATIC_DIR, 'assets', 'fonts', 'NanumGothicBold.ttf')))
        pdfmetrics.registerFont(TTFont('NanumGothicExtraBold', os.path.join(settings.STATIC_DIR, 'assets', 'fonts', 'NanumGothicExtraBold.ttf')))
        pdfmetrics.registerFont(TTFont('NanumGothicLight', os.path.join(settings.STATIC_DIR, 'assets', 'fonts', 'NanumGothicLight.ttf')))
        donation_info_canvas = canvas.Canvas(donation_info_stream)
        donation_info_canvas.setFont('NanumGothic', 7)
        if self.donation_type == self.DONATION_TYPE_REGULAR:
            donation_info_canvas.drawString(415, 743, '월(년)정액후원')
        else:
            donation_info_canvas.drawString(415, 743, '일시후원')
        """ 1. 후원기관정보 """
        donation_info_canvas.drawString(180, 730, information.chief_executive)
        donation_info_canvas.drawString(415, 730, information.registration_number)
        donation_info_canvas.drawString(180, 717, information.address_street)
        """ 2. 회원정보 """
        # 신청인 정보
        donation_info_canvas.drawString(182, 682, self.applicant_name)
        donation_info_canvas.drawString(452, 682, self.applicant_birthday)
        donation_info_canvas.drawString(250, 668, str(self.address) if self.address else '')
        donation_info_canvas.drawString(455, 641, self.applicant_phone)
        donation_info_canvas.drawString(250, 625, self.email)
        donation_info_canvas.setFont('NanumGothicBold', 9)
        if self.agree_newsletter:
            donation_info_canvas.drawString(428, 658, 'V')
        else:
            donation_info_canvas.drawString(458, 658, 'V')
        if self.agree_email:
            donation_info_canvas.drawString(347, 627, 'V')
        else:
            donation_info_canvas.drawString(374, 627, 'V')
        ## 가입동기
        if self.donation_type == self.DONATION_TYPE_REGULAR:
            if self.motivation == self.MOTIVATION_SUGGESTION:
                donation_info_canvas.drawString(185, 502, 'V')
            elif self.motivation == self.MOTIVATION_SNS:
                donation_info_canvas.drawString(271, 502, 'V')
            elif self.motivation == self.MOTIVATION_PRESS:
                donation_info_canvas.drawString(376, 502, 'V')
            elif self.motivation == self.MOTIVATION_CAMPAIGN:
                donation_info_canvas.drawString(405, 502, 'V')
            elif self.motivation == self.MOTIVATION_ACTIVITY:
                donation_info_canvas.drawString(462, 502, 'V')
            elif self.motivation == self.MOTIVATION_PLAN:
                donation_info_canvas.drawString(185, 490, 'V')
            elif self.motivation == self.MOTIVATION_CONSULTING:
                donation_info_canvas.drawString(241, 490, 'V')
            elif self.motivation == self.MOTIVATION_EDUCATION:
                donation_info_canvas.drawString(298, 490, 'V')
            else: # self.motivation == self.MOTIVATION_ETC
                donation_info_canvas.drawString(329, 490, 'V')

        # 예금주 정보
        donation_info_canvas.setFont('NanumGothic', 7)
        donation_info_canvas.drawString(182, 600, self.account_holder_name)
        donation_info_canvas.drawString(452, 600, self.account_holder_birthday)
        donation_info_canvas.drawString(182, 575, str(self.account_number))
        donation_info_canvas.drawString(452, 575, self.bank_name)
        donation_info_canvas.drawString(182, 556, self.account_holder_phone)
        # 기부금액
        donation_info_canvas.setFont('NanumGothicBold', 9)
        price = self.price
        if self.donation_type == self.DONATION_TYPE_TEMPORARY:
            donation_info_canvas.drawString(230, 528, 'V')
            donation_info_canvas.setFont('NanumGothic', 7)
            donation_info_canvas.drawString(265, 526, f'{price}원')
            donation_info_canvas.setFont('NanumGothicBold', 12)
        else:
            if price == 12000:
                donation_info_canvas.drawString(185, 540, 'V')
            elif price == 20000:
                donation_info_canvas.drawString(238, 540, 'V')
            elif price == 30000:
                donation_info_canvas.drawString(280, 540, 'V')
            elif price == 120000:
                donation_info_canvas.drawString(185, 528, 'V')
            elif price == 1000000: # 평생회원
                donation_info_canvas.drawString(185, 516, 'V')
            else:
                donation_info_canvas.drawString(230, 528, 'V')
                donation_info_canvas.setFont('NanumGothic', 7)
                donation_info_canvas.drawString(265, 526, f'{price}원')
            donation_info_canvas.setFont('NanumGothicBold', 12)
            donation_info_canvas.drawString(471, 535, 'V')
        """ 3. 기부금영수증 """
        if self.agree_receipt:
            donation_info_canvas.drawString(146, 441, 'V')
            donation_info_canvas.setFont('NanumGothic', 7)
            donation_info_canvas.drawString(146, 412, self.resident_registration_number)
        else:
            donation_info_canvas.drawString(193, 441, 'V')

        donation_info_canvas.setFont('NanumGothicBold', 12)
        # 고유식별정보수집
        if self.agree_unique:
            donation_info_canvas.drawString(237, 393, 'V')
        else:
            donation_info_canvas.drawString(290, 393, 'V')
        # 개인정보수집
        if self.agree_personal:
            donation_info_canvas.drawString(236, 335, 'V')
        else:
            donation_info_canvas.drawString(286, 335, 'V')
        # 개인정보 3자제공
        if self.agree_offer:
            donation_info_canvas.drawString(221, 270, 'V')
        else:
            donation_info_canvas.drawString(271, 270, 'V')
        """ 4. 서명 """
        donation_info_canvas.setFont('NanumGothicBold', 10)
        donation_info_canvas.drawString(309, 135, str(self.created_at.year))
        donation_info_canvas.drawString(355, 135, str(self.created_at.month))
        donation_info_canvas.drawString(373, 135, str(self.created_at.day))
        donation_info_canvas.drawString(440, 136, str(self.applicant_name))
        self._draw_signature(donation_info_canvas)
        if self.applicant_name != self.account_holder_name:
            donation_info_canvas.drawString(440, 122, str(self.account_holder_name))
        """ 5. 하단 회사정보 """
        donation_info_canvas.setFont('NanumGothic', 7)
        donation_info_canvas.drawString(203, 56, information.phone)
        donation_info_canvas.drawString(308, 56, information.fax)
        donation_info_canvas.drawString(413, 56, information.email)

        donation_info_canvas.save()

    def _draw_signature(self, signature_canvas):
        if self.image_signature:
            signature_canvas.drawImage(
                self.image_signature.path,
                500,
                125,
                height=30,
                width=30,
                mask='auto',
            )

    def generate_document(self):
        with open(os.path.join(settings.STATIC_DIR, 'assets', 'application_template.pdf'), 'rb') as f:
            from information.models import Information

            application_template_reader = PdfFileReader(f)
            application_writer = PdfFileWriter()
            information = Information.objects.all().first()

            page = application_template_reader.getPage(0)
            donation_info_stream = io.BytesIO()
            self._draw_result(donation_info_stream, information)
            if donation_info_stream.getvalue():
                donation_info_page_reader = PdfFileReader(donation_info_stream)
                donation_info_page = donation_info_page_reader.getPage(0)
                page.mergePage(donation_info_page)

            application_writer.addPage(page)

            application_file_stream = io.BytesIO()
            application_writer.write(application_file_stream)
            application_file_name = f'민우회 후원신청서_{self.applicant_name}.pdf'

        return File(file=application_file_stream, name=application_file_name)

    def get_absolute_url(self):
        return reverse('information:donation_download', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(self.id))})
