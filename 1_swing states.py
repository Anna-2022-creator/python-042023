import pandas
import numpy
import matplotlib.pyplot as plt

data = pandas.read_csv("1976-2020-president.csv")

# č.1
data = data[["year", "state", "party_simplified", "candidatevotes", "totalvotes"]]
data ["rank"] = data.groupby(["state", "year"])["candidatevotes"].rank(axis = 0, method = "min", ascending = False)

# č.2
data = data[data["rank"] == 1.0]
data.to_csv("winners.csv")

df = pandas.read_csv("winners.csv")


#č.3
df = df.sort_values(["state", "year" ], ascending=[True, True])
df["Winner Previous Year"] = df.groupby(["state"])["party_simplified"].shift(+1)



# č.4
df = df.dropna()
df ["change"] = numpy.where(df["party_simplified"] == df["Winner Previous Year"], 0, 1)
print(df.head(50))

# č.5 Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.
data_pivot = df.groupby(["state"])["change"].sum()
data_pivot = pandas.DataFrame(data_pivot)
data_pivot = data_pivot.sort_values("change", ascending=False)
data_pivot.to_csv("data_tab.csv")
print(data_pivot)


#č.6 Vytvoř sloupcový graf s 10 státy, kde došlo k nejčastější změně vítězné strany. Jako výšku sloupce nastav počet změn.
# Postup níže mi vytvoří histogram ze všech dat:
#data_tab = pandas.read_csv("data_tab.csv")
#data_tab = data_tab
#data_tab.hist()
#plt.legend(["state", "change"])
#plt.ylabel("change")
#plt.xlabel("state")
#plt.show()

data_tab = pandas.read_csv("data_tab.csv")
data_tab = data_tab.set_index("state")
data_tab = data_tab.iloc[:10]
data_tab.plot(color = "green", kind="bar", grid=True)
plt.legend(["state", "change"])
plt.ylabel("change")
plt.xlabel("state")
#plt.show()

# č.1B, pracuj s tabulkou se dvěma nejúspěšnějšími kandidáty pro každý rok a stát. 
# Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí.

data = pandas.read_csv("1976-2020-president.csv")
data = data[["year", "state", "party_simplified", "candidatevotes", "totalvotes"]]
data ["rank"] = data.groupby(["state", "year"])["candidatevotes"].rank(axis = 0, method = "min", ascending = False)

data = data[(data["rank"]==1.0) | (data["rank"]==2.0)]
print(data.head())
data.to_csv("1st+2nd.csv")

df = pandas.read_csv("1st+2nd.csv")
df ["candidatevotes_2"] = df.groupby(["state"])["candidatevotes"].shift(-1)

df["delta 1-2"] = df["candidatevotes"] - df["candidatevotes_2"]

df = df[df["rank"] == 1.0]



# č.2B Přidej sloupec s relativním marginem, tj. rozdílem vyděleným počtem hlasů. ( = delta/total)

df["margin"] = df["delta 1-2"] / df["totalvotes"]

#č.3B Seřaď tabulku podle velikosti relativního marginu a zjisti, kdy a ve kterém státě byl výsledek voleb nejtěsnější.

df = df.sort_values(["margin" ], ascending=[True])
print(df.head())


#č.4B Vytvoř pivot tabulku, která zobrazí pro jednotlivé volební roky, 
# kolik států přešlo od Republikánské strany k Demokratické straně, 
# kolik států přešlo od Demokratické strany k Republikánské straně a 
# kolik států volilo kandidáta stejné strany.

data_pivot_tab = pandas.read_csv("winners.csv")
data_pivot_tab = data_pivot_tab.sort_values(["state", "year"], ascending=[True, True])

data_pivot_tab ["previous party"] = data_pivot_tab.groupby(["state"])["party_simplified"].shift(+1)

data_pivot_tab = data_pivot_tab.dropna()

data_pivot_tab ["swing"] = numpy.where((data_pivot_tab["party_simplified"] == "DEMOCRAT")  & (data_pivot_tab["previous party"] == "REPUBLICAN") , "to DEM", "NO swing")
data_pivot_tab["swing"] = numpy.where((data_pivot_tab["party_simplified"] == "REPUBLICAN") & (data_pivot_tab["previous party"] == "DEMOCRAT"), "to REP",  data_pivot_tab["swing"])


data_pivot_tab.to_csv("data_pivot_tab.csv")

data = pandas.read_csv("data_pivot_tab.csv")

overview_pivot = pandas.pivot_table(data=data_pivot_tab, values="state", index="year", columns="swing", aggfunc=len)

print(overview_pivot)

