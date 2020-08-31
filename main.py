#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import string
import hashlib
import sys
import argparse

parser = argparse.ArgumentParser(description="Password cracker")
parser.add_argument("-f", "--file", dest="file", help="Chemin du fichier disctionnaire", required=False)
parser.add_argument("-g", "--generate", dest="gen", help="genere un hash md5", required=False)
parser.add_argument("-md5", dest="md5", help="Mot de passe hacher en md5", required=False)
parser.add_argument("-l", dest="long", help="Longueur du mot de passe", required=False, type=int)
args = parser.parse_args()

#md5 très faillible, il renvoit des bytes et hexigest permet de retourner un string

def crack_dict(md5, file):
    try:
        trouver = False
        file = open(file, "r")
        for mot in file:
            mot = mot.strip("\n").encode("utf8")
            mot_hashed = hashlib.md5(mot).hexdigest()
            print(f"Essai mot => {mot} et son hash vaut : => {mot_hashed}")
            if mot_hashed == md5:
                print(f'Mot de passe trouvé : {mot} dont le hash est : {mot_hashed} en {time.time() - debut_crack} secondes')
                trouver = True
            if trouver:
                break
        if not trouver:
            print("Mot de passe non-trouvé")
        file.close()
    except FileNotFoundError:
        print("Fichier non trouvé")
        sys.exit(1)
    except Exception as err:
        print("Erreur trouvé dans crack_dict() :", err)
        sys.exit(1)

def crack_incr(md5, length, currentPassword=[]):
    lettres = string.ascii_letters
    if length >= 1:
        if len(currentPassword) == 0:
            currentPassword = ['a' for _ in range(length)] #mettre autant de 'a' que la longueur length
            crack_incr(md5, length, currentPassword)
        else:
            for c in lettres:
                currentPassword[length-1] = c
                print("Trying : " + "".join(currentPassword))
                if hashlib.md5("".join(currentPassword).encode("utf8")).hexdigest() == md5:
                    print("Mot de passe trouvé : " + "".join(currentPassword) + " en " + str(time.time() - debut_crack) + " secondes")
                    sys.exit(0)
                else:
                    crack_incr(md5, length-1, currentPassword)


debut_crack = time.time()
if args.md5:
    print(f"[CRACKING HASH {args.md5}]")
    if args.file and not args.long:
        print(f"[USING DICTIONNARY {args.file}]")
        crack_dict(args.md5, args.file)
    elif args.long and not args.file:
        print(f"USING INCREMENTAL MODE FOR {args.long} letters")
        crack_incr(args.md5, args.long)
    else:
        print("Choose -l or -f argument")
else:
    print("Pas de hash md5 de fournit")

if args.gen:
    print(f"[MD5 HASH DE {args.gen} : " + hashlib.md5(args.gen.encode("utf8")).hexdigest())
