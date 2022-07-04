import oead
import os
import pathlib
import json

indexLetters = ['A-','B-','C-','D-','E-','F-','G-','H-','I-','J-']
indexNumbers = ['1','2','3','4','5','6','7','8']

seeName = True
seeHealth = False
seePower = False
seeAwareness = False
seeWeaknesses = False

def openPack(filePath):
    data: bytes = pathlib.Path(filePath).read_bytes()
    data = oead.yaz0.decompress(data)
    sarc = oead.Sarc(data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    stats = {}
    if seeName:
        stats['Actor Name'] = filePath[7:].replace('.sbactorpack','')
    #print(stats['Actor Name'])
    for file in sarc.get_files():
        sarc_writer.files[file.name] = file.data.tobytes()
        if ".bgparamlist" in file.name:
            dataFile: bytes = file.data
            dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
            if 'General' in dataFile.objects and seeHealth:
                stats['Health'] = dataFile.objects['General'].params['Life'].v
            if 'Enemy' in dataFile.objects and seePower:
                stats['Attack power'] = dataFile.objects['Enemy'].params['Power'].v
        elif ".bdmgparam" in file.name:
            dataFile: bytes = file.data
            dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
            if seeWeaknesses:
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
        elif ".bawareness" in file.name and seeAwareness:
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
    return stats
            
def basicStats():
    global seeHealth
    seeHealth = input('Do you want to see Health of the enemies ? y if yes : ') == 'y'
    global seePower
    seePower = input('Do you want to see Power of the enemies ? y if yes : ') == 'y'
    global seeAwareness
    seeAwareness = input('Do you want to see Awareness of the enemies ? y if yes : ') == 'y'
    global seeWeaknesses
    seeWeaknesses = input('Do you want to see Weaknesses of the enemies ? y if yes : ') == 'y'
    finalList = []
    for filename in os.listdir('Actors'):
        if filename != '.gitkeep':
            onestats = openPack('Actors\\'+filename)
            finalList.append(onestats)
    with open('stats.json','w') as f:
        f.write(json.dumps(finalList, indent = 4))

def main():
    basicStats()

if __name__ == "__main__":
    main()