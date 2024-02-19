def swap(dict, c1, c2):
    for key, value in dict.items():
        if value == c1:
            k1 = key
            break 

    for key, value in dict.items():
        if value == c2:
            k2 = key
            break 

    dict[k2] = c1
    dict[k1] = c2


text = """
KVU HQBINKWALU DNBAURG BWO AU YUGHRCAUY ARCUPLO WG KVU RUWL DNBAURG ZVQGU
UTIRUGGCQDG WG W YUHCBWL WRU HWLHNLWALU AO PCDCKU BUWDG. WLKVQNJV KVU GNAEUHK
QP KVCG IWIUR CG QGKUDGCALO KVU HQBINKWALU DNBAURG. CK CG WLBQGK UFNWLLO
UWGO KQ YUPCDU WDY CDXUGKCJWKU HQBINKWALU PNDHKCQDG QP WD CDKUJRWL XWRCWALU
QR W RUWL QR HQBINKWALU XWRCWALU, HQBINKWALU IRUYCHWKUG, WDY GQ PQRKV. KVU
PNDYWBUDKWL IRQALUBG CDXQLXUY WRU, VQZUXUR, KVU GWBU CD UWHV HWGU, WDY C VWXU
HVQGUD KVU HQBINKWALU DNBAURG PQR UTILCHCK KRUWKBUDK WG CDXQLXCDJ KVU LUWGK
HNBARQNG KUHVDCFNU. C VQIU GVQRKLO KQ JCXU WD WHHQNDK QP KVU RULWKCQDG QP KVU
HQBINKWALU DNBAURG, PNDHKCQDG, WDY GQ PQRKV KQ QDU WDQKVUR. KVCG ZCLL CDHLNYU W
YUXULQIBUDK QP KVU KVUQRO QP PNDHKCQDG QP W RUWL XWRCWALU UTIRUGGUY CD KURBG
QP HQBINKWALU DNBAURG. WHHQRYCDJ KQ BO YUPCDCKCQD, W DNBAUR CG HQBINKWALU
CP CKG YUHCBWL HWD AU ZRCKKUD YQZD AO W BWHVCDU. C JCXU GQBU WRJNBUDKG ZCKV
KVU CDKUDKCQD QP GVQZCDJ KVWK KVU HQBINKWALU DNBAURG CDHLNYU WLL DNBAURG
ZVCHV HQNLY DWKNRWLLO AU RUJWRYUY WG HQBINKWALU. CD IWRKCHNLWR, C GVQZ KVWK
HURKWCD LWRJU HLWGGUG QP DNBAURG WRU HQBINKWALU. KVUO CDHLNYU, PQR CDGKWDHU,
KVU RUWL IWRKG QP WLL WLJUARWCH DNBAURG, KVU RUWL IWRKG QP KVU MURQG QP KVU
AUGGUL PNDHKCQDG, KVU DNBAURG IC, U, UKH. KVU HQBINKWALU DNBAURG YQ DQK,
VQZUXUR, CDHLNYU WLL YUPCDWALU DNBAURG, WDY WD UTWBILU CG JCXUD QP W YUPCDWALU
DNBAUR ZVCHV CG DQK HQBINKWALU. WLKVQNJV KVU HLWGG QP HQBINKWALU DNBAURG
CG GQ JRUWK, WDY CD BWDO ZWOG GCBCLWR KQ KVU HLWGG QP RUWL DNBAURG, CK CG
DUXURKVULUGG UDNBURWALU. C UTWBCDU HURKWCD WRJNBUDKG ZVCHV ZQNLY GUUB KQ IRQXU
KVU HQDKRWRO. AO KVU HQRRUHK WIILCHWKCQD QP QDU QP KVUGU WRJNBUDKG, HQDHLNGCQDG
WRU RUWHVUY ZVCHV WRU GNIURPCHCWLLO GCBCLWR KQ KVQGU QP JQYUL. KVUGU RUGNLKG
VWXU XWLNWALU WIILCHWKCQDG. CD IWRKCHNLWR, CK CG GVQZD KVWK KVU VCLAURKCWD
UDKGHVUCYNDJGIRQALUB HWD VWXU DQ GQLNKCQD.
"""

freq = {}
for i in "QWERTYUIOPASDFGHJKLZXCVBNM":
    freq[i] = 0

for c in text:
    if c == '\n' or c == ' ' or c == '.' or c ==',':
        continue
    freq[c] += 1

eng_freq = {
    'E' : 0.111607,
    'A' : 0.084966,
    'R' : 0.075809,
    'I' : 0.075448,
    'O' : 0.071635,
    'T' : 0.069509,
    'N' : 0.066544,
    'S' : 0.057531,
    'L' : 0.054893,
    'C' : 0.045338,
    'U' : 0.036308,
    'D' : 0.033844,
    'P' : 0.031671,
    'M' : 0.030129,
    'H'	: 0.030034,
    'G'	: 0.024705,
    'B' : 0.020720,
    'F'	: 0.018121,
    'Y'	: 0.017779,
    'W'	: 0.012899,
    'K'	: 0.011016,	
    'V'	: 0.010074,
    'X'	: 0.002902,	
    'Z'	: 0.002722,
    'J'	: 0.001965,	
    'Q'	: 0.001962
}

sorted_letters = sorted(freq, key=lambda k: freq[k])

sorted_eng_letters = sorted(eng_freq, key=lambda k: eng_freq[k])

subs = {}
for i in range(26):
    subs[sorted_letters[i]] = sorted_eng_letters[i]

decrypted = ""
for c in text:
    if c == '\n' or c == ' ' or c == '.' or c ==',':
        decrypted = decrypted + c
    else:
        decrypted = decrypted + subs[c]



#Ξεκινάει με RCE, πιθανόν να είναι THE

swap(subs, 'T', 'R')

swap(subs, 'H', 'C')

# #HAFE -> HAVE
swap(subs, 'V', 'F')

# #ALE -> ARE
swap(subs, 'R', 'L')

# #CACER -> PAPER
swap(subs, 'C', 'P')

# #THEORW -> THEORY
swap(subs, 'W', 'Y')

# #REAS->REAL
swap(subs, 'S', 'L')

# #PROMLECN -> PROBLEMS
swap(subs, 'M', 'B')

swap(subs, 'C', 'M')

swap(subs, 'N', 'S')

# #HOKEVER -> HOWEVER
swap(subs, 'K', 'W')

# #EAUH UASE -> EACH CASE
swap(subs, 'U', 'C')

# #COMPDTABLE -> COMPUTABLE
swap(subs, 'D', 'U')

# #IUMBERS -> NUMBERS
swap(subs, 'I', 'N')

# #BRIEGLY -> BRIEFLY
swap(subs, 'G', 'F')

# #EGPRESSIONS -> EXPRESSIONS
swap(subs, 'G', 'X')

# #ALTHOUKH -> ALTHOUGH 
swap(subs, 'K', 'G')

# #EKUALLY -> EQUALLY
swap(subs, 'K', 'Q')

decrypted = ""
for c in text:
    if c == '\n' or c == ' ' or c == '.' or c ==',':
        decrypted = decrypted + c
    else:
        decrypted = decrypted + subs[c]

print(decrypted)

print(subs)