# coding: utf8
import PIL
from PIL import Image
from numpy import *
from PIL import ImageOps
import numpy
numpy.seterr(invalid='ignore')
import os.path
import ttk 
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import * 
from sys import *
import NW
from NW import *


def effectif(m):
	cpt=0
	x=[]
	y=[]
	for i in range(0,m.shape[0]):
		for j in range(0,m.shape[1]):
			#print(m[i,j]==True)
			if m[i,j]==0 :
				cpt=cpt+1;
				x.append(i)
				y.append(j)

	return (x,y,cpt)

	
def listdirectory(path):  
		fichier=[]  
		for root, dirs, files in os.walk(path):  
				for i in files:  
						fichier.append(os.path.join(root, i))  
		return fichier

def traitement(img):
	img=PIL.Image.open(img)
	im2= img.convert('L')

	#im2 = img.convert('1')
	#im2.show()
	im=numpy.asarray(im2)
	matrix=numpy.asmatrix(im)
	#entry.insert(INSERT,matrix.shape)
	#entry.insert(END,type(matrix))
	#print(matrix)
	cellule=[]
	mylist=[]
	for i in range(0,4):
		for j in range(0,4):
			
			cellule.append(matrix[(30*i):(30*(i+1)),(20*j):(20*(j+1))])

	'''for i in range(0,16):
		entry.insert(END,cellule[i].shape)
		entry.insert(END,"\n\n")
		entry.insert(END,cellule[i])
		entry.insert(END,"\n\n")'''

	#print(cellule[0].shape[0])
	for m in cellule:
		x,y,n=effectif(m)
		list_element=[]
		if n==0:
			list_element.append(0)
			list_element.append(0)
			list_element.append(0)
			mylist.append(list_element)
			#entry.insert(END,"effectife =  0 ")
			#entry.insert(END,"cannot be calculated \n")
		else:
			#entry.insert(END,"effectife =  {}".format(float(n)/float(100)))
			cov=numpy.cov(x,y)
			cov.resize(1,4)
			cov=cov[0,1]
			var=numpy.var(x)
			#@print(cov.shape)
			#entry.insert(END,"cov = {}".format(cov))
			#entry.insert(END,"var = {}".format(var))
			if var==0:
				a=0
				#entry.insert(END,"    â = {}\n".format(0))
			else:
				a=cov/var
				#entry.insert(END,"    â = {}\n".format(cov/var))
			#entry.insert(END,"    ni/Ni = {}\n".format((float(len(x))/float(1600))))
			list_element.append((float(len(x))/float(1600)))
			list_element.append((2*a)/(1+a**2))
			list_element.append((1-a**2)/(1+a**2))
			mylist.append(list_element)
	entry.insert(END,"\nEND Traitement\n\n\n")
	#entry.insert(END,mylist)
	return mylist


def save(mylist):
	myfile = open("/Volumes/Othmane Ansari/Otmane/Studies/Systeme_base_de_connaissance/Handwriting recognation/Projet/test.txt", 'a')

	for row in mylist:
		for e in row:
			myfile.write(str(e))
			myfile.write("\t")
	myfile.write('0')
	myfile.write("\t")
	myfile.write('0')
	myfile.write("\t")
	myfile.write('0')
	myfile.write("\t")
	myfile.write("\n")
	myfile.close()
	
	#f = open ( '/Volumes/Othmane Ansari/Otmane/Studies/Systeme_base_de_connaissance/Handwriting recognation/Draft/file.txt' , 'r')
	#l = [ map(str,line.split('\t')) for line in f ]
	#print (l)
def load():
	data=loadtxt('/Volumes/Othmane Ansari/Otmane/Studies/Systeme_base_de_connaissance/Handwriting recognation/Projet/dataset.txt')
	#print(data[:,:48])
	#print(data[:,48:])
	#entry.insert(END,data[:,:48])
	#entry.insert(END,data[:,48:])
	return (data[:,:48],data[:,48:])
def loadTest():
	data=loadtxt('/Volumes/Othmane Ansari/Otmane/Studies/Systeme_base_de_connaissance/Handwriting recognation/Projet/test.txt')
	#print(data[:,:48])
	#print(data[:,48:])
	#entry.insert(END,data[:,:48])
	#entry.insert(END,data[:,48:])
	return (data[:,:48],data[:,48:])
class TkFileDialogExample(Tkinter.Frame):

	def __init__(self, root,neuralnetwork):

		Tkinter.Frame.__init__(self, root)

		self.neuralnetwork=neuralnetwork
		# options for buttons
		button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

		# define buttons

		Tkinter.Button(self, text='askopenfilename', command=self.askopenfilename).pack(**button_opt)
		#Tkinter.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)
		Tkinter.Button(self, text='Learn', command=self.learn).pack(**button_opt)
		# define options for opening or saving a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = 'myfile.txt'
		options['parent'] = root
		options['title'] = 'This is a title'

		# This is only available on the Macintosh, and only when Navigation Services are installed.
		#options['message'] = 'message'

		# if you use the multiple file version of the module functions this option is set automatically.
		#options['multiple'] = 1

		# defining options for opening a directory
		self.dir_opt = options = {}
		options['initialdir'] = 'C:\\'
		options['mustexist'] = False
		options['parent'] = root
		options['title'] = 'This is a title'

	def learn(self):
		entry.insert(END,"LEARNIN  ...\n")
		x,y=load()
		
		patterns=[]
		for i in range(0,x.shape[0]):
			p=[]
			p.append(x[i])
			p.append(y[i])
			patterns.append(p)
		self.neuralnetwork.train(patterns)
		entry.insert(END,"DONE LEARNIN  ...\n")
		import pickle
		pickle.dump(neuralnetwork,open("neuralnetwork.p","wb"))
	def askopenfilename(self):

		"""Returns an opened file in read mode.
		This time the dialog just returns a filename and the file is opened by your own code.
		"""

		# get filename
		filename = tkFileDialog.askopenfilename(filetypes = (("Image Files","*.jpg"),("Image Files","*.png")))
		mylist=traitement(filename)
		inputs=[]
		for row in mylist:
			for e in row:
				inputs.append(e)

		print(len(inputs))

		resultat=self.neuralnetwork.test(inputs)
		for i in range(len(resultat)):
			if resultat[i]>0.6:
				resultat[i]=1
			else:
				resultat[i]=0
		entry.insert(END,"prediction = {}".format(resultat))
		#save(mylist)
		# open file on your own
		'''if filename:
			return open(filename, 'r')'''



	def askdirectory(self):

		"""Returns a selected directoryname."""

		path=tkFileDialog.askdirectory(**self.dir_opt)
		fichier=[]  
		for root, dirs, files in os.walk(path):  
				for i in range(1,len(files)):  
						fichier.append(os.path.join(root,files[i]))
						mylist=traitement(os.path.join(root,files[i]))
						save(mylist)
		load()
		#entry.insert(END,fichier)
	

if __name__=='__main__':
	root = Tkinter.Tk()
	#neuralnetwork=MLP_NeuralNetwork(48,30,3,iterations = 120, learning_rate = 0.5, momentum = 0.5, rate_decay = 0.2)
	import pickle
	neuralnetwork=pickle.load(open("OLDneuralnetwork.p","rb"))
	root.geometry("800x600")
	TkFileDialogExample(root,neuralnetwork).pack()
	'''value = StringVar() 
	value.set("texte par défaut")'''
	frame= Frame(root, bg="white", width=300, padx=10, pady=10)
	canevas=Canvas(frame)
	canevas.configure(width=77,height=117,bg="white",borderwidth=0,highlightthickness=1,highlightbackground="black")
	canevas.pack( side=LEFT,fill=X,padx=5, pady=5)
	# commande clic
	def clic():
			canevas.delete("all")
	def saveImg():
			#img = Image.new('RGBA', canevas, (255, 255, 255, 255))

			canevas.postscript(file="save.eps", colormode="mono")
			im=PIL.Image.open('./save.eps')
			im=im.convert('L')
			im.save('./save.png')
			#cmd = 'convert  save.eps  -type Grayscale  save.png'
			#os.system(cmd)
			#cmd = 'convert save.png -resize 43x43 save.png'
			#os.system(cmd)
			cmd = 'rm -r  save.eps'
			os.system(cmd)
			canevas.delete("all")
			mylist=traitement("./save.png")
			inputs=[]
			for row in mylist:
				for e in row:
					inputs.append(e)

			#print(len(inputs))

			resultat=neuralnetwork.predict(inputs)
			proba=[]
			for i in range(len(resultat)):
				if resultat[i]>0.6:
					#print(resultat[i])
					proba.append(float((resultat[i]-0.6))/float(0.4))
					resultat[i]=1
				else:
					#print(resultat[i])
					proba.append(1-(resultat[i]/0.6))
					resultat[i]=0

			if resultat==[0,0,0]:
				predict="B"
			elif resultat==[0,0,1]:
				predict="F"
			elif resultat==[0,1,0]:
				predict="H"
			elif resultat==[0,1,1]:
				predict="K"
			elif resultat==[1,0,0]:
				predict="G"
			elif resultat==[1,0,1]:
				predict="J"
			else:
				predict="Not recognized"
			#print(float(proba[0]*proba[1]*proba[2]))
			prod=float(proba[0]*proba[1]*proba[2])
			entry.delete(0.0, END)
			entry.insert(END,"prediction = {} , avec une probabilité de {}%\n".format(predict,round(prod,2)*100))
	def Testing():
		entry.insert(END,"Testing  ...\n")

		x,y=loadTest()
		
		patterns=[]
		for i in range(0,x.shape[0]):
			p=[]
			p.append(x[i])
			p.append(y[i])
			patterns.append(p)
		neuralnetwork.test(patterns,entry)
		entry.insert(END,"DONE Testing  ...\n")
	Button(root, text='Testing', command=Testing).pack()
	# creation des boutons
	Button(frame, text ='Traiter',command= saveImg).pack(side=LEFT, padx=5, pady=5)
	Button(frame, text ='Effacer', command= clic).pack(side=LEFT, padx=5,pady=5)
	frame.pack(side=TOP,fill=Y)
	# initialisation des variables de position
	x="vide"
	y="vide"
	# initialisation de l’etat du bouton gauche de la souris
	etatboutonsouris="haut"

	# gestionnaire d’evenement associe au clic sur le canevas
	def clic(event):
			global etatboutonsouris,x,y
			etatboutonsouris="bas"
			x=event.x
			y=event.y
	canevas.bind("<ButtonPress-1>",clic)
	# gestionnaire d’evenement associe au declic sur le canevas
	def declic(event):
			global etatboutonsouris
			etatboutonsouris="haut"
	canevas.bind("<ButtonRelease-1>",declic)
	# gestionnaire d’evenement associe au mouvement sur le canevas
	def mouvement(event):
			global etatboutonsouris,x,y
			if (etatboutonsouris=="bas"):
					canevas.create_line(x,y,event.x,event.y,width=3)
			x=event.x
			y=event.y
	canevas.bind("<Motion>",mouvement)
	yscrollbar = Scrollbar(root)
	yscrollbar.pack(side=RIGHT, fill=Y)
	entry = Text(root,yscrollcommand=yscrollbar.set, width=300,highlightthickness=1,highlightbackground="black")
	entry.pack(side=BOTTOM)
	yscrollbar.config(command=entry.yview)
	root.mainloop()