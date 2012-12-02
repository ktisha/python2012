__author__ = 'sergio'

import sys
import random
import common_functions

def freq_dict(text, k_gramm_size):
    result = {}
    alphabet = {}
    k_gramm_count = 0
    for i in range(len(text) - k_gramm_size + 1):
        k_gramm = text[i : i + k_gramm_size]
        result[k_gramm] = result[k_gramm] + 1 if k_gramm in result else 1
        k_gramm_count += 1

        for char in k_gramm:
            alphabet[char] = True

    for k_gramm in result:
        result[k_gramm] *= 1.0 / k_gramm_count

    return result, alphabet

def make_random_decoder(key_set, value_set):
    value_list = [value for value in value_set]
    result = {}
    for key in key_set:
        result[key] = value_list[random.randrange(len(value_set))]
    return result

def decode(chipher_text, decoder):
    result = ''
    for char in chipher_text:
        result += decoder[char] if char in decoder else char
    return result

def decoder_quality(decoder, language_freq_dict, chipher_freq_dict, eps):

    result = 0;
    for first_char in decoder:
        for second_char in decoder:
            k_gramm = first_char + second_char
            decoded_k_gramm = decoder[first_char] + decoder[second_char]
            chipher_freq = chipher_freq_dict[k_gramm] if k_gramm in chipher_freq_dict else 0
            lang_freq = language_freq_dict[decoded_k_gramm] \
                if decoded_k_gramm in language_freq_dict else 0
            result += abs(lang_freq - chipher_freq) ** 2 # TODO: why?
    return result;

def one_point_crossover(first_decoder, second_decoder):
    key_list = [key for key in first_decoder] # предполагается, что у декодеров ключи совпадают
    genom_size = len(key_list)
    cross_point = random.randrange(genom_size)
    child_1 = {}
    child_2 = {}
    for i in range(genom_size):
        key = key_list[i]
        child_1[key], child_2[key] = (first_decoder[key], second_decoder[key]) \
            if i <= cross_point else (second_decoder[key], first_decoder[key])
    return child_1, child_2

def all_point_crossover(first_decoder, second_decoder, probability):
    child_1 = {}
    child_2 = {}
    for key in first_decoder:
        child_1[key], child_2[key] = (first_decoder[key], second_decoder[key]) \
            if random.random() > probability else (second_decoder[key], first_decoder[key])
    return child_1, child_2

def one_point_mutation(decoder):
    key_list = [key for key in decoder]
    value_list = [decoder[key] for key in decoder]
    values_count = len(value_list)
    genom_size = len(key_list)
    mutation_point = random.randrange(genom_size)
    child = {}
    for i in range(genom_size):
        key = key_list[i]
        child[key] = decoder[key] \
            if i <= mutation_point else value_list[random.randrange(values_count)]
    return child

def all_point_mutation(decoder, probability):
    value_list = [decoder[key] for key in decoder]
    values_count = len(value_list)
    child = {}
    for key in decoder:
        child[key] = decoder[key] \
            if random.random() > probability else value_list[random.randrange(values_count)]
    return child




def genetic_algorithm(language_freq_dict, language_alphabet, \
                       chipher_freq_dict, chipher_alphabet):
    population_size = 20
    eps = 0.000000001
    target_quality = 0.003
    all_point_crossover_probability = 0.1
    all_points_mutation_probability = 0.05

    # константы для встрясок
    progress_quality = 0.00001
    number_generations_since_last_improvement_for_shake = 5
    number_generations_since_last_improvement_for_big_shake = 15

    # генерируем много декодеров
    decoders = [make_random_decoder(chipher_alphabet, language_alphabet) \
        for i in range(1000)]
    decoders_with_qualities = [(decoder, \
        decoder_quality(decoder, language_freq_dict, chipher_freq_dict, eps)) \
        for decoder in decoders]
    decoders_with_qualities.sort(key = lambda x: x[1])
    decoders_with_qualities = decoders_with_qualities[:population_size]
    best_quality = decoders_with_qualities[0][1]
    generations_since_last_improvement = 0
    last_best_quality = 0
    while best_quality > target_quality:

        if abs(last_best_quality - best_quality) > progress_quality:
            generations_since_last_improvement = 0
        else : generations_since_last_improvement += 1
        last_best_quality = best_quality

        # встряска, если давно не было улучшения
        if generations_since_last_improvement % \
                number_generations_since_last_improvement_for_shake \
                == number_generations_since_last_improvement_for_shake - 1:
            print ("shake")
            for i in range( population_size // 10, population_size):
                child = all_point_mutation(decoders_with_qualities[i][0], 0.2)
                decoders_with_qualities[i] = \
                    (child, decoder_quality(child,language_freq_dict, chipher_freq_dict, eps))

        # большая встряска, если давно не было улучшения
        if generations_since_last_improvement % \
                number_generations_since_last_improvement_for_big_shake == \
                number_generations_since_last_improvement_for_big_shake - 1:
            print ("big shake")
            for key in decoders_with_qualities[0][0]:
                print (key, decoders_with_qualities[0][0][key])
            for i in range(population_size):
                child = all_point_mutation(decoders_with_qualities[i][0], 0.5) \
                    if random.random() > 0.5 else \
                    make_random_decoder(chipher_alphabet, language_alphabet)
                decoders_with_qualities[i] = \
                    (child, decoder_quality(child, language_freq_dict, chipher_freq_dict, eps))


        # скрещивание обоими способами
        for i in range(population_size):
            if random.random() < 0.25:
                for j in range(i):
                    if random.random() < 0.25:
                        child_1, child_2 = one_point_crossover(decoders_with_qualities[i][0], \
                            decoders_with_qualities[j][0])
                        child_3, child_4 = all_point_crossover(decoders_with_qualities[i][0], \
                            decoders_with_qualities[j][0], all_point_crossover_probability)
                        decoders_with_qualities.append((child_1, decoder_quality(child_1, \
                            language_freq_dict, chipher_freq_dict, eps)))
                        decoders_with_qualities.append((child_2, decoder_quality(child_2, \
                            language_freq_dict, chipher_freq_dict, eps)))
                        decoders_with_qualities.append((child_3, decoder_quality(child_3, \
                            language_freq_dict, chipher_freq_dict, eps)))
                        decoders_with_qualities.append((child_4, decoder_quality(child_4, \
                            language_freq_dict, chipher_freq_dict, eps)))

        # мутация обоими способами
        for i in range(population_size):
            child = one_point_mutation(decoders_with_qualities[i][0])
            decoders_with_qualities.append((child, \
                decoder_quality(child, language_freq_dict, chipher_freq_dict, eps)))

        for i in range(population_size):
            child = all_point_mutation(decoders_with_qualities[i][0], \
                all_points_mutation_probability)
            decoders_with_qualities.append((child, \
                decoder_quality(child, language_freq_dict, chipher_freq_dict, eps)))


        #отбор
        decoders_with_qualities.sort(key = lambda x: x[1])
        decoders_with_qualities = decoders_with_qualities[:population_size]

        #результат
        best_quality = decoders_with_qualities[0][1]
        print(best_quality)

    return decoders_with_qualities[0][0]


if __name__ == "__main__":
    gramm_size = 2
    big_text = common_functions.input_text(sys.argv[1])
    big_text_freq_dict, big_text_alphabet = freq_dict(big_text, gramm_size)
    chipher_text = common_functions.input_text(sys.argv[2])
    chipher_freq_dict, chipher_alphabet = freq_dict(chipher_text, gramm_size)

#    # тест freq_dict
#    print (len(chipher_alphabet))
#    for key in chipher_alphabet:
#        print (key)
#    print("\n", chipher_freq_dict)

    # тест make_random_decoder
    #random_decoder = make_random_decoder(chipher_alphabet, big_text_alphabet)
    #for key in random_decoder:
    #    print (key, random_decoder[key])

    #тест decoder_quality
#    ideal_decoder = {}
#    for key in chipher_alphabet:
#        ideal_decoder[key] = key

    #print(decoder_quality(random_decoder, big_text_freq_dict, chipher_freq_dict))
    #print(decoder_quality(ideal_decoder, big_text_freq_dict, chipher_freq_dict))

    # тест one_point_crossover
    # half_ideal_random_1, half_ideal_random_2 = \
    #   one_point_crossover(random_decoder, ideal_decoder)
    #for  key in half_ideal_random_2:
    #    print (key, half_ideal_random_2[key])

    # тест all_point_crossover
    # half_ideal_random_1, half_ideal_random_2 = \
    #   all_point_crossover(random_decoder, ideal_decoder)
    # for  key in half_ideal_random_2:
    #    print (key, half_ideal_random_2[key])

    # тест one_point_mutation
#    half_ideal_random = one_point_mutation(ideal_decoder)
#    for  key in half_ideal_random:
#        print (key, half_ideal_random[key])

    # запускаем генетический алгоритм
    random.seed()
    decoder = genetic_algorithm(big_text_freq_dict, big_text_alphabet, \
                                 chipher_freq_dict, chipher_alphabet)

    for key in decoder:
        print(key, decoder[key])

    decoded_text = decode(chipher_text, decoder)
    print(decoded_text)