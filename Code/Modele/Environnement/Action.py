from enum import Enum

class Action(Enum):
    Left = 0,
    Right = 1,
    Up = 2,
    Down = 3

## Transforme un entier en string qui correspond a l'action choisie ##
def int2Action2String(integer):
    if(integer == 0) : return "LEFT"
    if(integer == 1) : return "RIGHT"
    if(integer == 2) : return "UP"
    if(integer == 3) : return "DOWN"
    print("ERREUR DE CONVERSION : int2Action2String → EXIT")
    exit(0)

## Transforme un entier en String de 1 charactere qui denote l'action choisie ##
def int2Action2String1Char(integer):
    if(integer == 0) : return "L"
    if(integer == 1) : return "R"
    if(integer == 2) : return "U"
    if(integer == 3) : return "D"
    print("ERREUR DE CONVERSION : int2Action2String1Char → EXIT")
    exit(0)

## Transforme un entier en l'action correspondante ##
def int2Action(integer):
    if(integer == 0) : return Action.Left
    if(integer == 1) : return Action.Right
    if(integer == 2) : return Action.Up
    if(integer == 3) : return Action.Down
    print("ERREUR DE CONVERSION : int2Action → EXIT")
    exit(0)