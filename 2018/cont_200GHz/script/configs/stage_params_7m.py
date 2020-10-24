testversion = ''

Dir = '/home/heh15/research/Antennae/2018/cont_200GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'

vis_7m = '/home/heh15/antennae/2018.1.00272.S/'\
	'science_goal.uid___A001_X133d_X96d/'\
	'group.uid___A001_X133d_X96e/'\
	'member.uid___A001_X133d_X973/'\
	'calibrated_nrao/calibrated_final.ms'

par_stage={}

par_stage['vis'] = vis_7m
par_stage['outputvis'] = calDir + 'ngc4038_band6_cont_7m'+ testversion + '.ms'
par_stage['spw'] = '16, 18, 20, 22, 40, 42, 44, 46, 64, 66, 68, 70'
par_stage['field'] = 'NGC4038'
par_stage['lines_to_flag'] = ['co21', '13co21', 'c18o21']
# par_stage['lines_to_flag'] = [] # no lines to flage. 
par_stage['vsys'] = 1550.0
par_stage['vwidth'] = 685
par_stage['do_statwt'] = False
par_stage['do_collapse'] = True
par_stage['collapse_width'] = [64, 32, 32, 32]*3

