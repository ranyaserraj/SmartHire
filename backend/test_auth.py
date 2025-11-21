"""
Script de test pour l'authentification
Teste les endpoints register, login, et me
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_auth():
    print("=" * 60)
    print("🧪 TEST D'AUTHENTIFICATION - SmartHire")
    print("=" * 60)
    print()
    
    # Test 1: Vérifier si le serveur est en cours d'exécution
    print("1️⃣  Test de connexion au serveur...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ Serveur accessible")
        else:
            print(f"   ⚠️  Serveur répond mais statut: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERREUR: Serveur non accessible")
        print("   💡 Solution: Démarrez le serveur avec START_SERVER.bat")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    print()
    
    # Test 2: Inscription
    print("2️⃣  Test d'inscription...")
    test_user = {
        "email": "test@smarthire.com",
        "mot_de_passe": "test123456",
        "nom": "Test",
        "prenom": "User",
        "telephone": "+212612345678",
        "ville_preferee": "Casablanca"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            print("   ✅ Inscription réussie")
            user_data = response.json()
            print(f"   📧 Email: {user_data['email']}")
            print(f"   👤 Nom: {user_data['prenom']} {user_data['nom']}")
        elif response.status_code == 400:
            print("   ⚠️  Email déjà enregistré (normal si déjà testé)")
        else:
            print(f"   ❌ Erreur lors de l'inscription: {response.status_code}")
            print(f"   📝 Détails: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    print()
    
    # Test 3: Connexion
    print("3️⃣  Test de connexion...")
    login_data = {
        "email": test_user["email"],
        "mot_de_passe": test_user["mot_de_passe"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ Connexion réussie")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   🔑 Token reçu: {access_token[:50]}...")
        else:
            print(f"   ❌ Erreur lors de la connexion: {response.status_code}")
            print(f"   📝 Détails: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    print()
    
    # Test 4: Récupérer les infos utilisateur
    print("4️⃣  Test de récupération du profil...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ Profil récupéré avec succès")
            user_info = response.json()
            print(f"   👤 ID: {user_info['id']}")
            print(f"   📧 Email: {user_info['email']}")
            print(f"   👤 Nom complet: {user_info['prenom']} {user_info['nom']}")
            if user_info.get('telephone'):
                print(f"   📱 Téléphone: {user_info['telephone']}")
            if user_info.get('ville_preferee'):
                print(f"   🏙️  Ville: {user_info['ville_preferee']}")
        else:
            print(f"   ❌ Erreur lors de la récupération du profil: {response.status_code}")
            print(f"   📝 Détails: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
    print("=" * 60)
    print()
    print("💡 L'authentification fonctionne correctement.")
    print("   Si le frontend ne fonctionne pas, vérifiez:")
    print("   1. Le frontend est en cours d'exécution (npm run dev)")
    print("   2. Les CORS sont configurés dans le backend")
    print("   3. Les URLs dans AuthContext.tsx pointent vers http://localhost:8080")
    print()
    
    return True


if __name__ == "__main__":
    try:
        test_auth()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue: {e}")

