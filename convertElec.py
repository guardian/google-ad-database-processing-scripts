#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import simplejson as json

with open('poa-to-ced2.json') as json_file:
    postcodes = json.load(json_file)

# row = {}
# row['Geo_Targeting_Included'] = "4304,Queensland,Australia, 4158,Queensland,Australia, 4512,Queensland,Australia, 4873,Queensland,Australia, 4133,Queensland,Australia, 4305,Queensland,Australia, 4131,Queensland,Australia, 4036,Queensland,Australia, 4881,Queensland,Australia, 4521,Queensland,Australia, 4154,Queensland,Australia, 4506,Queensland,Australia, 4500,Queensland,Australia, 4507,Queensland,Australia, 4035,Queensland,Australia, 4155,Queensland,Australia, 4511,Queensland,Australia, 4875,Queensland,Australia, 4157,Queensland,Australia, 4505,Queensland,Australia, 4520,Queensland,Australia, 4814,Queensland,Australia, 4874,Queensland,Australia, 4022,Queensland,Australia, 4165,Queensland,Australia, 4129,Queensland,Australia, 4125,Queensland,Australia, 4515,Queensland,Australia, 4502,Queensland,Australia, 4153,Queensland,Australia, 4172,Queensland,Australia, 4164,Queensland,Australia, 4312,Queensland,Australia, 4205,Queensland,Australia, 4306,Queensland,Australia, 4159,Queensland,Australia, 4019,Queensland,Australia, 4509,Queensland,Australia, 4311,Queensland,Australia, 4818,Queensland,Australia, 4037,Queensland,Australia, 4340,Queensland,Australia, 4895,Queensland,Australia, 4870,Queensland,Australia, 4508,Queensland,Australia, 4122,Queensland,Australia, 4510,Queensland,Australia, 4346,Queensland,Australia, 4812,Queensland,Australia, 4163,Queensland,Australia, 4161,Queensland,Australia, 4514,Queensland,Australia, 4313,Queensland,Australia, 4876,Queensland,Australia, 4877,Queensland,Australia, 4020,Queensland,Australia, 4130,Queensland,Australia, 4301,Queensland,Australia, 4819,Queensland,Australia, 4156,Queensland,Australia, 4179,Queensland,Australia, 4128,Queensland,Australia, 4504,Queensland,Australia, 4173,Queensland,Australia, 4207,Queensland,Australia, 4879,Queensland,Australia, 4303,Queensland,Australia, 4878,Queensland,Australia, 4810,Queensland,Australia, 4184,Queensland,Australia, 4817,Queensland,Australia, 4025,Queensland,Australia, 4174,Queensland,Australia, 4160,Queensland,Australia, 4516,Queensland,Australia, 4868,Queensland,Australia, 4178,Queensland,Australia, 4183,Queensland,Australia, 4501,Queensland,Australia, 4815,Queensland,Australia, 4503,Queensland,Australia, 4021,Queensland,Australia, 6107,Western Australia,Australia, 6024,Western Australia,Australia, 6065,Western Australia,Australia, 6022,Western Australia,Australia, 6021,Western Australia,Australia, 6061,Western Australia,Australia, 6066,Western Australia,Australia, 6068,Western Australia,Australia, 6090,Western Australia,Australia, 6064,Western Australia,Australia, 6067,Western Australia,Australia, 6079,Western Australia,Australia, 6071,Western Australia,Australia, 6055,Western Australia,Australia, 6063,Western Australia,Australia, 6104,Western Australia,Australia, 6062,Western Australia,Australia, 6102,Western Australia,Australia, 6106,Western Australia,Australia, 6103,Western Australia,Australia, 6152,Western Australia,Australia, 6101,Western Australia,Australia, 6100,Western Australia,Australia, 6105,Western Australia,Australia, 6151,Western Australia,Australia, 6057,Western Australia,Australia, 6058,Western Australia,Australia, 6070,Western Australia,Australia, 6072,Western Australia,Australia, 6076,Western Australia,Australia, 6081,Western Australia,Australia, 6073,Western Australia,Australia, 6056,Western Australia,Australia, 6069,Western Australia,Australia, 6082,Western Australia,Australia, 6083,Western Australia,Australia, 6558,Western Australia,Australia, 6074,Western Australia,Australia, 6556,Western Australia,Australia, 6077,Western Australia,Australia, 6032,Western Australia,Australia, 6078,Western Australia,Australia, 6031,Western Australia,Australia, 6030,Western Australia,Australia, 6036,Western Australia,Australia, 6038,Western Australia,Australia, 6034,Western Australia,Australia, 6033,Western Australia,Australia, 6035,Western Australia,Australia, 6037,Western Australia,Australia, 0800,Northern Territory,Australia, 0820,Northern Territory,Australia, 0812,Northern Territory,Australia, 0828,Northern Territory,Australia, 0810,Northern Territory,Australia, 0832,Northern Territory,Australia, 0830,Northern Territory,Australia, 5045,South Australia,Australia, 5150,South Australia,Australia, 5052,South Australia,Australia, 5062,South Australia,Australia, 5041,South Australia,Australia, 5039,South Australia,Australia, 5042,South Australia,Australia, 5050,South Australia,Australia, 5049,South Australia,Australia, 5047,South Australia,Australia, 5043,South Australia,Australia, 5048,South Australia,Australia, 5044,South Australia,Australia, 5046,South Australia,Australia, 3321,Victoria,Australia, 3331,Victoria,Australia, 3223,Victoria,Australia, 3225,Victoria,Australia, 3943,Victoria,Australia, 3944,Victoria,Australia, 3226,Victoria,Australia, 3222,Victoria,Australia, 3224,Victoria,Australia, 3227,Victoria,Australia, 3942,Victoria,Australia, 3217,Victoria,Australia, 3228,Victoria,Australia, 3221,Victoria,Australia, 3240,Victoria,Australia, 3941,Victoria,Australia, 3939,Victoria,Australia, 3929,Victoria,Australia, 3916,Victoria,Australia, 3937,Victoria,Australia, 3928,Victoria,Australia, 3938,Victoria,Australia, 3940,Victoria,Australia, 3936,Victoria,Australia, 3934,Victoria,Australia, 3915,Victoria,Australia, 3926,Victoria,Australia, 3933,Victoria,Australia, 3931,Victoria,Australia, 3930,Victoria,Australia, 3912,Victoria,Australia, 3913,Victoria,Australia, 3918,Victoria,Australia, 3919,Victoria,Australia, 3927,Victoria,Australia, 3920,Victoria,Australia, 3200,Victoria,Australia, 3910,Victoria,Australia, 3911,Victoria,Australia, 3198,Victoria,Australia, 3201,Victoria,Australia, 3806,Victoria,Australia, 3808,Victoria,Australia, 3807,Victoria,Australia, 3978,Victoria,Australia, 3809,Victoria,Australia, 3810,Victoria,Australia, 3160,Victoria,Australia, 3158,Victoria,Australia, 3785,Victoria,Australia, 3789,Victoria,Australia, 3159,Victoria,Australia, 3782,Victoria,Australia, 3795,Victoria,Australia, 3786,Victoria,Australia, 3787,Victoria,Australia, 3767,Victoria,Australia, 3765,Victoria,Australia, 3788,Victoria,Australia, 3793,Victoria,Australia, 3792,Victoria,Australia, 3791,Victoria,Australia, 3770,Victoria,Australia, 3116,Victoria,Australia, 3136,Victoria,Australia, 3140,Victoria,Australia, 3796,Victoria,Australia, 3766,Victoria,Australia, 3138,Victoria,Australia, 3759,Victoria,Australia, 3096,Victoria,Australia, 3091,Victoria,Australia, 3132,Victoria,Australia, 3137,Victoria,Australia, 3135,Victoria,Australia, 3134,Victoria,Australia, 3133,Victoria,Australia, 3131,Victoria,Australia, 3151,Victoria,Australia, 3125,Victoria,Australia, 3128,Victoria,Australia, 3089,Victoria,Australia, 3090,Victoria,Australia, 3754,Victoria,Australia, 3430,Victoria,Australia, 3148,Victoria,Australia, 3800,Victoria,Australia, 3149,Victoria,Australia, 3150,Victoria,Australia, 3199,Victoria,Australia, 3440,Victoria,Australia, 3437,Victoria,Australia, 3438,Victoria,Australia, 3431,Victoria,Australia, 3432,Victoria,Australia, 3433,Victoria,Australia, 3442,Victoria,Australia, 3441,Victoria,Australia, 3764,Victoria,Australia, 3756,Victoria,Australia, 3434,Victoria,Australia, 3435,Victoria,Australia, 3755,Victoria,Australia, 3751,Victoria,Australia, 3753,Victoria,Australia, 3758,Victoria,Australia, 3762,Victoria,Australia, 3757,Victoria,Australia, 3099,Victoria,Australia, 3760,Victoria,Australia, 3761,Victoria,Australia, 3775,Victoria,Australia, 2250,New South Wales,Australia, 2256,New South Wales,Australia, 2756,New South Wales,Australia, 2757,New South Wales,Australia, 2754,New South Wales,Australia, 2758,New South Wales,Australia, 2782,New South Wales,Australia, 2778,New South Wales,Australia, 2783,New South Wales,Australia, 2780,New South Wales,Australia, 2785,New South Wales,Australia, 2784,New South Wales,Australia, 2786,New South Wales,Australia, 2776,New South Wales,Australia, 2779,New South Wales,Australia, 2747,New South Wales,Australia, 2777,New South Wales,Australia, 2773,New South Wales,Australia, 2774,New South Wales,Australia, 2745,New South Wales,Australia, 2748,New South Wales,Australia, 2750,New South Wales,Australia, 2760,New South Wales,Australia, 2749,New South Wales,Australia, 2753,New South Wales,Australia, 2146,New South Wales,Australia, 2145,New South Wales,Australia, 2115,New South Wales,Australia, 2118,New South Wales,Australia, 2117,New South Wales,Australia, 2121,New South Wales,Australia, 2151,New South Wales,Australia, 2116,New South Wales,Australia, 2127,New South Wales,Australia, 2142,New South Wales,Australia, 2046,New South Wales,Australia, 2112,New South Wales,Australia, 2122,New South Wales,Australia, 2128,New South Wales,Australia, 2114,New South Wales,Australia, 2109,New South Wales,Australia, 2113,New South Wales,Australia, 2111,New South Wales,Australia, 2138,New South Wales,Australia, 2140,New South Wales,Australia, 2047,New South Wales,Australia, 2132,New South Wales,Australia, 2134,New South Wales,Australia, 2222,New South Wales,Australia, 2210,New South Wales,Australia, 2209,New South Wales,Australia, 2223,New South Wales,Australia, 2218,New South Wales,Australia, 2135,New South Wales,Australia, 2137,New South Wales,Australia, 2150,New South Wales,Australia, 2160,New South Wales,Australia, 2221,New South Wales,Australia, 2212,New South Wales,Australia, 2211,New South Wales,Australia, 2213,New South Wales,Australia, 2535,New South Wales,Australia, 2533,New South Wales,Australia, 2534,New South Wales,Australia, 2541,New South Wales,Australia, 2538,New South Wales,Australia, 2539,New South Wales,Australia, 2622,New South Wales,Australia, 2536,New South Wales,Australia, 2537,New South Wales,Australia, 2621,New South Wales,Australia, 2620,Australia, 2619,New South Wales,Australia, 2582,New South Wales,Australia, 2584,New South Wales,Australia, 2618,Australia, 2720,New South Wales,Australia, 2729,New South Wales,Australia, 2730,New South Wales,Australia, 2653,New South Wales,Australia, 2625,New South Wales,Australia, 3777,Victoria,Australia, 3799,Victoria,Australia, 3815,Victoria,Australia, 3797,Victoria,Australia, 3139,Victoria,Australia, 3781,Victoria,Australia, 3783,Victoria,Australia, 3812,Victoria,Australia, 3813,Victoria,Australia, 3814,Victoria,Australia, 3981,Victoria,Australia, 2551,New South Wales,Australia, 2549,New South Wales,Australia, 2550,New South Wales,Australia, 2631,New South Wales,Australia, 2632,New South Wales,Australia, 2627,New South Wales,Australia, 2628,New South Wales,Australia, 2624,New South Wales,Australia, 2629,New South Wales,Australia, 2626,New South Wales,Australia, 2630,New South Wales,Australia, 2545,New South Wales,Australia, 2546,New South Wales,Australia, 2548,New South Wales,Australia, 2251,New South Wales,Australia, 2257,New South Wales,Australia, 2260,New South Wales,Australia, 2258,New South Wales,Australia, 2261,New South Wales,Australia, 2259,New South Wales,Australia, 2262,New South Wales,Australia, 2263,New South Wales,Australia, 2280,New South Wales,Australia, 2281,New South Wales,Australia, 2326,New South Wales,Australia, 2327,New South Wales,Australia, 2323,New South Wales,Australia, 2282,New South Wales,Australia, 2290,New South Wales,Australia, 2306,New South Wales,Australia, 2322,New South Wales,Australia, 2320,New South Wales,Australia, 2321,New South Wales,Australia, 2318,New South Wales,Australia, 2316,New South Wales,Australia, 2319,New South Wales,Australia, 2324,New South Wales,Australia, 2317,New South Wales,Australia, 2315,New South Wales,Australia, 7469,Tasmania,Australia, 7467,Tasmania,Australia, 7468,Tasmania,Australia, 7178,Tasmania,Australia, 7179,Tasmania,Australia, 7184,Tasmania,Australia, 7182,Tasmania,Australia, 7180,Tasmania,Australia, 7172,Tasmania,Australia, 7173,Tasmania,Australia, 7177,Tasmania,Australia, 7174,Tasmania,Australia, 7026,Tasmania,Australia, 7171,Tasmania,Australia, 7025,Tasmania,Australia, 7017,Tasmania,Australia, 7139,Tasmania,Australia, 7140,Tasmania,Australia, 7302,Tasmania,Australia, 7300,Tasmania,Australia, 7291,Tasmania,Australia, 7301,Tasmania,Australia, 7250,Tasmania,Australia, 7290,Tasmania,Australia, 7258,Tasmania,Australia, 7249,Tasmania,Australia, 7248,Tasmania,Australia, 7259,Tasmania,Australia, 7212,Tasmania,Australia, 7214,Tasmania,Australia, 7211,Tasmania,Australia, 7213,Tasmania,Australia, 7215,Tasmania,Australia, 7190,Tasmania,Australia, 7209,Tasmania,Australia, 7210,Tasmania,Australia, 7120,Tasmania,Australia, 7030,Tasmania,Australia, 7027,Tasmania,Australia, 7216,Tasmania,Australia, 7263,Tasmania,Australia, 7260,Tasmania,Australia, 7261,Tasmania,Australia, 7264,Tasmania,Australia, 7262,Tasmania,Australia, 7254,Tasmania,Australia, 7252,Tasmania,Australia, 7277,Tasmania,Australia, 7268,Tasmania,Australia, 7275,Tasmania,Australia, 7253,Tasmania,Australia, 7270,Tasmania,Australia, 7307,Tasmania,Australia, 7305,Tasmania,Australia, 7303,Tasmania,Australia, 7292,Tasmania,Australia, 7304,Tasmania,Australia, 7306,Tasmania,Australia, 7321,Tasmania,Australia, 7470,Tasmania,Australia, 7325,Tasmania,Australia, 7315,Tasmania,Australia, 7310,Tasmania,Australia, 7316,Tasmania,Australia, 7320,Tasmania,Australia, 7322,Tasmania,Australia, 7331,Tasmania,Australia, 7330,Tasmania,Australia, 7265,Tasmania,Australia, 2633,New South Wales,Australia, 7466,Tasmania,Australia, 7183,Tasmania,Australia, 7257,Tasmania,Australia, 7186,Tasmania,Australia, 7187,Tasmania,Australia, 7176,Tasmania,Australia, 7185,Tasmania,Australia, 2649,New South Wales,Australia, 7175,Tasmania,Australia, 3921,Victoria,Australia, 2623,New South Wales,Australia, 7119,Tasmania,Australia"

excludes = ["Western Australia", "South Australia", "New South Wales", "Northern Territory", "Tasmania", "Victoria", "Queensland", "Australian Capital Territory", "Australia"]

def convertElec(row):
	
# 	print(row['Geo_Targeting_Included'])
	if row['Geo_Targeting_Included'] == "Northern Territory":
	 	return ['Lingiari', 'Solomon']
	
	if row['Geo_Targeting_Included'] == "Australia":
		return ['All']

	else:
		row_str = row['Geo_Targeting_Included']
		results = []
		for word in excludes:
			row_str = row_str.replace(word, "")
		
		row_str = row_str.replace(" ", "")
		
		row_list = row_str.split(",")
		row_list = [i for i in row_list if i]
		temp_list = []
		for row_pc in row_list:
			if row_pc in postcodes:
				elec_list = postcodes[row_pc]
				for elec in elec_list:
					temp_list.append(elec)
			else:
				pass
		
		temp_df = pd.DataFrame(temp_list)
		if len(temp_df) > 0:
			electorates = temp_df.groupby(['electorate']).sum()
			target_electorates = electorates[(electorates['pop_pct'] >= 40)]
			result = list(target_electorates.index)
			return(result)
		else:
			return None
	
# print(convertElec(row))


def convertPostcodes(row):
	row_str = row['Geo_Targeting_Included']
	results = []
	for word in excludes:
		row_str = row_str.replace(word, "")
	row_str = row_str.replace(" ", "")
	
	row_list = row_str.split(",")
	row_list = [i for i in row_list if i]

	return list(set(row_list))

def convertStates(row):
	row_str = row['Geo_Targeting_Included']
	results = []
	for word in excludes:
		row_str = row_str.replace(word, "")
	row_str = row_str.replace(" ", "")
	
	row_list = row_str.split(",")
	row_list = [i for i in row_list if i]

	return list(set(row_list))