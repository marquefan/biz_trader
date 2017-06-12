from db import *

class Brain:
	content = ""
	coinscores = []
	def rate_coin(self, coinlist):

		self.coinscores = [None] * len(coinlist)
		
		for index, coin in enumerate(coinlist):
			coin_id = get_id(coin[0])
			coin_average_mentions = get_val(coin_id, "average")
			coin_actual_mentions = get_val(coin_id, "value")
			coin_name = coin[0]
			coin_price_history = get_val(coin_id, "price_history")

			score = 10

			if coin_average_mentions == 0:
				# division by 0 not allowed!
				coin_average_mentions = 0.01
			mention_calculus = (coin_actual_mentions[-1] / float(coin_average_mentions))
		
			#exponent
			score = score ** mention_calculus
			
			self.coinscores[index] = score


		return self.coinscores
	def highest_score(self):
		highest = 0
		idx = -1

		for score in self.coinscores:
			if score > highest:
				highest = score
				idx = self.coinscores.index(score)
		return idx
	def read_file(self, file):
		try:
			with open(file, "r") as f:
				self.content = f.read()
				f.close()
		except:
			print "Failed while opening: ",file


"""
if __name__ == "__main__":
	testshit = Brain()
	test = Brain.rate_coin(testshit, "stratis")
	print test
"""