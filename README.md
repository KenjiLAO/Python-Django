📘 Projet Django – Générateur d'Articles avec ChatGPT + Image IA
Ce projet Django permet à un utilisateur authentifié de générer automatiquement des articles et des illustrations à partir d’un simple titre grâce à l’API OpenAI (ChatGPT + DALL·E).
Cela inclus également les fonctionnalités demandes lors du TP de la semaine

⚙️ Fonctionnalités
🔒 Authentification requise (@login_required)

✍️ Génération de contenu automatique avec gpt-3.5-turbo

🖼️ Génération d’image illustrative avec DALL·E

🧠 Bouton "Générer" dans le formulaire d’ajout d’article

🗂️ Catégorisation et tags fictifs automatiques

🔐 Clé API sécurisée via fichier .env

🧪 Démonstration de fonctionnement
L’utilisateur entre un titre.

Il clique sur "🧠 Générer".

Le backend envoie le prompt à OpenAI :

Génère le texte avec GPT.

Génère une image avec DALL·E.

Le contenu + image sont insérés automatiquement dans le formulaire.

