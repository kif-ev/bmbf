#!/usr/bin/env python3
from fdfgen import forge_fdf
import sh
from math import ceil
import csv
from operator import itemgetter
from pathlib import Path
import os
import config
from pprint import pprint
import databaseConnect as db
import helper

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
    if(config.debug):
        pprint(persons)
    return persons



def generate_pdfs(persons, massnahmenzeitraum, datum, kif_ev, massname, leer_blaetter, template):
    seite = 1
    data_file="data_fdf.bin"
    output_file_name="output"
    personen_pro_seite = 14

    #check if vorlage exits
    test_file = Path(template)
    if not test_file.is_file():
        print("[X] File {} not found!".format(template))
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

                headers = [("1", seite), ("2", massnahmenzeitraum), ("3", datum), ("4", kif_ev), ("5", massname)]

                fields = felder + headers


                fdf = forge_fdf("",fields,[],[],[])
                fdf_file = open(data_file,"wb")
                fdf_file.write(fdf)
                fdf_file.close()

                sh.pdftk(template,"fill_form", data_file,"output",output_file,"flatten")

                pdfs.append(output_file)
                if (config.debug):
                    pprint("File " + str(output_file) + " created.")
                seite+=1
    return pdfs

def generate_pdfsDB(persons, massnahmenzeitraum, datum, kif_ev, massname, leer_blaetter, template, page):
    seite = page
    data_file="data_fdf.bin"
    output_file_name="output"
    personen_pro_seite = 14

    #check if vorlage exits
    test_file = Path(template)
    if not test_file.is_file():
        print("[X] File {} not found!".format(template))
        exit(-1)

    anzahl_seiten = ceil(len(persons)/personen_pro_seite)
    pdfs = []

    for j in range(anzahl_seiten+leer_blaetter):
        felder = []
        i=0
        for item in form_mapping:
            if personen_pro_seite*j+i < len(persons):
                felder.append((item[0], persons[j*personen_pro_seite+i]["id"]))
                felder.append((item[1], persons[j*personen_pro_seite+i]["Name"]))
                felder.append((item[2], persons[j*personen_pro_seite+i]["Hochschule"]))
            i+=1

            if i == personen_pro_seite:
                output_file = output_file_name + str(seite) +".pdf"

                headers = [("1", seite), ("2", massnahmenzeitraum), ("3", datum), ("4", kif_ev), ("5", massname)]

                fields = felder + headers


                fdf = forge_fdf("",fields,[],[],[])
                fdf_file = open(data_file,"wb")
                fdf_file.write(fdf)
                fdf_file.close()

                sh.pdftk(template, "fill_form", data_file, "output", output_file, "flatten")

                pdfs.append(output_file)
                if (config.debug):
                    pprint("File " + str(output_file) + " created.")
                seite+=1
    return {'filename': pdfs, 'page': seite}

def mainFiles():
    if (config.debug):
        pprint("FILE-Start")
    person_list = readcsv(config.csv_file_name)
    if (config.debug):
        pprint(person_list)
    output_files_ges = []
    for datum in config.list_dates:
        final_pdf_name = "teilnehmendenliste_{}.pdf".format(datum.replace(".", "_"))
        output_files = generate_pdfs(person_list, config.measures_period, config.date, config.organization, config.measure, config.empty_sheets, config.template)
        sh.pdftk(output_files, "cat","output",final_pdf_name )
        output_files_ges.append(final_pdf_name)
        if (config.debug):
            pprint("File " + str(final_pdf_name) + " created.")
        helper.GarbageCollect(output_files)
    sh.pdftk(output_files_ges, "cat", "output", config.measure + ".pdf")
    for file in output_files_ges:
        os.remove(file)
    os.remove("output1.pdf")
    os.remove("output2.pdf")
    os.remove("output3.pdf")
    os.remove("data_fdf.bin")
    if (config.debug):
        print ("finished")
    return

def mainDB(id):
    if (config.debug):
        pprint("DB-Start: " + str(id))
    if (db.checkGrp(id)):
        event = db.ReadEventWG(id)
        if config.debug:
            pprint("Event has Group")
    else:
        event = db.ReadEventWOG(id)
        if config.debug:
            pprint("Event has not Group")
    if (config.debug):
        pprint(event)
        pprint("try renumber")
    event = helper.RenumberPersons(event)
    if (config.debug):
        pprint("renumbered Persons:")
        pprint(event)
    page = 1
    output_files_ges = []
    if event['type'] == 'p':
        person_list = helper.assimilatePersons(event['persons'])
        for datum in event['days']:
            if (config.debug):
                pprint(datum)
            final_pdf_name = "teilnehmendenliste_" + str(event['id']) + "_{}.pdf".format(datum.replace(".", "_"))
            output_files = generate_pdfsDB(person_list, event['measure_periode'], datum, event['organization'], event['measure'], config.empty_sheets, event['template']['filename'], page)
            sh.pdftk(output_files['filename'], "cat", "output", final_pdf_name )
            helper.GarbageCollect(output_files['filename'])
            output_files_ges.append(final_pdf_name)
            if (config.debug):
                pprint("File " + str(final_pdf_name) + " created.")
    elif event['type'] == 'g':
        for datum in event['days']:
            if config.debug:
                pprint(event['groups'].keys())
            for x in event['groups'].keys():
                person_list = helper.assimilatePersons(event['groups'][str(x)])
                if (config.debug):
                    pprint(datum)
                    pprint("X in MainDB" + str(x))
                final_pdf_name = "teilnehmendenliste_" + str(event['id']) + "_g_" + str(x) + "_{}.pdf".format(datum.replace(".", "_"))
                output_files = generate_pdfsDB(person_list, event['measure_periode'], datum, event['organization'],
                                               event['measure'], config.empty_sheets, event['template']['filename'], page)
                page = output_files['page']
                sh.pdftk(output_files['filename'], "cat", "output", final_pdf_name)
                helper.GarbageCollect(output_files['filename'])
                output_files_ges.append(final_pdf_name)
                if (config.debug):
                    pprint("File " + str(final_pdf_name) + " created.")
                    pprint(output_files_ges)
    final_pdf_name_complete = "Event_" + str(id) + ".pdf"
    sh.pdftk(output_files_ges, "cat", "output", final_pdf_name_complete)
    output_files_ges.append("data_fdf.bin")
    helper.GarbageCollect(output_files_ges)
    if (config.debug):
        print ("finished")
    return final_pdf_name_complete

if __name__ == "__main__":
    exit(1)



