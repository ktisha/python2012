# coding=utf-8
from result_analyser import aggregate_tag_for_test, aggregate_tag
import time

def test():
    with open("2.5_tag", "r") as file:
        tags = map(str.strip, file.readlines())
    print("Finish reading")

    with open("test_res", "w") as output:
        c = 0
        start_time=time.time()
        for tag in tags:
            c += 1
            answers = aggregate_tag_for_test(tag)
            for answer in answers:
                output.write(answer + "\n")
            if c % 100 == 0:
                print (c)
                print (time.time() - start_time, "seconds")
                start_time = time.time()

#create_normalized_index()
#create_indexes()

aggregate_tag("galaxy gt i9001 plus s samsung отзыв")
print("*")
aggregate_tag_for_test("galaxy gt i9001 plus s samsung отзыв")

test()

#key = "logitech"
#print r.smembers(key)
#key = r.randomkey()
#print key

#aggregate_tag("ежики мылились 1 1 1 3 4 5")
#aggregate_tag_for_test("ежики мылились 1 1 1 3 4 5")
#print aggregate_tag_for_test("galaxy gt i9001 plus s samsung отзыв")
#aggregate_tag("000021 1 2 3 941 driving force gt logitech")
#aggregate_tag("black ericsson mini sony st15i xperia")
#aggregate_tag("Стильный и функциональный пылесос от известного производителя!")
#aggregate_tag("Пылесосы и пылесборники")
#aggregate_tag("nikon Coolpix S8200")
#aggregate_tag("8 blackbox xdevice видеорегистратор")
#aggregate_tag("325 clp")


#aggregate_tag("oregon scientific")
#r = redis_connect(1)
#print r.get("8990")
#print r.get("8991")
#print r.get("8992")
#print r.get("8993")

'''
aggregate_tag("galaxy gt i9001 plus s samsung отзыв")
f = open("example", "r")
for line in f:
    aggregate_tag(line.strip())

f.close()
'''
