import sys
f = open('input9.txt', "w")
i = 1
n = 12
m = 10
f.write(str(n))
f.write(' ')
f.write(str(m))
f.write('\n')
f.write('1 1 ')
f.write(str(n))
f.write(' ')
f.write(str(m))
f.write('\n')
f.write('4\n')
while i <= n:
        j = 1
        while j <= m:
                if ((i*j + 3*i + 2*j - i*i*i*j) % 5 == 0 or (i*j + 3*i + 2*j - i*i*i*j) % 5 == 1):
                        a = '0 '
                        a = a + str(i)
                        a = a + ' '
                        a = a + str(j)
                        f.write(a)
                        f.write('\n')
                if ((i*j + 3*i + 2*j - i*i*i*j + i*j*j - 1 + 2*j) % 5 == 2 or (i*j + 3*i + 2*j - i*i*i*j + i*j*j - 1 + 2*j) % 5 == 1):
                        a = '1 '
                        a = a + str(i)
                        a = a + ' '
                        a = a + str(j)
                        f.write(a)
                        f.write('\n')
                j = j + 1
        i = i + 1
i = 1
while i <= n:
        j = 1
        while j <= m:
                if ((i*j + 3*i + 2*j - i*i*i*j) % 7 == 0 or (i*j + 3*i + 2*j - i*i*i*j) % 7 == 1):
                        a = '0 '
                        a = a + str(i)
                        a = a + ' '
                        a = a + str(j)
                        f.write(a)
                        f.write('\n')
                if ((i*j + 3*i + 2*j - i*i*i*j + i*j*j - 1 + 2*j) % 7 == 0 or (i*j + 3*i + 2*j - i*i*i*j + i*j*j - 1 + 2*j) % 7 == 1):
                        a = '1 '
                        a = a + str(i)
                        a = a + ' '
                        a = a + str(j)
                        f.write(a)
                        f.write('\n')
                j = j + 1
        i = i + 1
f.close()
print ('Ready!')
