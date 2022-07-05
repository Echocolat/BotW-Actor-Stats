import oead
import os
import pathlib
import json
import dictdiffer

indexLetters = ['A-','B-','C-','D-','E-','F-','G-','H-','I-','J-']
indexNumbers = ['1','2','3','4','5','6','7','8']

seeEnemy = True
seeNameE = True
seeHealthE = False
seePowerE = False
seeAwarenessE = False
seeWeaknessesE = False

seeWeapon = True
seeNameW = True
seePowerW = False
seeHealthW = False
seeBonusesW = False
seeRangeBow = False
seeBowMisc = False

def openPack(filePath):
    data: bytes = pathlib.Path(filePath).read_bytes()
    data = oead.yaz0.decompress(data)
    sarc = oead.Sarc(data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    stats = {}
    if seeEnemy and 'Enemy' in filePath[7:].replace('.sbactorpack',''):
        if seeNameE and not 'Comparison' in filePath:
            stats['Actor Name'] = filePath[7:].replace('.sbactorpack','')
        elif seeNameE:
            stats['Actor Name'] = filePath[20:].replace('.sbactorpack','')
        #print(stats['Actor Name'])
        for file in sarc.get_files():
            sarc_writer.files[file.name] = file.data.tobytes()
            if ".bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if 'General' in dataFile.objects and seeHealthE:
                    stats['Health'] = dataFile.objects['General'].params['Life'].v
                if 'Enemy' in dataFile.objects and seePowerE:
                    stats['Attack power'] = dataFile.objects['Enemy'].params['Power'].v
            elif ".bdmgparam" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if seeWeaknessesE:
                    stats['Weaknesses'] = {}
                    stats['Weaknesses']['Ancient Arrow one shot'] = dataFile.lists['damage_param'].objects['Parameters'].params['VanishAffect'].v
                    stats['Weaknesses']['Fire'] = {}
                    stats['Weaknesses']['Ice'] = {}
                    stats['Weaknesses']['Elec'] = {}
                    stats['Weaknesses']['Urbosa'] = {}
                    stats['Weaknesses']['Thunder'] = {}
                    if dataFile.lists['damage_param'].objects['Parameters'].params['Burnable'].v:
                        stats['Weaknesses']['Fire']['Is affected'] = True
                        stats['Weaknesses']['Fire']['Time affected'] = dataFile.lists['damage_param'].objects['Parameters'].params['BurnTime'].v
                        stats['Weaknesses']['Fire']['Damage'] = dataFile.lists['damage_param'].objects['Parameters'].params['BurnDamage'].v
                        stats['Weaknesses']['Fire']['Fire one shot'] = dataFile.lists['damage_param'].objects['Parameters'].params['BurnCritical'].v
                    else:
                        stats['Weaknesses']['Fire']['Is affected'] = False
                    if dataFile.lists['damage_param'].objects['Parameters'].params['Iceable'].v:
                        stats['Weaknesses']['Ice']['Is affected'] = True
                        stats['Weaknesses']['Ice']['Time affected'] = dataFile.lists['damage_param'].objects['Parameters'].params['IceTime'].v
                        stats['Weaknesses']['Ice']['Damage'] = dataFile.lists['damage_param'].objects['Parameters'].params['IceDamage'].v
                        stats['Weaknesses']['Ice']['Ice one shot'] = dataFile.lists['damage_param'].objects['Parameters'].params['IceCritical'].v
                    else:
                        stats['Weaknesses']['Elec']['Is affected'] = False
                    if dataFile.lists['damage_param'].objects['Parameters'].params['Electricable'].v:
                        stats['Weaknesses']['Elec']['Is affected'] = True
                        stats['Weaknesses']['Elec']['Time affected'] = dataFile.lists['damage_param'].objects['Parameters'].params['ElectricTime'].v
                        stats['Weaknesses']['Elec']['Damage'] = dataFile.lists['damage_param'].objects['Parameters'].params['ElectricDamage'].v
                    else:
                        stats['Weaknesses']['Elec']['Is affected'] = False
                    if dataFile.lists['damage_param'].objects['Parameters'].params['GerudoHeroAffect'].v:
                        stats['Weaknesses']['Urbosa']['Is affected'] = True
                        stats['Weaknesses']['Urbosa']['Time affected'] = dataFile.lists['damage_param'].objects['Parameters'].params['GerudoHeroTime'].v
                        stats['Weaknesses']['Urbosa']['Damage'] = dataFile.lists['damage_param'].objects['Parameters'].params['GerudoHeroDamage'].v
                    else:
                        stats['Weaknesses']['Urbosa']['Is affected'] = False
                    if dataFile.lists['damage_param'].objects['Parameters'].params['LightningAffect'].v:
                        stats['Weaknesses']['Thunder']['Is affected'] = True
                        stats['Weaknesses']['Thunder']['Damage'] = dataFile.lists['damage_param'].objects['Parameters'].params['LightningDamage'].v
                    else:
                        stats['Weaknesses']['Thunder']['Is affected'] = False
            elif ".bawareness" in file.name and seeAwarenessE:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if 'Sight' in dataFile.objects:
                    stats['Awareness'] = {}
                    stats['Awareness']['Detected Cone'] = {}
                    stats['Awareness']['Suspicion Cone'] = {}
                    if 'sight_radius' in dataFile.objects['Sight'].params:
                        stats['Awareness']['Detected Cone']['Radius (m)'] = dataFile.objects['Sight'].params['sight_radius'].v
                    if 'sight_angle' in dataFile.objects['Sight'].params:
                        stats['Awareness']['Detected Cone']['Angle (rad)'] = dataFile.objects['Sight'].params['sight_angle'].v
                    if 'sight_alert_radius' in dataFile.objects['Sight'].params:
                        stats['Awareness']['Suspicion Cone']['Radius (m)'] = dataFile.objects['Sight'].params['sight_alert_radius'].v
                    if 'sight_alert_angle' in dataFile.objects['Sight'].params:
                        stats['Awareness']['Suspicion Cone']['Angle (rad)'] = dataFile.objects['Sight'].params['sight_alert_angle'].v
    elif seeWeapon and 'Weapon' in filePath[7:].replace('.sbactorpack',''):
        if seeNameW and not 'Comparison' in filePath:
            stats['Actor Name'] = filePath[7:].replace('.sbactorpack','')
        elif seeNameE:
            stats['Actor Name'] = filePath[20:].replace('.sbactorpack','')
        for file in sarc.get_files():
            sarc_writer.files[file.name] = file.data.tobytes()
            if ".bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if 'General' in dataFile.objects and seeHealthW:
                    stats['Health'] = dataFile.objects['General'].params['Life'].v
                if 'Attack' in dataFile.objects and seePowerW:
                    if dataFile.objects['Attack'].params['Power'].v != 0:
                        stats['Attack power'] = dataFile.objects['Attack'].params['Power'].v
                    if seeRangeBow and 'Bow' in filePath:
                        stats['Range'] = dataFile.objects['Attack'].params['Range'].v
                if 'WeaponCommon' in dataFile.objects and seeBonusesW:
                    if dataFile.objects['WeaponCommon'].params['GuardPower'].v != 0:
                        stats['Guard power'] = dataFile.objects['WeaponCommon'].params['GuardPower'].v
                    stats['Bonuses'] = {}
                    stats['Bonuses']['Attack up'] = {}
                    stats['Bonuses']['Durability up'] = {}
                    stats['Bonuses']['Guard up'] = {}
                    stats['Bonuses']['Has Crit bonus'] = dataFile.objects['WeaponCommon'].params['SharpWeaponAddCrit'].v
                    if dataFile.objects['WeaponCommon'].params['SharpWeaponAddAtkMin'].v == 0:
                        stats['Bonuses']['Attack up']['Has attack up bonus'] = False
                    else:
                        stats['Bonuses']['Attack up']['Has attack up bonus'] = True
                        stats['Bonuses']['Attack up']['Values of attack up'] = (dataFile.objects['WeaponCommon'].params['SharpWeaponAddAtkMin'].v,dataFile.objects['WeaponCommon'].params['SharpWeaponAddAtkMax'].v)
                        try:stats['Bonuses']['Attack up']['Values of attack up +'] = (dataFile.objects['WeaponCommon'].params['PoweredSharpAddAtkMin'].v,dataFile.objects['WeaponCommon'].params['PoweredSharpAddAtkMax'].v)
                        except:None 
                    if dataFile.objects['WeaponCommon'].params['SharpWeaponAddLifeMin'].v == 0:
                        stats['Bonuses']['Durability up']['Has durability up bonus'] = False
                    else:
                        stats['Bonuses']['Durability up']['Has durability up bonus'] = True
                        stats['Bonuses']['Durability up']['Values of durability up'] = (dataFile.objects['WeaponCommon'].params['SharpWeaponAddLifeMin'].v,dataFile.objects['WeaponCommon'].params['SharpWeaponAddLifeMax'].v)
                        try:stats['Bonuses']['Durability up']['Values of durability up +'] = (dataFile.objects['WeaponCommon'].params['PoweredWeaponAddLifeMin'].v,dataFile.objects['WeaponCommon'].params['PoweredWeaponAddLifeMax'].v)
                        except:None
                    if dataFile.objects['WeaponCommon'].params['SharpWeaponAddGuardMin'].v == 0:
                        stats['Bonuses']['Guard up']['Has guard up bonus'] = False
                    else:
                        stats['Bonuses']['Guard up']['Has guard up bonus'] = True
                        stats['Bonuses']['Guard up']['Values of Guard up'] = (dataFile.objects['WeaponCommon'].params['SharpWeaponAddGuardMin'].v,dataFile.objects['WeaponCommon'].params['SharpWeaponAddGuardMax'].v)
                        try:stats['Bonuses']['Guard up']['Values of Guard up +'] = (dataFile.objects['WeaponCommon'].params['PoweredSharpAddGuardMin'].v,dataFile.objects['WeaponCommon'].params['PoweredSharpAddGuardMax'].v)
                        except:None
                    if 'Bow' in filePath:
                        stats['Bonuses']['Can have x5 arrows'] = dataFile.objects['WeaponCommon'].params['PoweredSharpAddSpreadFire'].v
                        stats['Bonuses']['Can have rapid fire'] = dataFile.objects['WeaponCommon'].params['PoweredSharpAddZoomRapid'].v
                        if stats['Bonuses']['Can have rapid fire']:
                            stats['Bonuses']['Rapid fire values'] = (dataFile.objects['WeaponCommon'].params['PoweredSharpAddRapidFireMin'].v,dataFile.objects['WeaponCommon'].params['PoweredSharpAddRapidFireMax'].v)
                if 'Bow' in dataFile.objects and seeBowMisc:
                    stats['Bow Misc'] = {}
                    stats['Bow Misc']['Has multiple shot (spread)'] = dataFile.objects['Bow'].params['IsLeadShot'].v
                    if stats['Bow Misc']['Has multiple shot (spread)']:
                        stats['Bow Misc']['Number of arrows'] = dataFile.objects['Bow'].params['LeadShotNum'].v
                        stats['Bow Misc']['Angle between them'] = dataFile.objects['Bow'].params['LeadShotAng'].v
                    stats['Bow Misc']['Has multiple shot (line)'] = dataFile.objects['Bow'].params['IsRapidFire'].v
                    if stats['Bow Misc']['Has multiple shot (line)']:
                        stats['Bow Misc']['Number of arrows'] = dataFile.objects['Bow'].params['RapidFireNum'].v
                    stats['Bow Misc']['Arrow charge rate'] = dataFile.objects['Bow'].params['ArrowChargeRate'].v
                    stats['Bow Misc']['Arrow reload rate'] = dataFile.objects['Bow'].params['ArrowReloadRate'].v
    return stats
            
def basicStats():
    global seeEnemy
    seeEnemy = input('Do you want to see Enemies ? y if yes : ') == 'y'
    if seeEnemy:
        global seeHealthE
        seeHealthE = input('Do you want to see Health of the enemies ? y if yes : ') == 'y'
        global seePowerE
        seePowerE = input('Do you want to see Power of the enemies ? y if yes : ') == 'y'
        global seeAwarenessE
        seeAwarenessE = input('Do you want to see Awareness of the enemies ? y if yes : ') == 'y'
        global seeWeaknessesE
        seeWeaknessesE = input('Do you want to see Weaknesses of the enemies ? y if yes : ') == 'y'
    global seeWeapon
    seeWeapon = input('Do you want to see Weapons ? y if yes : ') == 'y'
    if seeWeapon:
        global seeHealthW
        seeHealthW = input('Do you want to see Health of the weapons ? y if yes : ') == 'y'
        global seePowerW
        seePowerW = input('Do you want to see Power of the weapons ? y if yes : ') == 'y'
        global seeBonusesW
        seeBonusesW = input('Do you want to see weapon bonuses ? y if yes : ') == 'y'
        global seeRangeBow
        seeRangeBow = input('Do you want to see the range of the bows ? y if yes : ') =='y'
        global seeBowMisc
        seeBowMisc = input('Do you want to see misc values for bows ? y if yes : ') == 'y'
    finalList = {}
    for filename in os.listdir('Actors'):
        if filename != '.gitkeep':
            onestats = openPack('Actors\\'+filename)
            finalList[onestats['Actor Name']] = onestats
    with open('stats.json','w') as f:
        f.write(json.dumps(finalList, indent = 4))

def comparison():
    global seeEnemy
    seeEnemy = input('Do you want to see Enemies ? y if yes : ') == 'y'
    if seeEnemy:
        global seeHealthE
        seeHealthE = input('Do you want to see Health of the enemies ? y if yes : ') == 'y'
        global seePowerE
        seePowerE = input('Do you want to see Power of the enemies ? y if yes : ') == 'y'
        global seeAwarenessE
        seeAwarenessE = input('Do you want to see Awareness of the enemies ? y if yes : ') == 'y'
        global seeWeaknessesE
        seeWeaknessesE = input('Do you want to see Weaknesses of the enemies ? y if yes : ') == 'y'
    global seeWeapon
    seeWeapon = input('Do you want to see Weapons ? y if yes : ') == 'y'
    if seeWeapon:
        global seeHealthW
        seeHealthW = input('Do you want to see Health of the weapons ? y if yes : ') == 'y'
        global seePowerW
        seePowerW = input('Do you want to see Power of the weapons ? y if yes : ') == 'y'
        global seeBonusesW
        seeBonusesW = input('Do you want to see weapon bonuses ? y if yes : ') == 'y'
        global seeRangeBow
        seeRangeBow = input('Do you want to see the range of the bows ? y if yes : ') =='y'
        global seeBowMisc
        seeBowMisc = input('Do you want to see misc values for bows ? y if yes : ') == 'y'
    finalList1 = {}
    finalList2 = {}
    finalList = {}
    for filename in os.listdir('Comparison\\Actors 1'):
        if filename != '.gitkeep':
            onestats1 = openPack('Comparison\\Actors 1\\'+filename)
            try:
                finalList1[onestats1['Actor Name']] = onestats1
            except:
                None
    for filename in os.listdir('Comparison\\Actors 2'):
        if filename != '.gitkeep':
            onestats2 = openPack('Comparison\\Actors 2\\'+filename)
            try:
                finalList2[onestats2['Actor Name']] = onestats2
            except:
                None
    for diff in list(dictdiffer.diff(finalList1,finalList2)):
        if diff[0] == 'add':
            for i in range(len(diff[2])):
                finalList[diff[2][i][0]] = f'found {diff[2][i][0]} in second folder and not in the first one'
        elif diff[0] == 'remove':
            for i in range(len(diff[2])):
                finalList[diff[2][i][0]] = f'found {diff[2][i][0]} in first folder and not in the second one'
        elif diff[0] == 'change':
            nameOfThing = diff[1].replace('.','/')
            finalList[nameOfThing] = f'found difference in {nameOfThing}. Value is {diff[2][0]} in first folder, and {diff[2][1]} in second folder.'
    with open('statsComparison.json','w') as f:
        f.write(json.dumps(finalList, indent = 4))

def main():
    if input('Do you want to make analysis of one Actor/Pack folder ? y for yes, anything else, else : ') == 'y':
        basicStats()
    if input('Do you want to compare two folders ? y for yes, anything else, else : ') =='y':
        comparison()

if __name__ == "__main__":
    main()