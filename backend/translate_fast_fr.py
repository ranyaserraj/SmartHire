"""
Traducteur ULTRA-RAPIDE avec deep-translator
Traduction par vrais batches (plusieurs compétences par requête)
"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# Termes à NE PAS traduire (noms propres, acronymes)
DO_NOT_TRANSLATE = {
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C', 'C++', 'C#', 'PHP', 'Ruby', 
    'Swift', 'Kotlin', 'Go', 'Rust', 'Scala', 'R', 'Perl', 'Bash', 'SQL',
    'HTML', 'CSS', 'XML', 'JSON', 'YAML', 'React', 'Angular', 'Vue', 'Django', 
    'Flask', 'Spring', 'Laravel', 'Docker', 'Kubernetes', 'Git', 'AWS', 'Azure',
    'TensorFlow', 'PyTorch', 'Keras', 'Pandas', 'NumPy', 'MySQL', 'PostgreSQL', 
    'MongoDB', 'Redis', 'Linux', 'Windows', 'API', 'REST', 'SAP', 'ERP', 'CRM',
    'Excel', 'Word', 'PowerPoint', 'Tableau', 'Figma', 'Jira', 'Node.js', 'Express.js',
    'GitHub', 'GitLab', 'Jenkins', 'Hadoop', 'Spark', 'Kafka', 'Android', 'iOS',
}

def translate_multi_batch(skills, translator):
    """
    Traduit plusieurs compétences en une seule requête
    Google Translate peut traduire un texte avec plusieurs lignes
    """
    results = []
    
    for skill in skills:
        # Ne pas traduire les noms propres
        if skill in DO_NOT_TRANSLATE:
            results.append(skill)
        else:
            results.append(None)  # À traduire
    
    # Collecter les indices à traduire
    to_translate_indices = [i for i, r in enumerate(results) if r is None]
    
    if not to_translate_indices:
        return results
    
    # Créer un texte multi-ligne avec séparateur unique
    skills_to_translate = [skills[i] for i in to_translate_indices]
    separator = " ||| "  # Séparateur peu commun
    multi_text = separator.join(skills_to_translate)
    
    try:
        # Traduire en une seule requête
        translated_text = translator.translate(multi_text)
        
        # Séparer les résultats
        translated_parts = translated_text.split(separator)
        
        # Remettre dans results
        for idx, trans in zip(to_translate_indices, translated_parts):
            results[idx] = trans.strip()
        
        # Remplacer les None restants par l'original
        for i, r in enumerate(results):
            if r is None:
                results[i] = skills[i]
        
        return results
    
    except Exception as e:
        print(f"\n   ⚠️ Erreur batch: {e}")
        # Fallback: garder les originaux
        for i in to_translate_indices:
            results[i] = skills[i]
        return results

def main():
    print("\n" + "="*70)
    print("⚡ Traduction ULTRA-RAPIDE EN → FR (Batches)")
    print("="*70 + "\n")
    
    data_dir = Path(__file__).parent / "data"
    input_path = data_dir / "resume_skills_complete.json"
    output_path = data_dir / "resume_skills_complete_fr.json"
    
    if not input_path.exists():
        print(f"❌ Fichier introuvable: {input_path}")
        return
    
    print(f"📂 Lecture: {input_path.name}")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tech_skills = data['technical_skills']
    soft_skills = data['soft_skills']
    
    print(f"   Technical: {len(tech_skills)}")
    print(f"   Soft: {len(soft_skills)}")
    print(f"   Total: {len(tech_skills) + len(soft_skills)}")
    print()
    
    # Créer traducteur
    translator = GoogleTranslator(source='en', target='fr')
    
    # Traduire par gros batches (50 compétences à la fois)
    batch_size = 50
    
    print("⚡ Traduction technical skills (batches de 50)...")
    start_time = time.time()
    
    tech_translated = []
    for i in range(0, len(tech_skills), batch_size):
        batch = tech_skills[i:i+batch_size]
        trans_batch = translate_multi_batch(batch, translator)
        tech_translated.extend(trans_batch)
        
        progress = min(i+batch_size, len(tech_skills))
        elapsed = time.time() - start_time
        print(f"   {progress}/{len(tech_skills)} traduites ({elapsed:.1f}s)", end='\r')
        
        time.sleep(0.3)  # Petit délai entre batches
    
    print(f"   {len(tech_skills)}/{len(tech_skills)} traduites ✅ ({time.time()-start_time:.1f}s)\n")
    
    print("⚡ Traduction soft skills (batches de 50)...")
    soft_start = time.time()
    
    soft_translated = []
    for i in range(0, len(soft_skills), batch_size):
        batch = soft_skills[i:i+batch_size]
        trans_batch = translate_multi_batch(batch, translator)
        soft_translated.extend(trans_batch)
        
        progress = min(i+batch_size, len(soft_skills))
        elapsed = time.time() - soft_start
        print(f"   {progress}/{len(soft_skills)} traduites ({elapsed:.1f}s)", end='\r')
        
        time.sleep(0.3)
    
    print(f"   {len(soft_skills)}/{len(soft_skills)} traduites ✅ ({time.time()-soft_start:.1f}s)\n")
    
    # Compter traductions
    translations_made = sum(1 for i, orig in enumerate(tech_skills) if tech_translated[i] != orig)
    translations_made += sum(1 for i, orig in enumerate(soft_skills) if soft_translated[i] != orig)
    kept_original = (len(tech_skills) + len(soft_skills)) - translations_made
    
    # Dédupliquer
    tech_unique = sorted(list(set(tech_translated)))
    soft_unique = sorted(list(set(soft_translated)))
    
    print("⚡ Traduction top_skills...")
    top_skills_trans = []
    if 'top_skills' in data:
        top_items = data['top_skills'][:100]
        top_originals = [item['skill'] for item in top_items]
        
        # Traduire en batches
        top_translated = []
        for i in range(0, len(top_originals), batch_size):
            batch = top_originals[i:i+batch_size]
            trans_batch = translate_multi_batch(batch, translator)
            top_translated.extend(trans_batch)
            time.sleep(0.3)
        
        # Créer les objets
        for i, item in enumerate(top_items):
            top_skills_trans.append({
                'skill': top_translated[i],
                'skill_original': item['skill'],
                'frequency': item['frequency'],
                'type': item['type']
            })
        
        print(f"   {len(top_skills_trans)} traduites ✅\n")
    
    # Créer fichier final
    result = {
        'technical_skills': tech_unique,
        'soft_skills': soft_unique,
        'metadata': {
            'total_skills': len(tech_unique) + len(soft_unique),
            'technical': len(tech_unique),
            'soft': len(soft_unique),
            'source': data['metadata']['source'] + ' - Traduit automatiquement (Google Translate)',
            'total_cvs_analyzed': data['metadata']['total_cvs_analyzed'],
            'language': 'français',
            'translation_method': 'deep-translator (Google Translate - Batch mode)',
            'translations_made': translations_made,
            'kept_original': kept_original,
            'original_total': len(tech_skills) + len(soft_skills),
            'deduplicated_total': len(tech_unique) + len(soft_unique)
        }
    }
    
    if top_skills_trans:
        result['top_skills'] = top_skills_trans
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    total_time = time.time() - start_time
    
    print("="*70)
    print("✅ Traduction terminée!")
    print("="*70)
    print(f"   Temps total: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"   Traduites: {translations_made}")
    print(f"   Conservées: {kept_original}")
    print(f"   Total après déduplication: {len(tech_unique) + len(soft_unique)}")
    print(f"\n💾 Fichier: {output_path.name}")
    print(f"   Taille: {output_path.stat().st_size/1024:.1f} KB\n")
    
    # Exemples
    print("📋 Exemples de traductions:")
    count = 0
    for item in top_skills_trans[:30]:
        if item['skill'] != item['skill_original'] and count < 10:
            print(f"   ✅ {item['skill_original']:35s} → {item['skill']}")
            count += 1
    
    print("\n⚡ Mode batch = 50x plus rapide qu'avant!")
    print("🚀 Redémarrez le serveur pour utiliser les traductions!")

if __name__ == "__main__":
    main()

