MagnetLines = {
    'Matrix' : ['Q3F3','c3F3','Q3D3','c3D3','Q3D2','c3D2','Q3F2','c3F2',
'RM5','SY1_3F4','SX1_3F4']
}


#dict [0,1,2,3]: name: type, power sources, polarity, direction
MagnetType = {
  'RM1' : ['ringmag',['12.drm','12.rst2.cRM1']],
  'RM2' : ['ringmag',['12.drm','12.rst2.cRM2']],
  'RM3' : ['ringmag',['12.drm','12.rst2.cRM3']],
  'RM4' : ['ringmag',['12.drm','12.rst2.cRM4']],
  'RM5' : ['ringmag',['12.drm','12.rst2.cRM5']],
  'RM6' : ['ringmag',['12.drm','12.rst2.cRM6']],
  'RM7' : ['ringmag',['12.drm','12.rst2.cRM7']],
  'RM8' : ['ringmag',['12.drm','12.rst2.cRM8']],
  'Q3D1' : ['quad60q',['12.qd1','12.rst3.c3D1_Q'],'minus'],
  'Q3F1' : ['quad60q',['12.qf1n2','12.rst3.c3F1_Q'],'plus'],
  'Q3F4' : ['quad60q',['12.qf4','12.rst3.c3F4_Q'],'plus'],
  'Q3F2' : ['quad60q',['12.qf1n2','12.rst3.c3F2_Q'],'plus'],
  'Q3D2' : ['quad80q',['12.qd2','12.rst3.c3D2_Q'],'minus'],
  'Q3D3' : ['quad80q',['12.qd3','12.rst3.c3D3_Q'],'minus'],
  'Q3F3' : ['quad80q',['12.qf3','12.rst3.c3F3_Q'],'plus'],
  'SY2_3F4' : ['sext',['12.rst3.Sy2_3F4']],
  'SX2_3F4' : ['sext',['12.rst3.Sx2_3F4']],
  'SX1_3F4' : ['sext',['12.rst3.Sx1_3F4']],
  'SY1_3F4' : ['sext',['12.rst3.Sy1_3F4']],
  'c3D1' : ['dcorr60',['12.rst2.c3D1_z'],'plus','V'],
  'c3F1' : ['dcorr60',['12.rst2.c3F1_x'],'plus','H'],
  'c3F4z' : ['dcorr60',['12.rst4.c3F4_z'],'plus','V'],
  'c3F2' : ['dcorr60',['12.rst2.c3F2_x'],'plus','H'],
  'c3D2' : ['dcorr80',['12.rst2.c3D2_z'],'plus','V'],
  'c3D3' : ['dcorr80',['12.rst3.c3D3_z'],'plus','V'],
  'c3F3' : ['dcorr80',['12.rst3.c3F3_x'],'plus','H']
}

AmperTurns = {
  'quad60q' : 1.5,
  'quad80q' : 1.36,
  'quad60c' : 5.0,
  'quad80c' : 5.45,
  'ringmag' : 6.67,
  'bm20inj'  : 1.1477,
  'bm45inj'  : 1.208,
  'bm20ext'  : 1.065,
  'bm45ext'  : 1.02
}

Rbends = {
  'ringmag' : 1.12,
  'bm20inj'  : 1.118,
  'bm45inj'  : 1.118,
  'bm20ext'  : 1.118,
  'bm45ext'  : 1.118,
  'sept'     : 2.334,
  'corr'     : 6.3
}