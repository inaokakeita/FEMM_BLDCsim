import femm
import matplotlib.pyplot as plt
import numpy as np

femm.openfemm()
femm.opendocument("24pole_36slot.fem");#ひな形になるファイル
femm.mi_saveas("temp.fem")
femm.mi_seteditmode("group")
z=[];
f=[];
#ステータをちょっとずつ回転しながらsim
for n in range(0,60):
	print("step"+str(n))
	femm.mi_analyze()
	femm.mi_loadsolution()
	femm.mo_resize(2000,2000)
	femm.mo_zoomnatural()
	femm.mo_showdensityplot(1,0,2,0,"bmag")
	femm.mo_savebitmap("img/img"+str(n)+".bmp")
	femm.mo_groupselectblock(2)#ステータを選択(ひな形のステータをgroup2にしておく)
	fz=femm.mo_blockintegral(22)#0,0中心のトルクを計算
	z.append(n*0.5)
	f.append(fz)
	femm.mi_selectcircle(0,0,47,4)#円選択
	femm.mi_moverotate(0,0, 0.5)#回転
femm.closefemm()
np.savetxt("kt.csv",np.array(f))
plt.plot(z,f)
plt.ylabel('Torque, [Nm]')
plt.xlabel('Angle, [deg]')
plt.show()

