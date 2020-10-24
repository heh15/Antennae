vis_12m_comp = '/home/brunettn/antennae/2018.1.00272.S/'\
               'science_goal.uid___A001_X133d_X963/'\
               'group.uid___A001_X133d_X964/'\
               'member.uid___A001_X133d_X967/calibrated_nrao/'\
               'calibrated_final.ms'
 

mstransform(vis= vis_12m_comp, outputvis = '../calibrated/test_mstransfrom.ms', datacolumn = 'DATA',  combinespws = True, nspw = 4, spw = '25, 27, 29, 31, 103, 105, 107, 109, 135, 137, 139, 141', field = 'NGC4038')
