#!/usr/bin/env python
#-*- encoding:utf8 -*-

import json

def listelem(data):
    res = u""
    for d in data:
        if isinstance(d, dict):
            idt = dictelem(d)
        elif isinstance(d, list):
            idt = listelem(d)
        else:
            idt = d
        res += u"""<li>{t}</li>""".format(t=idt)
    return u"<ul>{0}</ul>".format(res)



def dictelem(data):
    res = u""
    for k, v in data.iteritems():
        if isinstance(v, list):
            idt = listelem(v)
        elif isinstance(v, dict):
            idt = dictelem(v)
        else:
            idt = v
        res += u"""<div property="{p}">{t}</div>""".format(p=k, t=idt)
    return u"<div>{0}</div>".format(res)

def main(doc):
    data = doc if isinstance(doc, dict) else json.loads(doc)
    return dictelem(data)

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        for doc in sys.argv[1:]:
            print main(doc)
    else:
        testjson = u"""
        {
            "rating" : 4.8,
            "restaurant_tips" : "10元起送 / 41分钟 / 639米",
            "address" : "南京艺术学院",
            "is_new" : false,
            "business_district" : "",
            "is_time_ensure" : false,
            "is_premium" : false,
            "minimum_order_amount" : 10,
            "is_online_payment" : true,
            "id" : 75093,
            "description" : "为了大家的放心美味不断的在努力。",
            "flavors" : "中式",
            "is_in_book_time" : true,
            "is_support_invoice" : false,
            "opening_hours" : [
                    "00:00/01:20",
                    "10:00/15:00",
                    "16:20/24:00"
            ],
            "month_sales" : 4320,
            "minimum_invoice_amount" : 0,
            "rating_count" : 165,
            "latitude" : 32.064029,
            "minimum_order_description" : "",
            "supports" : [
                    {
                            "icon_name" : "付",
                            "description" : "可使用支付宝、微信、手机QQ进行在线支付",
                            "id" : 3,
                            "icon_color" : "FF4E00",
                            "name" : "支持在线支付"
                    }
            ],
            "status" : 1,
            "is_insurance" : false,
            "delivery_mode" : {
                    "color" : "899BB8",
                    "text" : "餐厅配送",
                    "is_solid" : false,
                    "id" : 2
            },
            "image_path" : "/7/9e/a9a03ca99046f541a9b03e49a425ejpeg.jpeg",
            "is_third_party_delivery" : false,
            "promotion_info" : "用餐高峰期，请提前订餐！1.为保证您获得最佳的用餐体验，请提前预定。2.首次下单请预留正确的地址和电话，确保您能及时用餐，祝您用餐愉快！",
            "phone" : "18100616601   18100617701",
            "time_ensure_full_description" : "",
            "is_coupon_enabled" : false,
            "distance" : 639,
            "is_free_delivery" : true,
            "name" : "浪花餐厅",
            "minimum_free_delivery_amount" : 0,
            "food_tips" : "(165) 月售4320份",
            "order_mode" : 9,
            "longitude" : 118.753245,
            "delivery_fee" : 0,
            "next_business_time" : "16:20",
            "name_for_url" : "nylhct",
            "order_lead_time" : 41
        }"""    
        print main(testjson)
