# -*- coding: utf-8 -*-
from ast import Sub
import math
import pandas as pd
import numpy as np
import codecs
import string
import json
from lxml.etree import Element, SubElement, Comment, ElementTree, tostring, indent

def LagrangeInterpol(x, y, xp):
    yp = 0
    for i in range(5):
        p = 1
        for j in range(5):
            if i != j:
                p = p * (xp - x[j])/(x[i] - x[j])
        
        yp = yp + p * y[i] 
    return yp

def LagrangeInterpolSpeed(xp):
    return LagrangeInterpol([5, 30, 50, 135, 160], [1, 3, 4, 6, 8], xp)

def LagrangeInterpolSize(xp):
    return LagrangeInterpol([0.2, 1, 5, 10, 14], [1.5, 2, 3.5, 5, 6], xp)

def GetCSVData(filePath):
    data = pd.read_csv(filePath, keep_default_na=False, encoding = "latin1")    
    return data

def main():  
    PokemonData = GetCSVData("Data/DataPokemon.csv")   
    useOldMove = True
    if(useOldMove == True):
        MoveData = GetCSVData("Data/DataMovesOld.csv")
    else:
        with open("Data/DataMoves.json", "r", encoding = "utf8") as f:
            MoveData = json.load(f)

    """Defining some lists containing data we iterate on, for evolutions and moves"""
 
    defNameList = list(PokemonData.DefName)

    with open("Data/forms.json", "r") as f:
        formsData = json.load(f)

    hasForm = list(formsData.keys())
    
    """Opening xml file where we write the Pokemon Defs"""
    #f = codecs.open("OutputFiles/Races_Pokemon.xml", "w", "utf-8")
    root = Element("Patch")

    findMod = SubElement(root, "Operation", {"Class": "PatchOperationFindMod"})
    mods = SubElement(findMod, "mods")
    ce = SubElement(mods, "li").text = "Combat Extended"
    poke = SubElement(mods, "li").text = "PokéWorld"
    operation = SubElement(findMod, "match", {"Class": "PatchOperationSequence"})
    operations = SubElement(operation, "operations")
    
    """Getting variables for patch values"""
    for i, pokemonDefName in enumerate(defNameList):
        #print(pokemonDefName)
        """Getting all data from csv file"""
        pokemonFullName = PokemonData.Name[i]        
        speedEV = PokemonData.SpeedEv[i]        
        statHealth = PokemonData.HP[i]
        statAtk = PokemonData.Attack[i]
        statDef = PokemonData.Defense[i]
        statAtkSpe = PokemonData.SpAttack[i]
        statDefSpe = PokemonData.SpDefense[i]
        statSpeed = PokemonData.Speed[i]  
        
        """We write everything for 1 Pokemon in the def file"""

        listOperation = SubElement(operations, "li", {"Class": "PatchOperationAdd"})

        xpath = SubElement(listOperation, "xpath").text = '/Defs/ThingDef[defName="PW_' + pokemonDefName + '"]/statBases'
        
        statBases = SubElement(listOperation, "value")
        SubElement(statBases, "MeleeDodgeChance").text = str(0.20)
        SubElement(statBases, "MeleeCritChance").text = str(0.10)
        SubElement(statBases, "MeleeParryChance").text = str(0.05)
        SubElement(statBases, "AimingAccuracy").text = str(0.75)
        SubElement(statBases, "ShootingAccuracyPawn").text = str(0.75)
        SubElement(statBases, "AimingDelayFactor").text = str(1)

       
    with open('OutputFiles/Patch_Races_Pokemon_CE.xml', 'wb') as f:
        indent(root, space = "  ")
        test = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(test)


if __name__ == "__main__":
    main()
