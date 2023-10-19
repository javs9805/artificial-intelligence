import checkers
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from keras.models import model_from_json
import matplotlib.pyplot as plot

# Metrics model, which only looks at heuristic scoring metrics used for labeling
metrics_model = Sequential()
metrics_model.add(Dense(32, activation='relu', input_dim=10)) 
metrics_model.add(Dense(16, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))

# output is passed to relu() because labels are binary
metrics_model.add(Dense(1, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))
metrics_model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=["acc"])

start_board = checkers.expand(checkers.np_board())
boards_list = checkers.generate_next(start_board)
branching_position = 0
nmbr_generated_game = 1000
while len(boards_list) < nmbr_generated_game:
	temp = len(boards_list) - 1
	for i in range(branching_position, len(boards_list)):
		if (checkers.possible_moves(checkers.reverse(checkers.expand(boards_list[i]))) > 0):
				boards_list = np.vstack((boards_list, checkers.generate_next(checkers.reverse(checkers.expand(boards_list[i])))))
	branching_position = temp

# calculate/save heuristic metrics for each game state
metrics	= np.zeros((0, 10))
winning = np.zeros((0, 1))

for board in boards_list[:nmbr_generated_game]:
	temp = checkers.get_metrics(board)
	metrics = np.vstack((metrics, temp[1:]))
	winning  = np.vstack((winning, temp[0]))
 
# Entrenar el modelo con datos de validación
history = metrics_model.fit(metrics, winning, epochs=32, batch_size=64, verbose=0, validation_split=0.2)

# Historial de precisión
plot.plot(history.history['acc'])
plot.plot(history.history['val_acc'])  # Esta línea debería funcionar ahora
plot.title('Precisión del modelo')
plot.ylabel('precisión')
plot.xlabel('época')
plot.legend(['entrenamiento', 'validación'], loc='upper left')
plot.show()

# Historial de pérdida
plot.plot(history.history['loss'])
plot.plot(history.history['val_loss'])
plot.title('Pérdida del modelo')
plot.ylabel('pérdida')
plot.xlabel('época')
plot.legend(['entrenamiento', 'validación'], loc='upper left')
plot.show()

# Board model
board_model = Sequential()

# input dimensions is 32 board position values
board_model.add(Dense(64 , activation='relu', input_dim=32))

# use regularizers, to prevent fitting noisy labels
board_model.add(Dense(32 , activation='relu', kernel_regularizer=regularizers.l2(0.01)))
board_model.add(Dense(16 , activation='relu', kernel_regularizer=regularizers.l2(0.01))) # 16
board_model.add(Dense(8 , activation='relu', kernel_regularizer=regularizers.l2(0.01))) # 8

# output isn't squashed, because it might lose information
board_model.add(Dense(1 , activation='linear', kernel_regularizer=regularizers.l2(0.01)))
board_model.compile(optimizer='nadam', loss='binary_crossentropy')

# calculate heuristic metric for data
metrics = np.zeros((0, 10))
winning = np.zeros((0, 1))
data = boards_list

print("Termino - parte 1")
contador = 0
for board in data:
	temp = checkers.get_metrics(board)
	metrics = np.vstack((metrics, temp[1:]))
	winning  = np.vstack((winning, temp[0]))
	contador = contador +1
	print(contador)

# calculate probilistic (noisy) labels
probabilistic = metrics_model.predict_on_batch(metrics)

# fit labels to {-1, 1}
probabilistic = np.sign(probabilistic)

# calculate confidence score for each probabilistic label using error between probabilistic and weak label
confidence = 1 / (1 + np.absolute(winning - probabilistic))
confidence = confidence.reshape(-1, 1)  # Asegúrate de que confidence tenga la forma (1889, 1)

# pass to the Board model
board_model.fit(data, probabilistic, epochs=32, batch_size=64, sample_weight=confidence, verbose=0)

board_json = board_model.to_json()
with open('board_model.json', 'w') as json_file:
	json_file.write(board_json)
board_model.save_weights('board_model.h5')

print('Checkers Board Model saved to: board_model.json/h5')


json_file = open('board_model.json', 'r')
board_json = json_file.read()
json_file.close()
print("board_json")
print(board_json)

print("comienzo reinforced_model")
reinforced_model = model_from_json(board_json)
reinforced_model.load_weights('board_model.h5')
reinforced_model.compile(optimizer='adadelta', loss='mean_squared_error')
print("termino reinforced_model")

data = np.zeros((1, 32))
labels = np.zeros(1)
win = lose = draw = 0
winrates = []
learning_rate = 0.5
discount_factor = 0.95
contador = 0
print("comienzo del for")
for gen in range(0, 50):
	print("gen")
	for game in range(0, 20):
		print("game")
		temp_data = np.zeros((1, 32))
		board = checkers.expand(checkers.np_board())
		player = np.sign(np.random.random() - 0.5)
		turn = 0
		while (True):
			moved = False
			boards = np.zeros((0, 32))
			if (player == 1):
				boards = checkers.generate_next(board)
			else:
				boards = checkers.generate_next(checkers.reverse(board))

			scores = reinforced_model.predict_on_batch(boards)
			max_index = np.argmax(scores)
			best = boards[max_index]

			if (player == 1):
				board = checkers.expand(best)
				temp_data = np.vstack((temp_data, checkers.compress(board)))
			else:
				board = checkers.reverse(checkers.expand(best))

			player = -player

			# punish losing games, reward winners  & drawish games reaching more than 200 turns
			winner = checkers.game_winner(board)
			if (winner == 1 or (winner == 0 and turn >= 200) ):
				if winner == 1:
					win = win + 1
				else:
					draw = draw + 1
				reward = 10
				old_prediction = reinforced_model.predict_on_batch(temp_data[1:])
				optimal_futur_value = np.ones(old_prediction.shape)
				temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
				data = np.vstack((data, temp_data[1:]))
				labels = np.vstack((labels, temp_labels))
				break
			elif (winner == -1):
				lose = lose + 1
				reward = -10
				old_prediction = reinforced_model.predict_on_batch(temp_data[1:])
				optimal_futur_value = -1*np.ones(old_prediction.shape)
				temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
				data = np.vstack((data, temp_data[1:]))
				labels = np.vstack((labels, temp_labels))
				break
			turn = turn + 1

		if ((game+1) % 200 == 0):
			reinforced_model.fit(data[1:], labels[1:], epochs=16, batch_size=256, verbose=0)
			data = np.zeros((1, 32))
			labels = np.zeros(1)
	winrate = int((win+draw)/(win+draw+lose)*100)
	winrates.append(winrate)
 
	reinforced_model.save_weights('reinforced_model.h5')
	contador = contador +1
	print(contador)
 
print('Checkers Board Model updated by reinforcement learning & saved to: reinforced_model.json/h5')
 
print("data")
print(len(data))
print("probabilistic")
print(len(probabilistic))
print("confidence")
print(len(confidence))

print("Entradas al modelo")
print("Data shape:", data.shape)
print("Probabilistic shape:", probabilistic.shape)
print("winning:", winning.shape)


print("Dimensiones de confidence")
print("Confidence shape:", confidence.shape)

generations = range(0, 50)
print("Final win/draw rate : " + str(winrates[49])+"%" )
plot.plot(generations,winrates)
plot.show()
