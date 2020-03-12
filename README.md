# Grundlegendes

Dieses kleine Skript erzeugt vorausgefüllte BMBF-Listen für den Nachweis der Teilnehmenden. 
Es benötigt Python3, einige zusätzliche Module (s. requirements.txt) und pdftk, sowie die PDF-Vorlage mit Formularfeldern vom BMBF. 
Dokumenatation der Web-API befindet sich im Unterordner "Dokumentation", Beispiele für JSON-Requests an die Web-API sind im Ordner "json-examples" zu finden.
Die Scripte zum initialisieren der Datenbank sind im Ordner "db".
Es ist nur unter Linux getestet und bedarf vermutlich einiger Anpassung, damit es unter Windows läuft (von Mac OS hab ich keine Ahnung :P ).

Fragen und Anmerkungen gerne an kif@matedealer.de .
Fragen zur Web-API gerne an martin@konfuzzyus.de .


**Ich übernehme keine Haftung für die Benutzung des Skriptes und ich habe bei der Erstellung des Skriptes nicht mit dem BMBF zusammen gearbeitet.**

# Installation

1.  Python3 installieren
2.  MariaDB oder MySQL installieren, eine Datenbank anlegen und in dieser das Script `db/createDB.sql` ausführen um die benötigten Tabellen an zu legen
3.  Benötigte module aus der Requirementsdatei mit `pip3 -r requirements.txt` installieren
4.  config-sample.py in config.py kopieren mittels `cp config-sample.py config.py`
5.  Konfigurationsdatei mit entsprechenden Werten wie in der Anleitung beschrieben mittels `nano config.py` ausfüllen
6.  Programm mittels `python3 webstart.py` für die Web-Api starten oder mit `python3 bmbf_main.py` die lokale Variante ausführen (Input kann zwischen DB und Datei umgeschaltet werden in der Konfigurationsdatei)
