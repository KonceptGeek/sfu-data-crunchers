__author__ = 'Jasneet Sabharwal <jsabharw@sfu.ca>'
import json
import copy
from collections import defaultdict


def mergeRentTuition(rentFilePath, tuitionFilePath, outputPath):
    with open(rentFilePath) as rentFile, open(tuitionFilePath) as tuitionFile:
        rentData = json.load(rentFile)
        tuitionData = json.load(tuitionFile)
    tuitionData = cleanTuition(tuitionData)
    rentData = cleanRentData(rentData)

    finalData = []
    for i in tuitionData:
        city = i['city']
        province = i['province']
        if city in ['Surrey', 'New Westminster', 'North Vancouver', 'Burnaby'] and province == 'British Columbia':
            city = 'Vancouver'
        if city in ['Kitchener', 'Waterloo'] and province == 'Ontario':
            city = 'Kitchener-Cambridge-Waterloo'
        if city in ['Ottawa', 'Gatineau'] and province in ['Ontario', 'Quebec']:
            city = 'Ottawa-Gatineau'
            province = 'Quebec'
        if 'Trois-Rivi' in city and province == 'Quebec':
            city = 'Trois-Rivieres'
        if city == 'The Pas and Thompson' and province == 'Manitoba':
            city = 'Thompson'

        key = province+'||'+city
        if key in rentData:
            rentInfo = rentData[key]
            avgRent = rentInfo['avgRent']
            rezFee = i['rezFee']
        else:
            avgRent = 0
            rezFee = i['rezFee']
        rezFee = rezFee/8
        i['areaRent'] = avgRent
        i['rezFee'] = rezFee
        if rezFee > 0 and avgRent > 0:
            avgRent = (avgRent+rezFee)/2
        if avgRent == 0 and rezFee > 0:
            avgRent = rezFee
        i['avgRent'] = avgRent
        finalData.append(i)

    finalDataStr = json.dumps(finalData)
    with open(outputPath, 'w') as outFile:
        outFile.write(finalDataStr+'\n')




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

    resultDict = {}
    for i in result:
        province = i['province']
        city = i['city']
        if city == 'Abbotsford-Mission':
            city = 'Abbotsford'
            i['city'] = 'Abbotsford'
        if 'Montr' in city and 'Quebec' in province:
            city = 'Montreal'
            i['city'] = 'Montreal'
        if 'bec' in city and 'Quebec' in province:
            city = 'Quebec City'
            i['city'] = 'Quebec City'
        if 'Trois-Rivi' in city and 'Quebec' in province:
            city = 'Trois-Rivieres'
            i['city'] = 'Trois-Rivieres'
        if city == 'Greater Sudbury' and province == 'Ontario':
            city = 'Sudbury'
        if city == 'St. Catharines-Niagara' and province == 'Ontario':
            city = 'St. Catharines'

        resultDict[province+'||'+city] = i


    return resultDict

def cleanTuition(tuitionData):
    result = []
    for i in tuitionData:
        record = {}
        record['city'] = i['City'].strip()
        record['institution'] = i['Institution name'].strip()
        record['province'] = i['Province'].strip()
        try:
            extraFees = int(i['Fees - Total'])
        except:
            extraFees = 0
        try:
            record['rezFee'] = int(i['Residence - Room only'])
        except:
            record['rezFee'] = 0
        for key, val in i.iteritems():
            if 'Tuition -' in key:
                recordCopy = copy.deepcopy(record)
                program = key.split('Tuition -')[1].strip()
                try:
                    programFees = int(val)
                except:
                    continue
                recordCopy['programFees'] = programFees+extraFees
                recordCopy['program'] = program
                result.append(recordCopy)
    print len(result)
    return result




if __name__ == '__main__':
    mergeRentTuition('/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/rent.json',
                     '/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/undergrad2014canada.json',
                     '/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/cleanData.json')