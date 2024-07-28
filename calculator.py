from pyluach import dates, hebrewcal
import os
import sys

class Period:
    def __init__(self, date, ona, haflaga=None):
        self.date = date
        self.ona = ona
        self.weekday = date.weekday()
        self.haflaga = haflaga
        self.seclusion_list = []

    @property
    def seclusion_list(self):
        return self._seclusion_list

    @seclusion_list.setter
    def seclusion_list(self, seclusion_list):
        self._seclusion_list = seclusion_list

    def add_seclusion(self, seclusion):
        self.seclusion_list.append(seclusion)

    @property
    def details(self):
        self._details = [self.ona, self.haflaga]
        return self._details

    @details.setter
    def details(self, haflaga):
        self._haflaga = haflaga


class Seclusion:
    def __init__(self, period, name, date, ona):
        self.period = period
        self.name = name
        self.date = date
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.weekday = date.weekday()
        self.ona = ona
        self.details = [self.name, self.ona, self.period.date.month]

    def get_details(self):
        return self.details

ona_dict = {0 : "ליל", 1 : "יום"}
weekday_dict = {
    1 : "ראשון",
    2 : "שני",
    3 : "שלישי",
    4 : "רביעי",
    5 : "חמישי",
    6 : "שישי",
    7 : "שבת"
}

def read_periods_list_file(file_path:str):
    #get txt from the dates file
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            date_list =  f.readlines()
        return date_list

def export_results(file_name, lines):
    
#export results in a file
    try:
        with open(file_name, "w") as f:
            f.writelines(lines)
    except NameError as err:
        print(err)

def convert_date_to_period(date_txt):
    #convert date text to period
    details = date_txt.split()
    if len(details) > 1:
        digits_of_date = [int(n) for n in details[0].split("/")]
        ona = int(details[1][0])
        if ona == 1 or ona == 0:
            period = Period(dates.HebrewDate(*digits_of_date[::-1]), ona)
        return period

def get_month_len(month:hebrewcal.Month):
    #get the length of the month
    date = dates.HebrewDate((month + 1).year, (month + 1).month, 1) - 1
    month_len = date.day
    return month_len

def get_seclusions(period, haflagot_list=None):
    #get list of seclusions from a period
    date = period.date
    year = date.year
    month = date.month
    day = date.day
    month_len = get_month_len(hebrewcal.Month(year, month))
    ona_beinonit30 = Seclusion(period, 'עונה בינונית 30', date + 29, period.ona)
    veset_hachodesh = Seclusion(period, 'וסת החודש', date + month_len, period.ona)
    ona_beinonit31 = Seclusion(period, 'עונה בינונית 31', date + 30, period.ona)
    seclusion_list = [ona_beinonit30, veset_hachodesh, ona_beinonit31]
    if period.haflaga:
        haflaga = Seclusion(period, 'הפלגה', date + period.haflaga - 1, period.ona)
        seclusion_list.append(haflaga)
    if haflagot_list:
        if len(haflagot_list) >= 2:
            haflagot_lechumra = []
            for h1 in haflagot_list[-1::-1]:
                akira = False
                for h2 in haflagot_list[-1:haflagot_list.index(h1):-1]:
                    if h2 > h1:
                        akira = True
                if not akira:
                    haf = Seclusion(period, str(h1), date + h1 - 1, period.ona)
                    haflagot_lechumra.append(haf)
            seclusion_list.append(haflagot_lechumra)
    
    if not period.ona:
        or_zarua = Seclusion(period, 'אור זרוע', ona_beinonit30.date - 1, period.ona + 1)
        kartyupleity = Seclusion(period, 'כרתי ופלתי', ona_beinonit30.date, period.ona + 1)
        seclusion_list.insert(0, or_zarua)
        seclusion_list.insert(2, kartyupleity)
    else:
        or_zarua = Seclusion(period, 'אור זרוע', ona_beinonit30.date, period.ona - 1)
        seclusion_list.insert(0, or_zarua)

    return seclusion_list

def main():

    # check args
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        json_file = sys.argv[1]
    else:
        print("Usage: python calculator.py <file>")
        sys.exit(1)

    #convert date to poriode
    period = convert_date_to_period(new_date, )

    periods_dates = {period.date: period for period in periods_list}
    
    #get the "haflagot" form periods
    seclusion_list = []
    for i, period in enumerate(periods_list[1:]):
        haflaga = period.date - periods_list[i].date + 1
        period.haflaga = int(haflaga)
    
    haflagot_list = [period.haflaga for period in periods_list[1:]]
    
    #get seclusions from periods
    for i, period in enumerate(periods_list):
        if haflagot_list:
            seclusion_list = get_seclusions(period, haflagot_list[:i])
        else:
            seclusion_list = get_seclusions(period)
        period.seclusion_list = seclusion_list
    
    #set results
    mid_line = "-" * 25
    lines = [f"רשימת הפלגות:\n{haflagot_list}\n{mid_line}\n"]

    for period in periods_dates:
        lines.append((f"{period.hebrew_date_string()} ב{ona_dict[periods_dates[period].ona]} {weekday_dict[period.weekday()]}:\n"))
        for seclusion in periods_dates[period].seclusion_list:
            if type(seclusion) != list:
                lines.append(f"  {seclusion.name} - {seclusion.date.hebrew_date_string()} ב{ona_dict[seclusion.ona]} {weekday_dict[seclusion.weekday]}\n")
            else:
                lines.append(("  הפלגות שלא נעקרו:\n"))
                for s in seclusion:
                    lines.append(f"    {s.name} - {s.date.hebrew_date_string()} ב{ona_dict[s.ona]} {weekday_dict[s.weekday]}\n")
        lines.append(mid_line + "\n")
    
    #export or print results
    if export_file:
        export_results(export_file, lines)
    else:
        print("")
        for line in lines:
            print(line[:-1])


if __name__ == "__main__":
    main()
