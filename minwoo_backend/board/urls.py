from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    ### BoardSettlement
    path('board/settlement', views.CreateBoardSettlementView.as_view(), name='board_settlement_create'),
    path('board/settlement/<int:board_id>', views.BoardSettlementView.as_view(), name='board_settlement'),
    path('board/settlements', views.BoardSettlementsView.as_view(), name='board_settlements'),
]
