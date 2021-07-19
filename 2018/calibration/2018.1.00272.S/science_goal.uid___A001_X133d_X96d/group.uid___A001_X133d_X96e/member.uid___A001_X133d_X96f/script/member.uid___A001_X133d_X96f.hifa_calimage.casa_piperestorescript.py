__rethrow_casa_exceptions = True
h_init()
try:
    hifa_restoredata (vis=['uid___A002_Xdaef5a_X799b', 'uid___A002_Xd50463_X61f5'], session=['session_2', 'session_1'], ocorr_mode='ca')
finally:
    h_save()
