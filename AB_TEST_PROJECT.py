#################################################
#           AB TESTİNG PROJECT                  #
#################################################
#<<<Şule AKÇAY >>>


#kütüphaneleri ekledim

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
from scipy.stats import shapiro
from scipy import stats

#veri seti içeriği
#~Impression->İzlenme sayısı
#~Click -> Tıklanma sayısı
#~Purchase -> Satın alma fiyati
#~Earning ->Kazanç

#eklentiler eklendi
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

#veri seti çekme işlemi
data = pd.read_excel(r"C:\Users\Suleakcay\PycharmProjects\pythonProject6\datasets\ab_testing_data.xlsx" ,sheet_name="Control Group")
data1 = pd.read_excel(r"C:\Users\Suleakcay\PycharmProjects\pythonProject6\datasets\ab_testing_data.xlsx" ,sheet_name="Test Group")


#veri setini detaylı incelemeye çalıştım

df_testing = data.copy()
df_control = data1.copy()

df_testing.head()
df_control.head()

df_testing.columns

df_testing.describe().T #4 değişkende float değerinde
df_testing.index #40 adet değişken var
df_testing.isnull().values.any() #boş değer yok

df_testing["Purchase"].describe().T
df_control["Purchase"].describe().T

df_testing.shape
df_control.shape


#1 Aydır devam eden AB testinin sonuçlarını analiz etmek istiyoruz
#Bu nedenle, istatitiksel testler için purchase metriğine odaklanacağız.

#Confidence Interval
sms.DescrStatsW(df_testing["Purchase"]).tconfint_mean()
sms.DescrStatsW(df_control["Purchase"]).tconfint_mean()
#test güven aralığı ortalaması (508.0041754264924, 593.7839421139709)
#control güven aralığı ortalaması 530.5670226990062, 633.6451705979289

#VARSAYIM KONTROLÜ
#1.1 Normallik Varsayımı
#1.2 Varyans Homejenliği

############################
# 1.1 Normallik Varsayımı
############################
#!Normallik varsayım testi için shapiro testi kullanılabilir
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.


test_istatistigi, pvalue = shapiro(df_testing["Purchase"])
print('Test İstatistiği = %.2f, p-değeri = %.2f' % (test_istatistigi, pvalue))
#Test İstatistiği = 0.97, p-değeri = 0.58


test_istatistigi, pvalue = shapiro(df_control["Purchase"])
print('Test İstatistiği = %.2f, p-değeri = %.2f' % (test_istatistigi, pvalue))
#Test İstatistiği = 0.96, p-değeri = 0.15

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
#test grubu için normallik varsayımı sağlanır p < 0.05 değil
#control grubu için normallik varsayımı sağlanır   p < 0.05 değil
#İkiside sağlanıyor.

############################
# 1.2 Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

statistic, pvalue = stats.levene(df_testing["Purchase"], df_control["Purchase"])
print('Test İstatistiği = %.2f, p-değeri = %.2f' % (statistic, pvalue))

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# Varyanslar homojen değerdedir.

############################
# 2. Hipotezin Uygulanması
############################

test_istatistigi, pvalue = stats.ttest_ind(df_testing["Purchase"], df_control["Purchase"],
                                          equal_var=True)
print('Test İstatistiği = %.2f, p-değeri = %.2f' % (test_istatistigi, pvalue))
#Test İstatistiği = -0.94, p-değeri = 0.35

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# 1.2 Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
test_istatistigi, pvalue = stats.mannwhitneyu(df_testing["Purchase"], df_control["Purchase"])
print('Test İstatistiği = %.2f, p-değeri = %.2f' % (test_istatistigi, pvalue))
# Test İstatistiği = 723.00, p-değeri = 0.23

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
#H0 reddedilmez.



