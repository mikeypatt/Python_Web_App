import Database as Db
import numpy as np
import os

def test_database_connects_when_instructed():
    database = Db.Connection()
    database.connect()
    assert database.connected() == True


def test_database_details_are_correct():
    database = Db.Connection()
    assert database.user() == 'bjp19'
    assert database.database() == 'bjp19'
    assert database.host() == 'cloud-vm-42-77.doc.ic.ac.uk'


def test_database_is_disconnected():
    database = Db.Connection()
    database.connect()
    database.disconnect()
    assert database.connected() == False


def test_lsoa_code_query_returns_correct_data():
    database = Db.Connection()
    database.connect()

    lsoa_query = "select distinct lsoa_code from crime_data where lsoa_code IS NOT NULL order by lsoa_code asc"
    database.cursor.execute(lsoa_query)
    lsoa_codes = np.array(database.cursor.fetchall())
    lsoa_codes = np.concatenate(lsoa_codes)

    # Get actual data from prepared source
    fname = os.path.join(os.path.dirname(__file__), "testData/lsoa_query_results.csv")
    lsoa_actuals = np.genfromtxt(fname,delimiter=",", dtype='<U11' ,skip_header=True)
    lsoa_actuals = np.core.defchararray.replace(lsoa_actuals, '"', '')

    assert len(lsoa_actuals) == len(lsoa_codes)
    comparison = lsoa_codes == lsoa_actuals
    assert comparison.all()


def test_1_month_summary_stats_are_correct_for_may19():
    database = Db.Connection()
    database.connect()

    query = "select lsoa_code from crime_data where lsoa_code IS NOT NULL and date = '2019-05'"
    database.cursor.execute(query)
    may_codes = np.array(database.cursor.fetchall())
    may_codes = np.concatenate(may_codes)

    fname = os.path.join(os.path.dirname(__file__), "testData/may_19_results.csv")
    may_actuals = np.genfromtxt(fname, delimiter=",", dtype='<U11', skip_header=True)
    may_actuals = np.core.defchararray.replace(may_actuals, '"', '')

    assert len(may_actuals) == len(may_codes)
    comparison = may_codes == may_actuals
    assert comparison.all()
