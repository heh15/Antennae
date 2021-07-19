__rethrow_casa_exceptions = True
h_init()
try:
    hifa_restoredata (vis=['uid___A002_Xd395f6_X6bd0', 'uid___A002_Xd3607d_X68a2', 'uid___A002_Xd3607d_X65a8'], session=['session_2', 'session_1', 'session_1'], ocorr_mode='ca')
finally:
    h_save()
