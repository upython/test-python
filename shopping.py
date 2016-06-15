#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by   2016/06/15


import sys

commodity = {
'apple':5000,
'android':8000,
'samsung':2000,
'mi':1500,
'huawei':6000
    }

shopcar = []


pice = int(raw_input('Please Enter your salary:'))
# pice = 10000

if pice < min(commodity.values()):
    print 'You are a beast so little money to support their families ah ye'
    sys.exit()
if pice > 50000:
    print 'Tyrant uncle, welcome your arrival'
# print commodity.values()
while True:
    for k,v in enumerate(commodity.items(),1):
        print k,v[0],':',v[1]

    while True:#购物循环

        basket = raw_input('Please Enter your id in car:')
        if basket =='q':
            print 'Welcome Kuan Lin again Bye,bye'
            print 'Shopping List',shopcar
            sys.exit()
        elif basket =='y':
            print 'balance:',pice

        elif basket =='l':
            print shopcar
        elif len(basket)==0:
            print 'You enter something silly X'
            break

        elif commodity.has_key(basket):

            if pice >= commodity.get(basket):
                shopcar.append(basket)

                pice = pice - commodity.get(basket)


                print 'your shoping car is ',shopcar
            else:
                print ' Insufficient balance:', pice
            if pice < min(commodity.values()):
                print 'The remaining balance of inadequate',pice

        else:
            print 'Please Taobao shopping...'



        elif basket == 'l':
            print shopcar
        elif len(basket) == 0:
            print 'You enter something silly X'
            break

        elif commodity.has_key(basket):

            if pice >= commodity.get(basket):
                shopcar.append(basket)

                pice = pice - commodity.get(basket)

                print 'your shoping car is ', shopcar
            else:
                print ' Insufficient balance:', pice
            if pice < min(commodity.values()):
                print 'The remaining balance of inadequate', pice

        else:
            print 'Please Taobao shopping...'
