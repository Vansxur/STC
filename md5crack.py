import hashlib

def hash_md5(chaine):
    """Convertit une chaîne en hash MD5"""
    return hashlib.md5(chaine.strip().encode()).hexdigest()

def comparer_hash(fichier, hash_cible):
    """Compare chaque ligne d'un fichier avec un hash MD5 donné"""
    try:
        with open(fichier, "r", encoding="utf-8") as file:
            for ligne in file:
                ligne_hash = hash_md5(ligne)
                print(f"Test : {ligne.strip()} → {ligne_hash}")
                
                if ligne_hash == hash_cible:
                    print(f"\n✅ Correspondance trouvée : {ligne.strip()}")
                    return ligne.strip()
        
        print("\n❌ Aucune correspondance trouvée.")
        return None

    except FileNotFoundError:
        print("🚨 Erreur : Le fichier n'existe pas.")
        return None

# 🔹 Exemple d'utilisation
if __name__ == "__main__":
    fichier_entrée = input("🔍 Entrez le chemin du fichier : ")
    hash_cible = input("🎯 Entrez le hash MD5 à comparer : ")
    
    result = comparer_hash(fichier_entrée, hash_cible)
    
    if result:
        print(f"\n🎉 Mot trouvé : {result}")
    else:
        print("\n🔎 Aucun mot ne correspond au hash fourni.")
