# Risk scoring module

def calculate_risk(row):
    """
    Example risk function:
    Risk = Clicks * 2 + DepartmentRisk + PreviousIncidents
    """
    return row["Clicks"]*2 + row["DepartmentRisk"] + row["PreviousIncidents"]