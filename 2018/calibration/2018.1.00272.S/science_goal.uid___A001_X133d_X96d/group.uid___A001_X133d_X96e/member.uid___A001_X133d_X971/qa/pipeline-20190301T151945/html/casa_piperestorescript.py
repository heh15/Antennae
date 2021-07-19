__rethrow_casa_exceptions = True
h_init()
try:
    hifa_restoredata (vis=['uid___A002_Xd7dd07_Xe7a5'], session=['session_1'], ocorr_mode='ca')
finally:
    h_save()
