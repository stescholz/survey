from survey.question import *

directory = "Scans"
csv_fn = "results.csv"


# old headline coordinates: header = (575, 260, 1145, 330)
header = (230, 330, 1510, 470)
off_x = 0
off_y = -4

lower = 120
upper = 210

questions = [
    YesNoQuestion("Erstsemester", [(996, 498), (1081, 498)]),
    Question("Mathematikkurs", ["Leistungskurs", "Grundkurs"],
             [(996, 546), (1223, 546)]),
    YesNoQuestion("CAS", [(996, 595), (1081, 595)]),
    Question("Vorbereitung", ["Brueckenkurs", "Einfuehrungskurs", "sonstige"],
             [(995, 642), (995, 691), (995, 739)], True),
    YesNoQuestion("Aussagenlogik", [(1312, 837), (1397, 837)]),
    YesNoQuestion("Mengenoperationen", [(1310, 915), (1395, 915)]),
    YesNoQuestion("Beweise", [(1310, 963), (1395, 963)]),
    YesNoQuestion("Induktion", [(1310, 1011), (1395, 1011)]),
    YesNoQuestion("komplexe Zahlen", [(1310, 1060), (1395, 1060)]),
    YesNoQuestion("Zahlenfolgen", [(1310, 1108), (1395, 1108)]),
    YesNoQuestion("Grenzwerte", [(1310, 1156), (1395, 1156)]),
    YesNoQuestion("Reihen", [(1310, 1204), (1395, 1204)]),
    YesNoQuestion("Stetigkeit", [(1017, 1290), (1104, 1290)]),
    Question("Definition Stetigkeit", ["Grenzwert", "EpsDelta"],
             [(1017, 1338), (1282, 1337)], True),
    YesNoQuestion("Zwischenwertsatz", [(1017, 1392), (1102, 1392)]),
    YesNoQuestion("Differenzenquotient", [(1017, 1440), (1102, 1440)]),
    Question("Differentiationsregeln",
             ["Produktregel", "Quotientenregel", "Kettenregel"],
             [(1016, 1489), (1225, 1489), (1016, 1537)], True),
    YesNoQuestion("Integral", [(1016, 1584), (1101, 1584)]),
    Question("Integrationstechniken",
             ["Substitution", "partielle Integration"],
             [(1015, 1633), (1215, 1633)], True),
    YesNoQuestion("Exponentialfunktion", [(1014, 1682), (1099, 1682)]),
    YesNoQuestion("Logarithmengesetze", [(1014, 1730), (1099, 1730)]),
    YesNoQuestion("Winkelfunktionen", [(1014, 1778), (1099, 1778)]),
    YesNoQuestion("Tangens und Arkustangens", [(1013, 1826), (1098, 1825)]),
    YesNoQuestion("Matrix", [(1301, 1941), (1386, 1941)]),
    YesNoQuestion("lineare Gleichungssyteme", [(1301, 1988), (1386, 1988)]),
    YesNoQuestion("Vektorrechnung", [(1301, 2038), (1386, 2038)])
    ]
