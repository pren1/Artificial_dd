'build model'
import tensorflow as tf
import pdb

class model_structure_loader(object):
	'load the lstm model'
	def __init__(self, characters, embedding_matrix, context_vector_length):
		self.EMBEDDING_DIM = 512
		self.HALF_EMBEDDING_DIM = int(self.EMBEDDING_DIM / 2)
		self.regularizer_coefficient = 0.00001
		self.context_vector_length = context_vector_length
		self.dict_length = len(characters)
		self.embedding_matrix = embedding_matrix

	def lstm_model(self, seq_len=30, batch_size=None, stateful=True):
		"""Language model: Encoder decoder favor for context term"""
		encoder_input = tf.keras.Input(name='Encoder_input', shape=(self.context_vector_length,), batch_size=batch_size, dtype=tf.int32)
		embedding_layer = tf.keras.layers.Embedding(input_dim=self.dict_length, output_dim=self.EMBEDDING_DIM,
		                                            embeddings_initializer=tf.keras.initializers.Constant(self.embedding_matrix),
		                                            trainable=False)
		encode_embedding = embedding_layer(encoder_input)
		enc_lstm1, forward_h, forward_c, backward_h, backward_c = tf.keras.layers.Bidirectional(
			tf.keras.layers.LSTM(self.HALF_EMBEDDING_DIM, name='encoder_lstm_1', return_state=True, return_sequences=True,
			                     kernel_regularizer=tf.keras.regularizers.l2(self.regularizer_coefficient)))(encode_embedding)
		state_h_1 = tf.keras.layers.concatenate([forward_h, backward_h])
		state_c_1 = tf.keras.layers.concatenate([forward_c, backward_c])
		enc_lstm1 = tf.keras.layers.Dropout(0.6)(enc_lstm1)
		encoder_states_1 = [state_h_1, state_c_1]

		enc_lstm2, forward_h, forward_c, backward_h, backward_c = tf.keras.layers.Bidirectional(
			tf.keras.layers.LSTM(self.HALF_EMBEDDING_DIM, name='encoder_lstm_2', return_state=True, return_sequences=True,
			                     kernel_regularizer=tf.keras.regularizers.l2(self.regularizer_coefficient)))(enc_lstm1)
		state_h_2 = tf.keras.layers.concatenate([forward_h, backward_h])
		state_c_2 = tf.keras.layers.concatenate([forward_c, backward_c])
		encoder_states_2 = [state_h_2, state_c_2]

		# Set up the decoder, using `encoder_states` as initial state.
		decoder_inputs = tf.keras.Input(name='Decoder_input', shape=(seq_len,), batch_size=batch_size, dtype=tf.int32)
		decode_embedding = embedding_layer(decoder_inputs)
		lstm_1_layer = tf.keras.layers.LSTM(self.EMBEDDING_DIM, name='decoder_lstm_1', stateful=stateful, return_state=True,
		                                    return_sequences=True,
		                                    kernel_regularizer=tf.keras.regularizers.l2(self.regularizer_coefficient))
		lstm_1, _, _ = lstm_1_layer(decode_embedding, initial_state=encoder_states_1)
		dropout_lstm_1 = tf.keras.layers.Dropout(0.6)(lstm_1)
		lstm_2_layer = tf.keras.layers.LSTM(self.EMBEDDING_DIM, name='decoder_lstm_2', stateful=stateful, return_state=True,
		                                    return_sequences=True,
		                                    kernel_regularizer=tf.keras.regularizers.l2(self.regularizer_coefficient))
		lstm_2, _, _ = lstm_2_layer(dropout_lstm_1, initial_state=encoder_states_2)
		dropout_lstm_2 = tf.keras.layers.Dropout(0.6)(lstm_2)

		'try to add attention here~'
		attention = tf.keras.layers.Dot(axes=[2, 2])([dropout_lstm_2, enc_lstm2])
		attention = tf.keras.layers.Activation('softmax', name='attention')(attention)
		context = tf.keras.layers.Dot(axes=[2, 1])([attention, enc_lstm2])
		decoder_combined_context = tf.keras.layers.concatenate([context, dropout_lstm_2])

		dense_layer_1 = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(self.EMBEDDING_DIM * 4, activation='tanh',
		                                                                      kernel_regularizer=tf.keras.regularizers.l2(
			                                                                      self.regularizer_coefficient)))
		predicted_char_layer = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(self.dict_length, activation='softmax',
		                                                                             kernel_regularizer=tf.keras.regularizers.l2(
			                                                                             self.regularizer_coefficient)))

		dense_layer_output_1 = dense_layer_1(decoder_combined_context)
		predicted_char = predicted_char_layer(dense_layer_output_1)

		Model = tf.keras.Model(inputs=[encoder_input, decoder_inputs], outputs=[predicted_char])
		Model.summary()
		# tf.keras.utils.plot_model(Model, show_shapes=True, to_file='./model_picture/model.png')

		'For reference, also prepared some tricks'
		encoder_model = tf.keras.Model(encoder_input,
		                               [encoder_states_1[0], encoder_states_1[1], encoder_states_2[0], encoder_states_2[1],
		                                enc_lstm2])
		# tf.keras.utils.plot_model(encoder_model, show_shapes=True, to_file='./model_picture/encoder_model.png')

		decoder_state_input_h = tf.keras.Input(shape=(self.EMBEDDING_DIM,))
		decoder_state_input_c = tf.keras.Input(shape=(self.EMBEDDING_DIM,))
		decoder_state_input_h1 = tf.keras.Input(shape=(self.EMBEDDING_DIM,))
		decoder_state_input_c1 = tf.keras.Input(shape=(self.EMBEDDING_DIM,))

		encoder_output_in = tf.keras.Input(shape=(self.context_vector_length, self.EMBEDDING_DIM,))
		decode_embedding = embedding_layer(decoder_inputs)
		decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c, decoder_state_input_h1,
		                         decoder_state_input_c1]
		d_o, state_h, state_c = lstm_1_layer(decode_embedding, initial_state=decoder_states_inputs[:2])
		d_o, state_h1, state_c1 = lstm_2_layer(d_o, initial_state=decoder_states_inputs[-2:])
		decoder_states = [state_h, state_c, state_h1, state_c1]

		'try to add attention here~'
		attention = tf.keras.layers.Dot(axes=[2, 2])([d_o, encoder_output_in])
		attention = tf.keras.layers.Activation('softmax', name='attention')(attention)
		context = tf.keras.layers.Dot(axes=[2, 1])([attention, encoder_output_in])
		decoder_combined_context = tf.keras.layers.concatenate([context, d_o])

		dense_layer_output_1 = dense_layer_1(decoder_combined_context)
		decoder_outputs = predicted_char_layer(dense_layer_output_1)
		decoder_model = tf.keras.Model([decoder_inputs] + decoder_states_inputs + [encoder_output_in],
		                               [decoder_outputs] + decoder_states)
		# tf.keras.utils.plot_model(decoder_model, show_shapes=True, to_file='./model_picture/decoder_model.png')

		return Model, encoder_model, decoder_model

	def get_stand_alone_decoder(self, seq_len=30, batch_size=None, stateful=True):
		decoder_state_input_h = tf.keras.Input(shape=(self.EMBEDDING_DIM,))
		decoder_state_input_c = tf.keras.Input(shape=(self.EMBEDDING_DIM,))
		decoder_state_input_h1 = tf.keras.Input(shape=(self.EMBEDDING_DIM,))
		decoder_state_input_c1 = tf.keras.Input(shape=(self.EMBEDDING_DIM,))

		decoder_inputs = tf.keras.Input(name='Decoder_input', shape=(seq_len,), batch_size=batch_size, dtype=tf.int32)

		encoder_output_in = tf.keras.Input(shape=(self.context_vector_length, self.EMBEDDING_DIM,))

		embedding_layer = tf.keras.layers.Embedding(input_dim=self.dict_length, output_dim=self.EMBEDDING_DIM,
		                                            embeddings_initializer=tf.keras.initializers.Constant(self.embedding_matrix),
		                                            trainable=False)
		decode_embedding = embedding_layer(decoder_inputs)
		decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c, decoder_state_input_h1,
		                         decoder_state_input_c1]
		lstm_1_layer = tf.keras.layers.LSTM(self.EMBEDDING_DIM, name='decoder_lstm_1', stateful=stateful, return_state=True,
		                                    return_sequences=True)
		d_o, state_h, state_c = lstm_1_layer(decode_embedding, initial_state=decoder_states_inputs[:2])
		lstm_2_layer = tf.keras.layers.LSTM(self.EMBEDDING_DIM, name='decoder_lstm_2', stateful=stateful, return_state=True,
		                                    return_sequences=True)
		d_o, state_h1, state_c1 = lstm_2_layer(d_o, initial_state=decoder_states_inputs[-2:])
		decoder_states = [state_h, state_c, state_h1, state_c1]

		'try to add attention here~'
		attention = tf.keras.layers.Dot(axes=[2, 2])([d_o, encoder_output_in])
		attention = tf.keras.layers.Activation('softmax', name='attention')(attention)
		context = tf.keras.layers.Dot(axes=[2, 1])([attention, encoder_output_in])
		decoder_combined_context = tf.keras.layers.concatenate([context, d_o])

		dense_layer_1 = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(self.EMBEDDING_DIM * 4, activation='tanh'))
		predicted_char_layer = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(self.dict_length, activation='softmax'))

		dense_layer_output_1 = dense_layer_1(decoder_combined_context)
		decoder_outputs = predicted_char_layer(dense_layer_output_1)
		decoder_model = tf.keras.Model([decoder_inputs] + decoder_states_inputs + [encoder_output_in],
		                               [decoder_outputs] + decoder_states)
		# tf.keras.utils.plot_model(decoder_model, show_shapes=True, to_file='./model_picture/decoder_model.png')
		return decoder_model