testversion = ''

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'

vis_7m = '/home/brunettn/antennae/2018.1.00272.S/'\
         'science_goal.uid___A001_X133d_X963/'\
         'group.uid___A001_X133d_X964/member.uid___A001_X133d_X969/'\
         'calibrated_nrao/calibrated_final.ms'

par_stage={}

par_stage['vis'] = vis_7m
par_stage['outputvis'] = calDir + 'ngc4038_band3_cont_7m'+ testversion + '.ms'
par_stage['spw'] = '16, 18, 20, 22, 40, 42, 44, 46, 64, 66, 68, 70,'\
                   '88, 90, 92, 94, 112, 114, 116, 118,'\
                   '136, 138, 140, 142, 160, 162, 164, 166,'\
                   '184, 186, 188, 190, 208, 210, 212, 214,'\
                   '232, 234, 236, 238'
par_stage['field'] = 'NGC4038'
par_stage['lines_to_flag'] = ['co10', 'cn10high', 'cn10low', 'hc3n1110']
# par_stage['lines_to_flag'] = [] # no lines to flage. 
par_stage['vsys'] = 1550.0
par_stage['vwidth'] = 685
par_stage['do_statwt'] = False
par_stage['do_collapse'] = True
par_stage['collapse_width'] = [128, 64, 32, 32]*10

