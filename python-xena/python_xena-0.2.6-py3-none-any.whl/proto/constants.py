MsgType_UnknownMsgType = ""
MsgType_RejectMsgType = "3"
MsgType_ExecutionReportMsgType = "8"
MsgType_OrderCancelRejectMsgType = "9"
MsgType_LogonMsgType = "A"
MsgType_TradeCaptureReportMsgType = "AE"
MsgType_OrderMassStatusRequest = "AF"
MsgType_AccountStatusReportRequest = "XAA"
MsgType_AccountStatusReport = "XAR"
MsgType_AccountStatusUpdateReport = "XAF"
MsgType_NewOrderSingleMsgType = "D"
MsgType_NewOrderListMsgType = "E"
MsgType_OrderCancelRequestMsgType = "F"
MsgType_OrderCancelReplaceRequestMsgType = "G"
MsgType_OrderStatusRequest = "H"
MsgType_ListStatus = "N"
MsgType_MarketDataRequest = "V"
MsgType_MarketDataSnapshotFullRefresh = "W"
MsgType_MarketDataIncrementalRefresh = "X"
MsgType_MarketDataRequestReject = "Y"
MsgType_OrderMassStatusResponse = "U8"
MsgType_PositionMaintenanceRequest = "AL"
MsgType_PositionMaintenanceReport = "AM"
MsgType_RequestForPositions = "AN"
MsgType_PositionReport = "AP"
MsgType_MassPositionReport = "MAP"
MsgType_MarginRequirementReport = "CJ"
MsgType_Heartbeat = "0"

BusinessRejectReason_ApplicationNotAvailable = "4"
BusinessRejectReason_ThrottleLimitExceeded = "8"

MarginAmtType_UnknownMarginTypeType = ""
MarginAmtType_CoreMargin = "7"
MarginAmtType_InitialMargin = "11"

MarginReqmtRptType_SummaryType = "0"

Side_UnknownSide = ""
Side_Buy = "1"
Side_Sell = "2"

OrdType_Market = "1"
OrdType_Limit = "2"
OrdType_Stop = "3"
OrdType_StopLimit = "4"
OrdType_MarketIfTouched = "J" # real FIX value is 'J'
OrdType_Pegged = "P" # real FIX value is 'P'

ExecInst_StayOnOfferSide = "0"
ExecInst_AllOrNone = "G"
ExecInst_IgnoreNotionalValueChecks = "x"
ExecInst_Suspend = "s"
ExecInst_LiquidationOrder = "Y"

TimeInForce_GoodTillCancel = "1"
TimeInForce_ImmediateOrCancel = "3"
TimeInForce_FillOrKill = "4"

PegPriceType_TrailingStopPeg = "8"

PegOffsetType_BasisPoints = "2"

ExecType_NewExec = "0"
ExecType_CanceledExec = "4"
ExecType_ReplacedExec = "5"
ExecType_PendingCancelExec = "6"
ExecType_RejectedExec = "8"
ExecType_SuspendedExec = "9"
ExecType_PendingNewExec = "A"
ExecType_Restated = "D"
ExecType_PendingReplaceExec = "E"
ExecType_Trade = "F"
ExecType_OrderStatus = "I"

ExecRestatementReason_UnknownRestatementReason = ""
ExecRestatementReason_RepricingOfOrder = "3"

OrdStatus_NewOrd = "0"
OrdStatus_PartiallyFilled = "1"
OrdStatus_Filled = "2"
OrdStatus_CanceledOrd = "4"
OrdStatus_PendingCancelOrd = "6"
OrdStatus_Stopped = "7"
OrdStatus_RejectedOrd = "8"
OrdStatus_Suspended = "9"
OrdStatus_PendingNewOrd = "A"
OrdStatus_Expired = "C"
OrdStatus_PendingReplaceOrd = "E"

OrdRejReason_UnknownSymbol = "1"
OrdRejReason_ExchangeClosed = "2"
OrdRejReason_OrderExceedsLimit = "3"
OrdRejReason_DuplicateOrder = "6"
OrdRejReason_UnsupportedOrderCharacteristic = "11"
OrdRejReason_IncorrectQuantity = "13"
OrdRejReason_UnknownAccount = "15"
OrdRejReason_PriceExceedsCurrentPriceBand = "16"
OrdRejReason_Other = "99"
OrdRejReason_StopPriceInvalid = "100"

LiquidityInd_AddedLiquidity = "1"
LiquidityInd_RemovedLiquidity = "2"

SettlType_Regular = "0"
SettlType_Cash = "1"

CxlRejResponseTo_OrderCancelRequestCxlRejResponseTo = "1"
CxlRejResponseTo_OrderCancelReplaceRequestResponseTo = "2"

CxlRejReason_TooLateToCancel = "0"
CxlRejReason_UnknownOrder = "1"
CxlRejReason_OrderAlreadyInPendingStatus = "3"
CxlRejReason_DuplicateClOrdId = "6"
CxlRejReason_OtherCxlRejReason = "99"

BidType_NonDisclosed = "1"
BidType_Disclosed = "2"
BidType_NoBiddingProcess = "3"

ContingencyType_OneCancelsTheOther = "1"
ContingencyType_OneTriggersTheOther = "2"
ContingencyType_OneUpdatesTheOtherAbsolute = "3"
ContingencyType_OneUpdatesTheOtherProportional = "4"

ListStatusType_AckListStatusType = "1"
ListStatusType_ResponseListStatusType = "2"
ListStatusType_TimedListStatusType = "3"
ListStatusType_ExecStartedListStatusType = "4"
ListStatusType_AllDoneListStatusType = "5"
ListStatusType_AlertListStatusType = "6"

ListOrderStatus_InBiddingProcessListOrderStatus = "1"
ListOrderStatus_ReceivedForExecutionListOrderStatus = "2"
ListOrderStatus_ExecutingListOrderStatus = "3"
ListOrderStatus_CancellingListOrderStatus = "4"
ListOrderStatus_AlertListOrderStatus = "5"
ListOrderStatus_AllDoneListOrderStatus = "6"
ListOrderStatus_RejectListOrderStatus = "7"

ListRejectReason_UnsupportedOrderCharacteristicListRejectReason = "11"
ListRejectReason_ExchangeClosedListRejectReason = "2"
ListRejectReason_TooLateToEnterListRejectReason = "4"
ListRejectReason_UnknownOrderListRejectReason = "5"
ListRejectReason_DuplicateOrderListRejectReason = "6"
ListRejectReason_OtherListRejectReason = "99"

TriggerAction_Activate = "1"
TriggerAction_SetNewCapPrice = "4"
TriggerAction_Transform = "3101"

TriggerType_PartialExecution = "1"

TriggerScope_OtherOrder = "1"

PositionEffect_Close = "C"
PositionEffect_Open = "O"

PartieRole_ClientId = "3"
PartieRole_ContraFirm = "17"

MDEntryType_Bid                = "0"
MDEntryType_Offer              = "1"
MDEntryType_Trade              = "2"
MDEntryType_MarketBid          = "b"
MDEntryType_MarketOffer        = "c"
	
MDUpdateAction_NewAction             = "0"
MDUpdateAction_ChangeAction          = "1"
MDUpdateAction_DeleteAction          = "2"
	
MDBookType_TopOfBook         = "1"
MDBookType_PriceDepth        = "2"
MDBookType_OrderDepth        = "3"

SubscriptionRequestType_SnapshotAndUpdates = "1";
SubscriptionRequestType_DisablePreviousSnapshot = "2";

ThrottleType_InboundRate         = "0"
ThrottleType_OutstandingRequests = "1"

ThrottleTimeUnit_Seconds             = "0"
ThrottleTimeUnit_TenthsOfASecond     = "1"
ThrottleTimeUnit_HundredthsOfASecond = "2"
ThrottleTimeUnit_Milliseconds        = "3"
ThrottleTimeUnit_Microseconds        = "4"
ThrottleTimeUnit_Nanoseconds         = "5"
ThrottleTimeUnit_Minutes             = "10"
ThrottleTimeUnit_Hours               = "11"

BalanceChangeReason_DepositReason               = "1"
BalanceChangeReason_WithdrawReason              = "2"
BalanceChangeReason_DealReason                  = "3"
BalanceChangeReason_HoldReason                  = "4"
BalanceChangeReason_ReleaseReason               = "5"
BalanceChangeReason_RebateReason                = "6"
BalanceChangeReason_CommissionReason            = "7"
BalanceChangeReason_PositionCloseReason         = "8"
BalanceChangeReason_ClearingReason              = "9"
BalanceChangeReason_InterestPaymentReason       = "10"
BalanceChangeReason_PremiumPaymentReason        = "11"
BalanceChangeReason_RiskAdjustmentPaymentReason = "12"
BalanceChangeReason_SpotRewardReason            = "13"
BalanceChangeReason_MarginRewardReason          = "14"

PaymentType_Commission         = "40"
PaymentType_Interest           = "41"
PaymentType_Settlement         = "42"
PaymentType_CumulativePayments = "43"

RelatedTradeType_OpenExecId       = "1"
RelatedTradeType_CloseExecId      = "2"
RelatedTradeType_ParentPositionId = "3"

PosMaintAction_Replace = "2"
PosTransType_Collapse  = "20"
