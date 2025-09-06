import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont

FICHIER_SAUVEGARDE = "liste_courses.txt"

class ListeCoursesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Application Liste de Courses")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        # Configuration des polices
        self.titre_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.sous_titre_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Arial", size=10)
        
        # Variables
        self.liste_de_courses = self.charger_liste()
        self.categories = ["fruits", "légumes", "produits laitiers", "viandes", "épicerie", "boissons", "autres"]
        
        self.setup_ui()
        self.afficher_liste()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        titre_label = ttk.Label(main_frame, text="🎯 APPLICATION LISTE DE COURSES", 
                               font=self.titre_font, foreground="#2c3e50")
        titre_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame pour les contrôles
        controls_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Boutons d'action
        ttk.Button(controls_frame, text="Ajouter Article", 
                  command=self.ouvrir_ajout, width=20).grid(row=0, column=0, pady=5)
        ttk.Button(controls_frame, text="Supprimer Article", 
                  command=self.supprimer_article, width=20).grid(row=1, column=0, pady=5)
        ttk.Button(controls_frame, text="Vider la Liste", 
                  command=self.vider_liste, width=20).grid(row=2, column=0, pady=5)
        ttk.Button(controls_frame, text="Rechercher", 
                  command=self.ouvrir_recherche, width=20).grid(row=3, column=0, pady=5)
        ttk.Button(controls_frame, text="Sauvegarder", 
                  command=self.sauvegarder_liste, width=20).grid(row=4, column=0, pady=5)
        ttk.Button(controls_frame, text="Quitter", 
                  command=self.quitter, width=20).grid(row=5, column=0, pady=5)
        
        # Frame pour l'affichage de la liste
        list_frame = ttk.LabelFrame(main_frame, text="Ma Liste de Courses", padding="10")
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview pour afficher la liste
        columns = ('catégorie', 'article', 'quantité')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('catégorie', text='Catégorie')
        self.tree.heading('article', text='Article')
        self.tree.heading('quantité', text='Quantité')
        
        self.tree.column('catégorie', width=120)
        self.tree.column('article', width=200)
        self.tree.column('quantité', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configuration des poids pour le redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
    def charger_liste(self):
        """Charge la liste depuis le fichier de sauvegarde"""
        liste_de_courses = []
        if os.path.exists(FICHIER_SAUVEGARDE):
            try:
                with open(FICHIER_SAUVEGARDE, 'r', encoding='utf-8') as f:
                    for ligne in f:
                        ligne = ligne.strip()
                        if ':' in ligne:
                            parts = ligne.split(':', 2)
                            if len(parts) >= 2:
                                categorie = parts[0]
                                article = parts[1]
                                quantite = parts[2] if len(parts) > 2 else "1"
                                liste_de_courses.append((categorie, article, quantite))
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement : {e}")
        return liste_de_courses
    
    def sauvegarder_liste(self):
        """Sauvegarde la liste dans le fichier"""
        try:
            with open(FICHIER_SAUVEGARDE, 'w', encoding='utf-8') as f:
                for categorie, article, quantite in self.liste_de_courses:
                    f.write(f"{categorie}:{article}:{quantite}\n")
            messagebox.showinfo("Sauvegarde", "Liste sauvegardée avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")
    
    def afficher_liste(self):
        """Affiche la liste dans le Treeview"""
        # Vider le treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajouter les éléments
        for i, (categorie, article, quantite) in enumerate(self.liste_de_courses, 1):
            self.tree.insert('', 'end', values=(categorie, article, quantite))
    
    def ouvrir_ajout(self):
        """Ouvre une fenêtre pour ajouter un article"""
        fenetre_ajout = tk.Toplevel(self.root)
        fenetre_ajout.title("Ajouter un article")
        fenetre_ajout.geometry("400x300")
        fenetre_ajout.transient(self.root)
        fenetre_ajout.grab_set()
        
        ttk.Label(fenetre_ajout, text="Ajouter un nouvel article", font=self.sous_titre_font).pack(pady=10)
        
        # Catégorie
        ttk.Label(fenetre_ajout, text="Catégorie:").pack(pady=5)
        categorie_var = tk.StringVar()
        categorie_combo = ttk.Combobox(fenetre_ajout, textvariable=categorie_var, 
                                      values=self.categories, state="readonly")
        categorie_combo.pack(pady=5)
        categorie_combo.set(self.categories[0])
        
        # Article
        ttk.Label(fenetre_ajout, text="Article:").pack(pady=5)
        article_entry = ttk.Entry(fenetre_ajout, width=30)
        article_entry.pack(pady=5)
        
        # Quantité
        ttk.Label(fenetre_ajout, text="Quantité:").pack(pady=5)
        quantite_var = tk.StringVar(value="1")
        quantite_spin = ttk.Spinbox(fenetre_ajout, from_=1, to=100, textvariable=quantite_var, width=10)
        quantite_spin.pack(pady=5)
        
        def valider_ajout():
            categorie = categorie_var.get()
            article = article_entry.get().strip()
            quantite = quantite_var.get()
            
            if not article:
                messagebox.showerror("Erreur", "Veuillez entrer un nom d'article !")
                return
            
            self.liste_de_courses.append((categorie, article, quantite))
            self.afficher_liste()
            self.sauvegarder_liste()
            fenetre_ajout.destroy()
            messagebox.showinfo("Succès", f"'{article}' ajouté à la liste !")
        
        ttk.Button(fenetre_ajout, text="Ajouter", command=valider_ajout).pack(pady=20)
        article_entry.focus()
    
    def supprimer_article(self):
        """Supprime l'article sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article à supprimer !")
            return
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet article ?"):
            index = self.tree.index(selection[0])
            article_supprime = self.liste_de_courses.pop(index)
            self.afficher_liste()
            self.sauvegarder_liste()
            messagebox.showinfo("Succès", f"'{article_supprime[1]}' supprimé de la liste !")
    
    def vider_liste(self):
        """Vide complètement la liste"""
        if not self.liste_de_courses:
            messagebox.showinfo("Info", "La liste est déjà vide !")
            return
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir vider toute la liste ?"):
            self.liste_de_courses.clear()
            self.afficher_liste()
            self.sauvegarder_liste()
            messagebox.showinfo("Succès", "Liste vidée avec succès !")
    
    def ouvrir_recherche(self):
        """Ouvre une fenêtre de recherche"""
        fenetre_recherche = tk.Toplevel(self.root)
        fenetre_recherche.title("Rechercher un article")
        fenetre_recherche.geometry("500x400")
        
        ttk.Label(fenetre_recherche, text="Rechercher un article", font=self.sous_titre_font).pack(pady=10)
        
        # Champ de recherche
        ttk.Label(fenetre_recherche, text="Terme de recherche:").pack(pady=5)
        recherche_var = tk.StringVar()
        recherche_entry = ttk.Entry(fenetre_recherche, textvariable=recherche_var, width=30)
        recherche_entry.pack(pady=5)
        recherche_entry.bind('<KeyRelease>', lambda e: self.executer_recherche(recherche_var.get(), resultats_text))
        
        # Zone de résultats
        ttk.Label(fenetre_recherche, text="Résultats:").pack(pady=5)
        resultats_text = scrolledtext.ScrolledText(fenetre_recherche, width=50, height=15, font=self.normal_font)
        resultats_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        recherche_entry.focus()
    
    def executer_recherche(self, terme, resultats_text):
        """Exécute la recherche et affiche les résultats"""
        resultats_text.delete(1.0, tk.END)
        
        if not terme.strip():
            return
        
        terme = terme.lower()
        resultats = []
        
        for i, (categorie, article, quantite) in enumerate(self.liste_de_courses, 1):
            if terme in article.lower() or terme in categorie.lower():
                resultats.append(f"{i}. [{categorie}] {article} (x{quantite})\n")
        
        if resultats:
            resultats_text.insert(tk.END, f"Résultats pour '{terme}':\n\n")
            for resultat in resultats:
                resultats_text.insert(tk.END, resultat)
        else:
            resultats_text.insert(tk.END, f"Aucun résultat trouvé pour '{terme}'")
    
    def quitter(self):
        """Quitte l'application"""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?\nLa liste sera sauvegardée automatiquement."):
            self.sauvegarder_liste()
            self.root.destroy()

def main():
    root = tk.Tk()
    app = ListeCoursesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()