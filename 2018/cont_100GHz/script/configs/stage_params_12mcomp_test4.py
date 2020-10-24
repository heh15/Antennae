testversion = 'automatic_nobin_Bary'

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'

vis_12m_comp = '/home/brunettn/antennae/2018.1.00272.S/'\
               'science_goal.uid___A001_X133d_X963/'\
               'group.uid___A001_X133d_X964/'\
               'member.uid___A001_X133d_X967/calibrated_nrao/'\
               'calibrated_final.ms'

par_stage={}
par_stage['vis'] = vis_12m_comp
par_stage['outputvis'] = calDir + 'ngc4038_band3_cont_12mcomp'+'_'+testversion + '.ms' 
par_stage['spw'] = '25, 27, 29, 31, 103, 105, 107, 109, 135, 137, 139, 141'
par_stage['field'] = 'NGC4038'
par_stage['lines_to_flag'] = ['co10', 'cn10high', 'cn10low', 'hc3n1110']
# par_stage['lines_to_flag'] = [] # no lines to flage. 
par_stage['vsys'] = 1550.0
par_stage['vwidth'] = 685
par_stage['do_statwt'] = False
par_stage['do_collapse'] = False
par_stage['collapse_width'] = [128, 64, 32, 32]*3
