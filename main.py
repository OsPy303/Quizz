#coding: utf-8
#################################
# Quiz game for android			#
# Developer: VAOHITA Ivan Oscar #
# GUI: using kivy				#
#################################

# Module importation

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from random import randrange
from time import sleep, strftime
import data
import sys


def sort(ls):
	ls_sc_dict = {}
	ls_sc = []
	ls_sc_sorted = []
	for elt in ls:
		val1, val2 = elt.split(";")
		ls_sc_dict [int(val1)] = elt
		ls_sc.append(int(val1))
	ls_sc.sort()
	for val in ls_sc:
		ls_sc_sorted.append(ls_sc_dict[val])
	return ls_sc_sorted


class ScoreManager:
	def __init__(self):
		self.mScore = 0
		self.life = 3
		self.month = [
					None,
					'january',
					'february',
					'march',
					'april',
					'may',
					'june',
					'july',
					'august',
					'september',
					'october',
					'november',
					'december'
				]

	def set_score(self):
		if self.life == 3:
			self.mScore += 25
		elif self.life == 2:
			self.mScore += 15
		else:
			self.mScore += 10

	def set_life(self):
		self.life -= 1

	def get_score(self):
		sc = str(self.mScore)
		return sc

	def get_life(self):
		return self.life

	def reset_score(self):
		self.mScore = 0

	def reset_life(self):
		self.life = 3

	def is_high_score(self, score):
		""" Une fonction qui verifie si le score passé en parametre
			est un nouveau meilleur score """
		scores = []
		# On récupère tout les scores enregistré dans le fichier
		with open("score.txt", 'r') as all_score:
			while 1:
				line = all_score.readline()
				if line == "":
					break
				scores.append(line)

		# Si le fichier est vide on enregistre le score
		if  not scores:
			mois = strftime("%B")
			mois = self.month.index(mois.lower())
			time_ = strftime("%d/{}/%Y %H:%M".format(mois))
			score_to = f"{score};{time_}\n"
			with open("score.txt", 'w') as all_score:
				all_score.write(score_to)
			return "Nouveau meilleur score!"

		# Si le fichier n'est pas vide on compare le plus grand score avec le nouveau
		elif scores:
			scores = sort(scores)
			hight_score = scores[-1]
			hscore, date = hight_score.split(";")
			if int(hscore) < int(score):
				if len(scores) == 4:
					scores.remove(scores[0])
					mois = strftime("%B")
					mois = self.month.index(mois.lower())
					time_ = strftime("%d/{}/%Y %H:%M".format(mois))
					scores.append(f"{score};{time_}\n")
					with open("score.txt", "w") as all_score:
						for elt in scores:
							all_score.write(elt)
				else:
					mois = strftime("%B")
					mois = self.month.index(mois.lower())
					time_ = strftime("%d/{}/%Y %H:%M".format(mois))
					#scores.append(f"{score};{time_}\n")
					save = str(score) + ";" + time_ + "\n"
					with open("score.txt", "a") as all_score:
						all_score.write(save)

				return "Nouveau meilleur score!"

			# On enregistre pas si ce n'est pas le meilleur score
			else:
				return ""

class QuestionManager:
	def __init__(self, file):
		self.questionFfile = file
		self.lsAllQuestion = []
		self.question = ""
		self.answere = ""
		self.trueAnswere = ""

	def getAllQuestion(self):
		self.lsAllQuestion = []
		with open(self.questionFfile, 'r') as myFile:
			while True:
				line = myFile.readline()
				if line == "":
					break
				self.lsAllQuestion.append(line)

	def getQuestion(self):
		try:
			indexOfQuestion = randrange(len(self.lsAllQuestion)) # On choisi un undex au hasar
		except ValueError:
			self.getAllQuestion()
			indexOfQuestion = randrange(len(self.lsAllQuestion)) # On choisi un undex au hasar

		chosedQuestion = self.lsAllQuestion[indexOfQuestion] # On choisit la question correspondant à l'index choisit
		self.lsAllQuestion.remove(self.lsAllQuestion[indexOfQuestion]) # On supprime la question choisit das la liste
		chosedQuestion = chosedQuestion.split(";")
		self.question = chosedQuestion[0] # On retire la question
		tmpAnswere = chosedQuestion[1:] # on retire les reponse
		i = 0
		for ans in tmpAnswere: # A la recherche du vrais reponse
			if ans[0] == '*':
				self.trueAnswere = tmpAnswere[i][1:] # On enleve le marqueur
				tmpAnswere.remove(tmpAnswere[i]) # On supprime la vrai rep
				break
			i += 1
		tmpAnswere.insert(randrange(2), self.trueAnswere) # On le reinsere dans la liste
		self.answere = self.mix(tmpAnswere)

	def getRealQuestion(self):
		return self.question

	def getAnswereA(self):
		return self.answere[0]

	def getAnswereB(self):
		return self.answere[1]

	def getAnswereC(self):
		return self.answere[2]

	def mix(self, ls):
		ls_2 = [None]
		for i in range(3):
			chosed = randrange(len(ls))
			ls_2.insert(randrange(len(ls_2)), ls[chosed])
			ls.remove(ls[chosed])
		ls_2.remove(None)
		return ls_2

# Chargement des données et initialisation des class
score_m = ScoreManager()
myQuest = QuestionManager(data.QUESTION)
myQuest.getAllQuestion()


err_sound = SoundLoader.load(data.FALSE_ANSWERE)
true_sound = SoundLoader.load(data.TRUE_ANSWERE)
fond = SoundLoader.load(data.SOUND_BACKGROUND)
fond.loop = True

err_sound.volume = .2
err_sound.seek(0)
true_sound.seek(0)

Window.size = data.DEFAULT_SCREEN_SIZE
# Screen management


class HomeScreen(Screen):
	fond.play()
	def set_sound(self, instance):
		if fond.state == 'play':
			fond.stop()
			instance.background_normal = data.IMG_SOUND_OFF
		else:
			fond.play()
			instance.background_normal = data.IMG_SOUND_ON

	def load(self):
		#myQuest.getAllQuestion()
		#myQuest1.getAllQuestion()
		score_m.reset_score()
		score_m.reset_life()
		self.manager.get_screen('game1').score_lab = "0"
		self.manager.get_screen('game2').score_lab2 = "0"

		self.manager.get_screen('game1').life_3_1.color = (1, 1, 1, 1)
		self.manager.get_screen('game1').life_2_1.color = (1, 1, 1, 1)
		self.manager.get_screen('game1').life_1_1.color = (1, 1, 1, 1)

		self.manager.get_screen('game2').life_3_2.color = (1, 1, 1, 1)
		self.manager.get_screen('game2').life_2_2.color = (1, 1, 1, 1)
		self.manager.get_screen('game2').life_1_2.color = (1, 1, 1, 1)

	def load_score(self):
		""" Lorsqu'on appuie sur le bouton score de l'accueil
			on lit les donné du fichier score et on les affichre
			par ordre décroissante """
		sc = []
		with open("score.txt", 'r') as all_score:
			while 1:
				sc_tmp = all_score.readline()
				if sc_tmp == "":
					break
				sc.append(sc_tmp)

		try:
			score, date = sc[3].split(';')
			self.manager.get_screen('score').score_1 = f"{score} === {date}"
		except:
			self.manager.get_screen('score').score_1 = ""

		try:
			score, date = sc[2].split(';')
			self.manager.get_screen('score').score_2 = f"{score} === {date}"
		except:
			self.manager.get_screen('score').score_2 = ""

		try:
			score, date = sc[1].split(';')
			self.manager.get_screen('score').score_3 = f"{score} === {date}"
		except:
			self.manager.get_screen('score').score_3 = ""

		try:
			score, date = sc[0].split(';')
			self.manager.get_screen('score').score_4 = f"{score} === {date}"
		except:
			self.manager.get_screen('score').score_4 = ""

	def exit(self):
		sys.exit()

class ScoreScreen(Screen):
	score_1 = StringProperty('')
	score_2 = StringProperty('')
	score_3 = StringProperty('')
	score_4 = StringProperty('')

	def reset(self):
		self.score_1 = ''
		self.score_2 = ''
		self.score_3 = ''
		self.score_4 = ''

		with open('score.txt', 'w') as all_score:
			all_score.write("")

class AboutScreen(Screen):
	pass

class GameScreen1(Screen):
	score_lab = StringProperty("0")
	life_1_1 = ObjectProperty()
	life_2_1 = ObjectProperty()
	life_3_1 = ObjectProperty()
	#life_ = 3

	quest_1 = ObjectProperty()
	ans_a_1 = ObjectProperty()
	ans_b_1 = ObjectProperty()
	ans_c_1 = ObjectProperty()

	p_bar = ObjectProperty()

	def up_chrono(self, dt):
		
		if self.p_bar.value >= 20:
			err_sound.seek(0)
			err_sound.play()
			Clock.unschedule(self.up_chrono)
			if score_m.get_life() == 3:
				self.life_3_1.color = (1, 1, 1, 0)
				self.manager.get_screen('game2').life_3_2.color = (1, 1, 1, 0)
				score_m.set_life()
				self.manager.current = "game2"
			elif score_m.get_life() == 2:
				self.life_2_1.color = (1, 1, 1, 0)
				self.manager.get_screen('game2').life_2_2.color = (1, 1, 1, 0)
				score_m.set_life()
				self.manager.current = "game2"
			elif score_m.get_life() == 1:
				self.life_1_1.color = (1, 1, 1, 0)
				self.manager.get_screen('game2').life_1_2.color = (1, 1, 1, 0)
				score_m.set_life()
				#self.life_ = score_m.get_life()
				ph = str(score_m.is_high_score(score_m.get_score()))  + "\n\n" + score_m.get_score() 
				self.manager.get_screen('over').finalScore = ph
				self.manager.current = 'over'
			self.p_bar.value = 0
		self.p_bar.value += 1/20

	def on_pre_enter(self):
		myQuest.getQuestion()
		self.quest_1.text = myQuest.getRealQuestion()
		self.ans_a_1.text = myQuest.getAnswereA()
		self.ans_b_1.text = myQuest.getAnswereB()
		self.ans_c_1.text = myQuest.getAnswereC()


	def on_enter(self):
		Clock.schedule_interval(self.up_chrono, 1/25)

	def on_leave(self):
		self.p_bar.value = 0
		self.ans_a_1.background_color = (1, 1, 1, 0)
		self.ans_b_1.background_color = (1, 1, 1, 0)
		self.ans_c_1.background_color = (1, 1, 1, 0)

	def check(self, instance):
		err_sound.seek(0)
		true_sound.seek(0)
		Clock.unschedule(self.up_chrono)
		if instance.text == myQuest.trueAnswere:
			true_sound.play()
			score_m.set_score()
			self.score_lab = score_m.get_score()
			self.manager.get_screen('game2').score_lab2 = self.score_lab
			instance.background_color = (27/255, 243/255, 5/255, 1)
		else:
			err_sound.play()
			instance.background_color = (1, 0, 0, 1)
			if score_m.get_life() == 3:
				self.life_3_1.color = (1, 1, 1, 0)
				self.manager.get_screen('game2').life_3_2.color = (1, 1, 1, 0)
				score_m.set_life()
			elif score_m.get_life() == 2:
				self.life_2_1.color = (1, 1, 1, 0)
				self.manager.get_screen('game2').life_2_2.color = (1, 1, 1, 0)
				score_m.set_life()
			elif score_m.get_life() == 1:
				self.life_1_1.color = (1, 1, 1, 0)
				self.manager.get_screen('game2').life_1_2.color = (1, 1, 1, 0)
				score_m.set_life()
				#self.life_ = score_m.get_life()
				ph = str(score_m.is_high_score(score_m.get_score()))  + "\n\n" + score_m.get_score() 
				self.manager.get_screen('over').finalScore = ph
			
	def get_l(self):
		return score_m.get_life()
		
			
class GameScreen2(Screen):
	score_lab2 = StringProperty("0")
	life_1_2 = ObjectProperty()
	life_2_2 = ObjectProperty()
	life_3_2 = ObjectProperty()
	#life_ = 3

	quest_2 = ObjectProperty()
	ans_a_2 = ObjectProperty()
	ans_b_2 = ObjectProperty()
	ans_c_2 = ObjectProperty()

	p_bar_2 = ObjectProperty()

	def up_chrono_2(self, dt):
		
		if self.p_bar_2.value >= 20:
			err_sound.seek(0)
			err_sound.play()
			Clock.unschedule(self.up_chrono_2)
			if score_m.get_life() == 3:
				self.life_3_2.color = (1, 1, 1, 0)
				self.manager.get_screen('game1').life_3_1.color = (1, 1, 1, 0)
				score_m.set_life()
				self.manager.current = "game1"
			elif score_m.get_life() == 2:
				self.life_2_2.color = (1, 1, 1, 0)
				self.manager.get_screen('game1').life_2_1.color = (1, 1, 1, 0)
				score_m.set_life()
				self.manager.current = "game1"
			elif score_m.get_life() == 1:
				self.life_1_2.color = (1, 1, 1, 0)
				self.manager.get_screen('game1').life_1_1.color = (1, 1, 1, 0)
				score_m.set_life()
				#self.life_ = score_m.get_life()
				ph = str(score_m.is_high_score(score_m.get_score()))  + "\n\n" + score_m.get_score() 
				self.manager.get_screen('over').finalScore = ph
				self.manager.current = 'over'
		self.p_bar_2.value += 1/20


	def on_pre_enter(self):
		myQuest.getQuestion()
		self.quest_2.text = myQuest.getRealQuestion()
		self.ans_a_2.text = myQuest.getAnswereA()
		self.ans_b_2.text = myQuest.getAnswereB()
		self.ans_c_2.text = myQuest.getAnswereC()

	def on_enter(self):
		Clock.schedule_interval(self.up_chrono_2, 1/25)

	def on_leave(self):
		self.p_bar_2.value = 0
		self.ans_a_2.background_color = (1, 1, 1, 0)
		self.ans_b_2.background_color = (1, 1, 1, 0)
		self.ans_c_2.background_color = (1, 1, 1, 0)


	def check(self, instance):
		err_sound.seek(0)
		true_sound.seek(0)
		Clock.unschedule(self.up_chrono_2)
		if instance.text == myQuest.trueAnswere:
			true_sound.play()
			score_m.set_score()
			self.score_lab2 = score_m.get_score()
			self.manager.get_screen('game1').score_lab = self.score_lab2			
			instance.background_color = (27/255, 243/255, 5/255, 1)

		else:
			err_sound.play()
			instance.background_color = (1, 0, 0, 1)
			if score_m.get_life() == 3:
				self.life_3_2.color = (1, 1, 1, 0)
				self.manager.get_screen('game1').life_3_1.color = (1, 1, 1, 0)
				score_m.set_life()
			elif score_m.get_life() == 2:
				self.life_2_2.color = (1, 1, 1, 0)
				self.manager.get_screen('game1').life_2_1.color = (1, 1, 1, 0)
				score_m.set_life()
			elif score_m.get_life() == 1:
				self.life_1_2.color = (1, 1, 1, 0)
				self.manager.get_screen('game1').life_1_1.color = (1, 1, 1, 0)
				ph = str(score_m.is_high_score(score_m.get_score()))  + "\n\n" + score_m.get_score() 
				self.manager.get_screen('over').finalScore = ph
				score_m.set_life()
				#self.life_ = score_m.get_life()


	def get_l(self):
		return score_m.get_life()


class GameOver(Screen):
	finalScore = StringProperty("0")
	def load(self):
		score_m.reset_score()
		score_m.reset_life()
		self.manager.get_screen('game1').score_lab = "0"
		self.manager.get_screen('game2').score_lab2 = "0"

		self.manager.get_screen('game1').life_3_1.color = (1, 1, 1, 1)
		self.manager.get_screen('game1').life_2_1.color = (1, 1, 1, 1)
		self.manager.get_screen('game1').life_1_1.color = (1, 1, 1, 1)

		self.manager.get_screen('game2').life_3_2.color = (1, 1, 1, 1)
		self.manager.get_screen('game2').life_2_2.color = (1, 1, 1, 1)
		self.manager.get_screen('game2').life_1_2.color = (1, 1, 1, 1)


class Manager (ScreenManager):
	pass

kv = Builder.load_file("widget.kv")
# MainClass


class MainApp(App):
	def build(self):
		self.icon = 'icon.png'
		self.presplash = 'acc.png'
		return kv


MainApp().run()