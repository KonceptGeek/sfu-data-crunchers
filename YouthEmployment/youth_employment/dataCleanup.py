__author__ = 'Jasneet Sabharwal <jsabharw@sfu.ca>'
import json
from collections import defaultdict


def mergeRentTuition(rentFilePath, tuitionFilePath, feesFilePath):
    with open(rentFilePath) as rentFile, open(tuitionFilePath) as tuitionFile, open(feesFilePath) as feesFile:
        rentData = json.load(rentFile)
        tuitionData = json.load(tuitionFile)
        feesData = json.load(feesFile)

    tuitionData = cleanTuitionData(tuitionData)
    rentData = cleanRentData(rentData)
    feesData = cleanFees(feesData)

    tuitionData = mergeTuitionFees(tuitionData, feesData)


def cleanRentData(rentData):
    result = []
    mergingDict = defaultdict(list)

    for i in rentData:
        if i['UNIT'] == 'Two bedroom units' or i['UNIT'] == 'Three bedroom units' or i['Ref_Date'] != int(2014):
            continue
        try:
            i['Value'] = float(i['Value'])
        except:
            continue

        province = i['GEO'].split(',')[1].strip()
        city = i['GEO'].split(',')[0].strip()

        if province == "Yukon":
            province = "Yukon Territory"

        if province == 'Newfoundland and Labrador':
            province = 'Newfoundland  & Labrador'

        if ' part' in province.lower():
            splits = province.split(' ')
            splits = splits[:-1]
            province = ' '.join(splits)

        i['province'] = province
        i['city'] = city
        i['year'] = i['Ref_Date']

        i.pop('UNIT', None)
        i.pop('GEO', None)
        i.pop('Ref_Date', None)

        mergingDict[city+'||'+province].append(i)

    for key, value in mergingDict.iteritems():
        resultToAppend = value[0]
        sumRent = 0
        count = 0
        for v in value:
            sumRent += v['Value']
            count += 1
        avgRent = sumRent/count
        resultToAppend['avgRent'] = avgRent
        resultToAppend.pop('Value', None)
        result.append(resultToAppend)

    return result


def cleanTuitionData(tuitionData):
    result = []
    for i in tuitionData:
        if i['Province'] == 'NL':
            i['Province'] = 'Newfoundland  & Labrador'
        if i['Province'] == 'PEI':
            i['Province'] = 'Prince Edward Island'
        if i['Province'] == 'NS':
            i['Province'] = 'Nova Scotia'
        if i['Province'] == 'NB':
            i['Province'] = 'New Brunswick'
        try:
            if int(i['Upper']):
                i['Upper'] = int(i['Upper'])
                i.pop('Lower', None)
        except:
            try:
                if int(i['Lower']):
                    i['Upper'] = int(i['Lower'])
                    i.pop('Lower', None)
            except:
                continue

        if i['Citizenship'] != 'Foreign' and i['Level'] != 'Graduate':
            i.pop('Citizenship', None)
            result.append(i)
    return result


def cleanFees(feesData):
    result = {}
    for i in feesData:
        if i['Citizenship'] != 'Canadian':
            continue
        if i['Level'] != 'Undergraduate':
            continue
        try:
            if int(i['Total']):
                i['Total'] = int(i['Total'])
        except:
            continue

        result[i['Institution name']] = i
    return result


def mergeTuitionFees(tuitionData, feesData):
    result = []
    for i in tuitionData:
        name = i['Institution name']
        fees = feesData[name]
        i['TotalFees'] = i['Upper'] + fees['Total']
        i.pop('Upper', None)
        result.append(i)
    print result



if __name__ == '__main__':
    mergeRentTuition('/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/rent.json',
                     '/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/tuition.json',
                     '/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/fees.json')