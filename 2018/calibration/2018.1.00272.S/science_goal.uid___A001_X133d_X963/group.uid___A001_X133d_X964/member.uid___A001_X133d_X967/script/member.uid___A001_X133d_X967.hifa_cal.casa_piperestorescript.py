__rethrow_casa_exceptions = True
h_init()
try:
    hifa_restoredata (vis=['uid___A002_Xd79d9a_X41af', 'uid___A002_Xd7842e_X2447', 'uid___A002_Xd7842e_X1fca'], session=['session_2', 'session_1', 'session_1'], ocorr_mode='ca')
finally:
    h_save()
