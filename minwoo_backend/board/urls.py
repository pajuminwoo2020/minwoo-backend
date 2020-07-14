from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    # BoardSettlement
    path('board/settlement', views.CreateBoardSettlementView.as_view(), name='board_settlement_create'),
    path('board/settlement/<int:board_id>', views.BoardSettlementView.as_view(), name='board_settlement'),
    path('board/settlements', views.BoardSettlementsView.as_view(), name='board_settlements'),

    # BoardNotice
    path('board/notice', views.CreateBoardNoticeView.as_view(), name='board_notice_create'),
    path('board/notice/<int:board_id>', views.BoardNoticeView.as_view(), name='board_notice'),
    path('board/notices', views.BoardNoticesView.as_view(), name='board_notices'),

    # Image
    path('board/image', views.UploadImageView.as_view(), name='image_upload'),
    path('board/image/<int:image_id>', views.ImageView.as_view(), name='image'),
    path('board/file', views.UploadFileView.as_view(), name='file_upload'),
    path('board/file/<int:file_id>', views.FileView.as_view(), name='file'),
]
