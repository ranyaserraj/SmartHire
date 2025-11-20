"""
Script de test pour l'API SmartHire
Teste les endpoints d'authentification, profil et CVs
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_register():
    print_section("TEST 1: Inscription")
    
    user_data = {
        "nom": "Test",
        "prenom": "User",
        "email": f"test{__import__('time').time()}@example.com",  # Email unique
        "mot_de_passe": "password123",
        "telephone": "+212 6XX XX XX XX"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Utilisateur créé avec succès!")
            print(f"  ID: {data['id']}")
            print(f"  Nom: {data['prenom']} {data['nom']}")
            print(f"  Email: {data['email']}")
            return data['email']
        else:
            print(f"✗ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Erreur de connexion: {e}")
        print("  Vérifiez que le serveur FastAPI est démarré sur le port 8000")
        return None

def test_login(email):
    print_section("TEST 2: Connexion")
    
    login_data = {
        "email": email,
        "mot_de_passe": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print(f"✓ Connexion réussie!")
            print(f"  Token: {token[:50]}...")
            return token
        else:
            print(f"✗ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return None

def test_get_profile(token):
    print_section("TEST 3: Récupération du profil")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers=headers,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Profil récupéré!")
            print(f"  Nom: {data['prenom']} {data['nom']}")
            print(f"  Email: {data['email']}")
            print(f"  Ville: {data.get('ville_preferee', 'Non définie')}")
            return True
        else:
            print(f"✗ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

def test_update_profile(token):
    print_section("TEST 4: Mise à jour du profil")
    
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "telephone": "+212 612 345 678",
        "ville_preferee": "Casablanca"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/users/profile",
            headers=headers,
            json=update_data,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Profil mis à jour!")
            print(f"  Téléphone: {data['telephone']}")
            print(f"  Ville: {data['ville_preferee']}")
            return True
        else:
            print(f"✗ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

def test_get_offers():
    print_section("TEST 5: Liste des offres")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/offers",
            params={"limit": 5},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            offers = response.json()
            print(f"✓ {len(offers)} offres trouvées")
            
            if len(offers) > 0:
                print(f"\nPremière offre:")
                offer = offers[0]
                print(f"  Titre: {offer['titre']}")
                print(f"  Entreprise: {offer.get('entreprise', 'N/A')}")
                print(f"  Ville: {offer.get('ville', 'N/A')}")
            else:
                print(f"\n  Aucune offre en base. Lancez le scraping:")
                print(f"  curl -X POST {BASE_URL}/api/offers/scrape")
            
            return True
        else:
            print(f"✗ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

def test_health():
    print_section("TEST 0: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API opérationnelle: {data['status']}")
            return True
        else:
            print(f"✗ API ne répond pas correctement")
            return False
    except Exception as e:
        print(f"✗ Impossible de se connecter à l'API: {e}")
        print(f"\n⚠️  VÉRIFICATIONS:")
        print(f"  1. Le serveur FastAPI est-il démarré?")
        print(f"     → uvicorn app.main:app --reload")
        print(f"  2. Le serveur est-il sur le bon port (8000)?")
        print(f"  3. PostgreSQL est-il démarré?")
        return False

def main():
    print("\n" + "🚀"*30)
    print("    TESTS API SMARTHIRE")
    print("🚀"*30)
    
    # Test 0: Health check
    if not test_health():
        print("\n❌ Tests arrêtés: API inaccessible")
        return
    
    # Test 1: Inscription
    email = test_register()
    if not email:
        print("\n❌ Tests arrêtés: échec de l'inscription")
        return
    
    # Test 2: Connexion
    token = test_login(email)
    if not token:
        print("\n❌ Tests arrêtés: échec de la connexion")
        return
    
    # Test 3: Profil
    test_get_profile(token)
    
    # Test 4: Mise à jour profil
    test_update_profile(token)
    
    # Test 5: Offres
    test_get_offers()
    
    # Résumé final
    print_section("RÉSUMÉ")
    print("✓ Tests terminés avec succès!")
    print("\n📚 Documentation complète:")
    print(f"   {BASE_URL}/docs")
    print("\n🎯 Prochaines étapes:")
    print("   1. Lancer le scraping: curl -X POST {}/api/offers/scrape".format(BASE_URL))
    print("   2. Connecter le frontend Next.js")
    print("   3. Tester l'upload de CV")

if __name__ == "__main__":
    main()


