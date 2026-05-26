# GitHub Setup Guide

Publiez votre repo sur GitHub en **3 étapes faciles**.

## Step 1 : Créer le repo vide sur GitHub

1. Allez à https://github.com/new
2. Remplissez :
   - **Repository name**: `docx-intelligent-shredder`
   - **Description**: `Smart document preprocessing for Word files`
   - **Public** (recommandé pour open-source)
3. **IMPORTANT**: Ne cochez PAS :
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
4. Cliquez **Create repository**

**Copier l'URL** : `https://github.com/[votre-username]/docx-intelligent-shredder.git`

---

## Step 2 : Exécuter le script PowerShell

Ouvrez PowerShell dans le dossier `code_repo` et lancez :

```powershell
.\GITHUB_SETUP.ps1 -GithubUsername "votre-username"
```

Remplacez `votre-username` par votre username GitHub réel.

**Exemple** :
```powershell
.\GITHUB_SETUP.ps1 -GithubUsername "maxime-cabon"
```

---

## Step 3 : Le script va demander votre permission pour pusher

À la fin, il va afficher :
```
Ready to push? Make sure the repo exists on GitHub first.
Press Enter to push, or Ctrl+C to cancel...
```

Appuyez sur **Enter** pour pusher.

---

## C'est tout ! ✓

Votre repo est maintenant live à :
```
https://github.com/[votre-username]/docx-intelligent-shredder
```

---

## Si ça échoue

### Erreur: "Git is not installed"
→ Installez Git: https://git-scm.com

### Erreur: "Push failed"
Les raisons possibles :
1. **Le repo n'existe pas sur GitHub** → Créez-le d'abord (Step 1)
2. **GitHub ne reconnaît pas vos credentials** → Utilisez GitHub CLI ou SSH keys

**Solution facile** : Utilisez GitHub Desktop ou VS Code pour pusher au lieu du script.

---

## Vérifier que ça a marché

Allez à : `https://github.com/[votre-username]/docx-intelligent-shredder`

Vous devriez voir :
- ✓ README.md
- ✓ LICENSE
- ✓ requirements.txt
- ✓ src/ folder
- ✓ docs/ folder
- ✓ Tous les autres fichiers

---

## Questions ?

Si le script échoue, lancez manuellement :

```bash
cd "D:\Projet AI\Management de carrière MCQ\Personal Branding Manager\code_repo"
git push -u origin main
```

Et dites-moi quel message d'erreur vous recevez.
