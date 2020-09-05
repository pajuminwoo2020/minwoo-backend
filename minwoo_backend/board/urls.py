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

    # BoardAction
    path('board/action', views.CreateBoardActionView.as_view(), name='board_action_create'),
    path('board/action/<int:board_id>', views.BoardActionView.as_view(), name='board_action'),
    path('board/actions', views.BoardActionsView.as_view(), name='board_actions'),

    # BoardActivityMember
    path('board/activity_member', views.CreateBoardActivityMemberView.as_view(), name='board_activity_member_create'),
    path('board/activity_member/<int:board_id>', views.BoardActivityMemberView.as_view(), name='board_activity_member'),
    path('board/activity_members', views.BoardActivityMembersView.as_view(), name='board_activity_members'),

    # BoardPress
    path('board/press', views.CreateBoardPressView.as_view(), name='board_press_create'),
    path('board/press/<int:board_id>', views.BoardPressView.as_view(), name='board_press'),
    path('board/presses', views.BoardPressesView.as_view(), name='board_presses'),

    # BoardMemberSpace
    path('board/member_space', views.CreateBoardMemberSpaceView.as_view(), name='board_member_space_create'),
    path('board/member_space/<int:board_id>', views.BoardMemberSpaceView.as_view(), name='board_member_space'),
    path('board/member_spaces', views.BoardMemberSpacesView.as_view(), name='board_member_spaces'),

    # BoardSocietyActivity
    path('board/society_activity', views.CreateBoardSocietyActivityView.as_view(), name='board_society_activity_create'),
    path('board/society_activity/<int:board_id>', views.BoardSocietyActivityView.as_view(), name='board_society_activity'),
    path('board/society_activities', views.BoardSocietyActivitysView.as_view(), name='board_society_activities'),

    # BoardNewsletter
    path('board/newsletter', views.CreateBoardNewsletterView.as_view(), name='board_newsletter_create'),
    path('board/newsletter/<int:board_id>', views.BoardNewsletterView.as_view(), name='board_newsletter'),
    path('board/newsletters', views.BoardNewslettersView.as_view(), name='board_newsletters'),

    # BoardGallery
    path('board/gallery', views.CreateBoardGalleryView.as_view(), name='board_gallery_create'),
    path('board/gallery/<int:board_id>', views.BoardGalleryView.as_view(), name='board_gallery'),
    path('board/gallerys', views.BoardGallerysView.as_view(), name='board_gallerys'),

    # BoardDrive
    path('board/drive', views.CreateBoardDriveView.as_view(), name='board_drive_create'),
    path('board/drive/<int:board_id>', views.BoardDriveView.as_view(), name='board_drive'),
    path('board/drives', views.BoardDrivesView.as_view(), name='board_drives'),

    # BoardAffiliateActivity
    path('board/affiliate_activity', views.CreateBoardAffiliateActivityView.as_view(), name='board_affiliate_activity_create'),
    path('board/affiliate_activity/<int:board_id>', views.BoardAffiliateActivityView.as_view(), name='board_affiliate_activity'),
    path('board/affiliate_activities', views.BoardAffiliateActivitiesView.as_view(), name='board_affiliate_activities'),

    # BoardIntranetShare
    path('board/intranetshare', views.CreateBoardIntranetShareView.as_view(), name='board_intranetshare_create'),
    path('board/intranetshare/<int:board_id>', views.BoardIntranetShareView.as_view(), name='board_intranetshare'),
    path('board/intranetshares', views.BoardIntranetSharesView.as_view(), name='board_intranetshares'),

    # BoardIntranetDrive
    path('board/intranetdrive', views.CreateBoardIntranetDriveView.as_view(), name='board_intranetdrive_create'),
    path('board/intranetdrive/<int:board_id>', views.BoardIntranetDriveView.as_view(), name='board_intranetdrive'),
    path('board/intranetdrives', views.BoardIntranetDrivesView.as_view(), name='board_intranetdrives'),

    # BoardIntranetGeneral
    path('board/intranetgeneral', views.CreateBoardIntranetGeneralView.as_view(), name='board_intranetgeneral_create'),
    path('board/intranetgeneral/<int:board_id>', views.BoardIntranetGeneralView.as_view(), name='board_intranetgeneral'),
    path('board/intranetgenerals', views.BoardIntranetGeneralsView.as_view(), name='board_intranetgenerals'),


    # Image
    path('board/image', views.UploadImageView.as_view(), name='image_upload'),
    path('board/file', views.UploadFileView.as_view(), name='file_upload'),
    path('board/file/<slug:uidb64>', views.FileView.as_view(), name='file'),

    # Category
    path('board/categories/select/<str:board_type>', views.SelectCategoriesView.as_view(), name='category_select'),
]
