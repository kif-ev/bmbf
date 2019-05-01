#!/usr/bin/env python3
from fdfgen import forge_fdf
import sh
from math import ceil
import csv
from operator import itemgetter
from pathlib import Path



######## Bitte hier Anpassen ##########################################
maßnahmenzeitraum = "09. - 13.05.18"
datum="09.05.18"
kif_ev= "Verein zur Förderung d. Konferenz d. deutschspr. Informatikfachschaften e.V."
maßname="46.0 Konferenz der deutschsprachtigen Informatikfachschaften"
csv_file_name="teilnehmer_innen.csv"
leer_blaetter=2
vorlage = "Vorlage_BMBF_Listen_2019.pdf"
datum_list = ["09.05.18","10.05.18","11.05.18","12.05.18","13.05.18",]


######## Nothing to change below here ##########################################

form_mapping = [("6","20","21"),("19","40","41"),("18","39","22"),
            ("17","42","23"),("16","43","24"),("15","44","25"),("14","45","26"),
            ("13","46","27"),("12","Text7","28"),("11","29","34"),("10","30","35"),
            ("9","31","36"),("8","32","37"),("7","33","38")]


def readcsv(csv_file_name):
    persons = []
    try:
        csvfile = open(csv_file_name,newline='')
    except FileNotFoundError:
        print("[X] File {} not found!".format(csv_file_name))
        exit(-1)
    else:
        with csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            persons = [{"Name":t[0],"Hochschule":t[1]} for t in reader if t[0] != "Name"]
            persons.sort(key=itemgetter("Hochschule","Name"))

    return persons


def generate_pdfs(persons, maßnahmenzeitraum, datum, kif_ev, maßname, leer_blaetter):
    seite = 1
    data_file="data_fdf.bin"
    output_file_name="output"
    personen_pro_seite = 14

    #check if vorlage exits
    test_file = Path(vorlage)
    if not test_file.is_file():
        print("[X] File {} not found!".format(vorlage))
        exit(-1)

    anzahl_seiten = ceil(len(persons)/personen_pro_seite)
    pdfs = []

    for j in range(anzahl_seiten+leer_blaetter):
        felder = []
        i=0
        for item in form_mapping:
            if personen_pro_seite*j+i < len(persons):
                felder.append((item[0],str(j*personen_pro_seite+i+1)))
                felder.append((item[1], persons[j*personen_pro_seite+i]["Name"]))
                felder.append((item[2], persons[j*personen_pro_seite+i]["Hochschule"]))
            i+=1

            if i == personen_pro_seite:
                output_file = output_file_name + str(seite) +".pdf"

                headers = [("1", seite), ("2", maßnahmenzeitraum), ("3", datum), ("4", kif_ev), ("5", maßname)]

                fields = felder + headers


                fdf = forge_fdf("",fields,[],[],[])
                fdf_file = open(data_file,"wb")
                fdf_file.write(fdf)
                fdf_file.close()

                sh.pdftk(vorlage,"fill_form", data_file,"output",output_file,"flatten")

                pdfs.append(output_file)

                seite+=1


    return pdfs



if __name__ == "__main__":
    person_list = readcsv(csv_file_name)
    for datum in datum_list:
        final_pdf_name = "teilnehmendenliste_{}.pdf".format(datum.replace(". ", "_"))
        output_files = generate_pdfs(person_list, maßnahmenzeitraum, datum, kif_ev, maßname, leer_blaetter)
        sh.pdftk(output_files, "cat","output",final_pdf_name )



