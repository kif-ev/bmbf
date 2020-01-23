use_db = False;
#### simple Usage ####
measures_period = "09. - 13.05.18"
date="09.05.18"
organization= "Initiative solidarische Welt Ilmenau e.V."
measure= "International Studentweek Ilmenau"
csv_file_name="teilnehmer_innen.csv"
empty_sheets=2
template = "Vorlage_BMBF_Listen_2019.pdf"
list_dates = ["09.05.18","10.05.18","11.05.18","12.05.18","13.05.18"]
debug = False
#### Database ####
db_host = "localhost"
db_port = "3306"
db_scheme = "bmbf_formular"
db_prefix = "bmbf_"
db_user = "root"
db_password = ""
#### NetworkAdress ####
dns = "Your Domain"

#### DO NOT CHANGE ####
if __name__ == "__main__":
    exit(1)