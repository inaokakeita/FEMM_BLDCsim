#FEMMライブラリのopenfemm()を1行変更
# HandleToFEMM = win32com.client.DispatchEx( "femm.ActiveFEMM") とする
# 
import femm
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures
from pythoncom import (CoInitializeEx, CoUninitialize,
					COINIT_MULTITHREADED, PumpWaitingMessages)

step_width = 1 #1stepでの回転角度deg
repeat = 30 #simのステップ数

#FEMMで1step分simする関数
def femm_analyze(step):
	import femm
	CoInitializeEx(COINIT_MULTITHREADED)
	femm.openfemm(1)
	femm.opendocument("tmp/temp"+str(step)+".fem");
	print("step"+str(step))
	femm.mi_seteditmode("group")
	femm.mi_analyze()
	print("step"+str(step)+"_end")
	femm.closefemm()
	CoUninitialize()
	
if __name__ == "__main__":
	#ステータをちょっとずつ回転させたfemファイルをステップ数分生成する
	femm.openfemm(1)
	for n in range(0,repeat):
		femm.opendocument("24pole_36slot.fem");#ひな形になるファイル
		femm.mi_selectcircle(0,0,47,4)#円選択
		femm.mi_moverotate(0,0, n*step_width)#回転
		femm.mi_seteditmode("Blocks")#なぜかブロックが回転しないので同じことをもう1回
		femm.mi_selectcircle(0,0,47)
		femm.mi_moverotate(0,0, n*step_width)
		femm.mi_saveas("tmp/temp"+str(n)+".fem")
	femm.closefemm()

	#マルチスレッドでsim実行
	args = range(0,repeat,1)
	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(femm_analyze, args)

	f = []
	#sim結果から画像とトルクをとりだす
	for step in range(0,repeat,1):
		print("output_step"+str(step))
		femm.openfemm(1)
		femm.opendocument("tmp/temp"+str(step)+".fem");
		femm.mi_loadsolution()
		#サイズ等をいい感じにする
		femm.mo_resize(2000,2000)
		femm.mo_zoomnatural()
		femm.mo_showdensityplot(1,0,2,0,"bmag") #densityplotの範囲を2Tまでにする
		femm.mo_savebitmap("img/tst"+str(step)+".bmp")
		femm.mo_groupselectblock(2)#ステータを選択(ひな形のステータをgroup2にしておく)
		f.append(femm.mo_blockintegral(22))#0,0中心のトルクを計算

	np.savetxt("tst.csv",f)
	plt.plot(list(f))
	plt.ylabel('Torque, [Nm]')
	plt.xlabel('Angle, [deg]')
	plt.show()

