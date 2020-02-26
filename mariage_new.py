from __future__ import unicode_literals
import random
from copy import copy
import xlrd
from xlrd import open_workbook
import xlwt
import numpy as np

"""Ce qui suit est une partie d'un code trouvé sur internet que j'ai modifié pour le faire marcher bien dans
le cas des familles de parrainage.
Pour obtenir les familles sans essayer de comprendre le code, aller à la fin de ce document.
Ne pas oublier de mettre 'individual.py' dans le même dossier afin de pouvoir l'importer """

class Individual():
    #constructeur :
    def __init__(self, nom, reponses, famille):
        self.nom = nom
        self.reponses = reponses[:-1]
        self.famille=-1
        for x in famille:
            if x[1]==nom:
                self.famille=x[0]
        self.preference_list = []
        self.available_proposals = []
        self.partner = None
        self.moy_lovesc=-1

    #Fonction de copie :
    def copiage(self):
        cop=Individual("",[],[])
        cop.nom = self.nom
        cop.reponses = self.reponses
        cop.famille=self.famille
        cop.preference_list =[]
        cop.available_proposals =[]
        cop.partner = None
        cop.moy_lovesc= -1
        return(cop)

        """Si ça marche pas, peut être que dé-commenter la section ci-dessus résolvera le problème
        (idem que pour la classe MarriagesSimulation, je me sers pas de tout mais je me rapelle plus si ce dont
        je me sert plus je peux le supprimer ou pas, donc je l'ai commenté au cas ou)"""

        output = ('nom={0}   '
                  'partner={1}'.format(
                     self.nom,
                     self.partner.nom if self.partner else None))
        return output


## Lovescore

#On configure un tableau pour pondérer les réponses :
ponde = [4,2,1,1,2,2,1,1,3,6,3,15,7] #A modifier selon l'ordre des questions

def moyenne(l):
    s=0
    for x in l:
        s+=x
    return(s/len(l))

def LoveScore(Romeo,Juliet,p=ponde):
    r1,r2=Romeo.reponses, Juliet.reponses
    nbReponses = len(r1)
    s=0
    for k in range(nbReponses): #On commence a 2 pour éviter le nom et la famille
        if k ==0 : #traitement spécial pour les listes
            for x in r1[k]:
                if x in r2[k]:
                    if x=="Pas de liste":
                        s-=3*p[k]
                    else:
                        s-=p[k]
        elif k == 2 :    #idem pour la musique
            for x in r1[k]:
                if x in r2[k]:
                    if x=="Je suis aigri et j'aime pas la musique":
                        s-=3*p[k]
                    else:
                        s-=p[k]
        elif k ==  3:    #idem pour les centre d'intérêts artistiques
            for x in r1[k]:
                if x in r2[k]:
                    if x=="pas du tout":
                        s-=3*p[k]
                    else:
                        s-=p[k]
        elif k ==  7:    #idem pour le type de sport pratiqué
            for x in r1[k]:
                if x in r2[k]:
                    if x=="Pas de sport":
                        s=s
                    else:
                        s-=p[k]
        elif k ==  6:    #pour le but du sport on test juste l'égalité des deux
            if r1[k]!=r2[k]:
                s+=2*p[k]
        else:
            s+=abs(r1[k]-r2[k])*p[k] #Si ils répondent la même chose 0 points, plus il y a de points au total moins le match est bon
    return (max(s,0))

#Modifier la fonction LoveScore si jamais le système de notation n'est pas satsfaisant

## Marriage

class MarriagesSimulation():
    """A simulation of men and women being matched with the Gale-Shapley
       algorithm."""
    """Ca je l'ai pris sur internet (flemme de faire un truc qui existe déjà) du coup comme j'ai modifié
    le reste de l'algo il y a des sections de MarriagesSimulation qui servent plus, mais comme ça fait
    longtemps je me rappelle plus si je peux les supprimer sans tout faire buger ou pas, du coup je laisse"""

    #Constructeur :
    def __init__(self, men,women):
        """Initialize the fundamental components of the simulation.

        Args:
            size: The size of the simulation, in numbers of men, which will be
                  the same as the number of women.
        """
        self.men = men
        self.women = women
        self.size = len(men)
        self.sizew = len(women)
        fammax=-1
        for man in self.men :
            if man.famille>fammax:
                fammax=man.famille
        self.fmax=fammax

    #Fusion de deux mariage
    def merge(self,M2):
        self.men+=M2.men
        self.women+=M2.women
        self.size+=M2.size
        self.sizew+=M2.sizew
        self.fmax=max(M2.fmax,self.fmax)


    def debut(self):
        """Pour remplir les available_proposals"""
        for i in self.men:
            i.available_proposals=self.women

    #Renvoie le nombre de parrain par famille :
    def fam_taille(self):
        taille=[0 for i in range(self.fmax+1)]
        for man in self.men :
            taille[man.famille]+=1
        return(taille)

    #Permet d'ajouter des parrains "fantôme" dans le cas où il y a plus de fillots que de parrains :
    def ajout_p(self):
        taille=self.fam_taille()
        nb_ajout=0
        men=[]
        for i in range(self.fmax+1):
            if taille[i]!=7:
                k=0
                man=self.men[0]
                while man.famille!=i:
                    k+=1
                    man=self.men[k]
                new=man.copiage()
                men.append(new)
                nb_ajout+=1
        return(men,nb_ajout)

    def populate(self):
        """Populate the simulation with valid men and women."""
        for i in range(0, self.size):
            self.men.append(Individual(i))
        for i in range(self.size, self.size * 2):
            self.women.append(Individual(i))

    def set_preferences(self):
        """Set the preference list for all the men and women in this
           simulation."""
        self.Moy_lovscore()
        women=self.tri_lovesc_women()
        for man in self.men:
            man.preference_list =[self.women[x[0]] for x in women]
            man.available_proposals =man.preference_list

    #Calcul de la moyenne de Lovescore pour chaque individu :
    def Moy_lovscore(self):
        echantw=[i for i in range(self.sizew)]
        echant=[i for i in range(self.size)]
        for man in self.men:
            random.shuffle(echant)
            love=[LoveScore(man,self.women[echantw[i]]) for i in range(self.sizew)]
            man.moy_lovesc=moyenne(love)
        for woman in self.women:
            random.shuffle(echant)
            love=[LoveScore(woman,self.men[echant[i]]) for i in range(self.size)]
            woman.moy_lovesc=moyenne(love)

    #Ordone les parrains par moyenne de Lovescore décroissant:
    def tri_lovesc_men(self):
        a=np.array([])
        type_men=[('pers',type(self.men[1])),('lv_sc',int)]
        men_sorted=np.array([(man,man.moy_lovesc) for man in self.men],dtype=type_men)
        men_sorted=np.sort(men_sorted,order="lv_sc")
        return(men_sorted)

    #Ordone les fillots par moyenne de Lovescore décroissant:
    def tri_lovesc_women(self):
        type_women=[('pers',int),('lv_sc',int)]
        women_sorted=(np.array([(i,self.women[i].moy_lovesc) for i in range(self.sizew)],dtype=type_women))
        women_sorted.sort(order="lv_sc")
        women_sorted=women_sorted.tolist()
        women_sorted.reverse()
        return(women_sorted)

    #Calcul le poids(Lovescore cummulé de tous les matchs) total du marriage et les parrains non matché (permet d'évaluer la performance du match):
    def poids(self):
        pds=0
        non_match=0
        for man in self.men:
            if man.partner==None:
                non_match+=1
            else:
                pds+= LoveScore(man.partner,man)
        return(pds,non_match)

    def random_id_list(self):
        """Get a randomized list of indexes that may be used to refer to
           internal lists of men and women.

        Returns:
            A randomized list of indexes.
        """
        id_list = [k for k in range(0, self.size)]
        random.shuffle(id_list)
        return id_list

    def random_idw_list(self):
        """Get a randomized list of indexes that may be used to refer to
           internal lists of men and women.

        Returns:
            A randomized list of indexes.
        """
        id_list = [k for k in range(0, self.sizew)]
        random.shuffle(id_list)
        return id_list

    def random_man_list(self):
        """Get a randomized list of men from this simulation.

        Returns:
            A random list of Man objects.
        """
        random_id_list = self.random_id_list()
        man_list = []
        for i in random_id_list:
            man_list.append(self.men[i])
        return man_list

    def random_woman_list(self):
        """Get a randomized list of women from this simulation.

        Returns:
            A random list of Woman objects.
        """
        random_id_list = self.random_idw_list()
        woman_list = []
        for i in random_id_list:
            woman_list.append(self.women[i])
        return woman_list

    def is_stable(self):
        """Check if this simulation has reached a stable state.

        The simulation is considered stable if both members of a couple would
        not be happier with an alternative match.

        Returns:
            A boolean indicating the stability of this simulation.
        """
        for woman in self.women:
            if not woman.partner:
                return False
        return True

    def pair_couple(self, man, woman):
        """Pair two individuals.

        The man in this couple will no longer be able to propose
        to the specified woman.

        Args:
            man: The first individual.
            woman: The second individual.
        """
        man.partner = woman
        woman.partner = man

    def free_couple(self, man, woman):
        """Free two individuals.

        Args:
            man: The first individual.
            woman: The second individual.
        """
        man.partner = None
        woman.partner = None

    def match(self):
        """Perform the Gale-Shapley matching algorithm.

        Print new matches that are made and the state of the simulation
        between iterations.
        """
        iterations = 0
        flts=0
        while not self.is_stable() and iterations<=100:
            iterations += 1
            s=0
            for man in self.men:
                s+=len(man.available_proposals)
                if not man.partner:
                    for woman in man.available_proposals:
                        if not woman.partner:

                            self.pair_couple(man, woman)
                            man.available_proposals.remove(woman)
                            flts+=1
                            break
                        else:

                            if LoveScore(man,woman) < LoveScore(woman.partner, woman):

                                self.free_couple(woman.partner, woman)
                                self.pair_couple(man, woman)
                                man.available_proposals.remove(woman)
                                break
                            else:
                                man.available_proposals.remove(woman)
        print("nb fillots ----> ", flts)


    def famille_liste(self): #récupère la liste des familles inscrites
        F=[]
        for man in self.men:
            if not(man.famille in F):
                F.append(man.famille)
        return(F)

    #Rempli le Excel avec les familles :
    def ecriture(self):
        wb = xlwt.Workbook('familles.xls') #création d'un fichier excel
        s = wb.add_sheet('A Test Sheet') #on crée une feuill de calcul
        familles=self.famille_liste()
        nbfam=len(familles)
        nb_membre_fam=[0 for x in familles] #stock le nombre de membre écrit dans chaque famille
        # écriture des entêtes :
        filts=0
        for i in range((nbfam//10)):
            x=3*i
            for j in range(10):
                y=10*j
                s.write(y,x+1,(10*i)+j+1,style_entete_d)
                s.write(y,x,"Nom de la famille : ",style_entete_g)
                s.write(y+1,x,"Parrains :",style_parrains_ent)
                s.write(y+1,x+1,"Fillots :",style_fillots_ent)
        for j in range(nbfam%10):
            y=10*j
            x=(nbfam//10)*3
            s.write(y,x+1,Familles_g[(nbfam//10)*10+j][0],style_entete_d)
            s.write(y,x,"Nom de la famille : ",style_entete_g)
            s.write(y+1,x,"Parrains :",style_parrains_ent)
            s.write(y+1,x+1,"Fillots :",style_fillots_ent)
        # écriture des noms :
        for man in self.men:
            famille=man.famille
            x=(famille//10)*3
            y=10*(famille%10)+2+nb_membre_fam[famille]
            if nb_membre_fam[famille]!=6:
                s.write(y,x,man.nom,style_parrains)
                if man.partner!=None :
                    s.write(y,x+1,man.partner.nom,style_fillots)
                    filts+=1
                else :
                    s.write(y,x+1," ",style_fillots)
            else:
                s.write(y,x,man.nom,style_parrains_fin)
                if man.partner!=None :
                    s.write(y,x+1,man.partner.nom,style_fillots_fin)
                    filts+=1
                else :
                    s.write(y,x+1," ",style_fillots_fin)
            nb_membre_fam[famille]+=1
        # fin de la mise en page :
        for i in range(len(nb_membre_fam)):
            f=nb_membre_fam[i]
            for j in range(f,7):
                y=((10*((i)%10))+j)+2
                x=((i)//10)*3
                if j!=6:
                    s.write(y,x," ",style_parrains)
                    s.write(y,x+1," ",style_fillots)
                else:
                    s.write(y,x," ",style_parrains_fin)
                    s.write(y,x+1," ",style_fillots_fin)
        print(filts)
        wb.save('familles.xls')

    def __str__(self):
        men_outputs = []
        for man in self.men:
            men_outputs.append(u'\t' + str(man))
        men_string = '\n'.join(men_outputs)
        women_outputs = []
        for woman in self.women:
            women_outputs.append('\t' + str(woman))
        women_string = '\n'.join(women_outputs)
        return ('Men:\n'
                '{0}\n'
                'Women:\n'
                '{1}'.format(men_string, women_string))

## Algo famille

## Fonctions de lecture fichier
#Ouverture des feuilles :

parrains=xlrd.open_workbook("Questionnaire Parrain-Fillot (Parrains).xlsx")
shnp=parrains.sheet_names()
shp=parrains.sheet_by_name(shnp[1]) #Feuille qui m'interresse
shfam=parrains.sheet_by_name(shnp[3]) #feuille avec les familles
shfampers=parrains.sheet_by_name(shnp[2]) #feuille avec les corespondances familles/personnes

def ListeFamille():
    n=shfam.ncols
    l=shfam.row_values(1)
    famille_id=[(l[i],i) for i in range(1,n)]
    return(famille_id)

def  ListeFamille_Pers():
    n=shfampers.ncols
    l=[]
    fam_pers=[]
    for i in range(6):
        l.append(shfampers.row_values(i+1)[1:])
    for i in range(6):
        for k in range(len(l[i])):
            if l[i][k]!="":
                fam_pers.append((k,(l[i][k])))
    return(fam_pers)

Familles_g=ListeFamille()
CompFam=ListeFamille_Pers()

def ListeParrains():
    #EI2={}  <-- Si on voulait faire avec un dictionnaire
    EI2=[]
    n=shp.ncols
    for k in range(1,shp.nrows):
        l=shp.row_values(k)
        #EI2["EI2"+str(k)]=[l[1],l[2:n]]  <-- Idem
        EI2+=[Individual(l[1],l[3:16],CompFam)]
    return(EI2)

fillots=xlrd.open_workbook("Questionnaire Parrain-Fillot (fillots) (réponses).xlsx")
shnf=fillots.sheet_names() #Noms des feuilles
shf=fillots.sheet_by_name(shnf[0]) #Feuille qui m'interresse

def ListeFillots():
    EI1=[]
    n=shf.ncols
    for k in range(1,shf.nrows):
        l=shf.row_values(k)
        EI1+=[Individual(l[1],l[3:16],CompFam)]
    return(EI1)


## Exploitation des réponses

def transformationrep(EI):
    for i in EI:
        j=i.reponses
        j[0]=j[0].split(", ")
        j[2]=j[2].split(", ")
        j[3]=j[3].split(", ")
        j[4]=int(j[4].replace("Seulement les soirs de pleine lune","0").replace("Une fois de temps en temps","1").replace("Quelques fois par semaine","2").replace("Une fois par jour","3"))
        j[5]=int(j[5].replace("Le dimanche à 15h32 s'il fait beau","0").replace("Une fois par semaine","1").replace("Plusieurs fois par semaine","2").replace("Une fois par jour","3"))
        j[7]=j[7].split(", ")
        j[8]=int(j[8].replace("Alterner entre grec et coquillettes ça compte ?","0").replace("Oh oui, et les trucs bien gras ça me connait !","1").replace("J'aime cuisiner le WE ou quand j'ai le temps","2").replace("Je fais toujours attention à bien manger","3"))
        j[10]=int(j[10].replace("Jamais","0").replace("Une fois par mois","1").replace("Une fois par semaine","2").replace("Une fois par jour (voire plus)","4").replace("Plusieurs fois par semaine","3"))
        j[11]=int(j[11].replace("Tu viens pas","0").replace("Tu te poses dans un coin, chill !!","1").replace("Objectif grosse défonce","2").replace("T'enflammes le dancefloor","3"))
    return(EI)


def epure(EI): #Pas necessaire si vous trouvez un moyen d'authentifier chaque personne et que chaque
                #personne de réponde qu'une fois
    N=[] #liste des noms
    Nt=[] #liste des noms sans doublets
    L=[] #liste qui va contenir les Ei sans doublet
    for i in EI:
        N+=[i.nom]
    for i in N:
        if i in Nt:
            L[Nt.index(i)]=EI[N.index(i)]
        else:
            Nt+=[i]
            L+=[EI[N.index(i)]]
    return(L)
## écriture

#styles des cases (bordures et fond)

style_entete_g= xlwt.easyxf('font: bold on, color black;\
borders: top_color black, bottom_color black, left_color black,\
left thin, top thin,bottom thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_entete_d= xlwt.easyxf('font: bold on, color black;\
borders: top_color black, bottom_color black,right_color black ,\
right thin, top thin,bottom thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_fillots_ent= xlwt.easyxf('font: bold on, color black;\
borders:right_color black,\
right thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_parrains_ent= xlwt.easyxf('font: bold on, color black;\
borders:left_color black,\
left thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_fillots= xlwt.easyxf('font: bold off, color black;\
borders:right_color black,\
right thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_parrains= xlwt.easyxf('font: bold off, color black;\
borders:left_color black,\
left thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_fillots_fin= xlwt.easyxf('font: bold off, color black;\
borders: bottom_color black,right_color black,\
right thin,bottom thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

style_parrains_fin= xlwt.easyxf('font: bold off, color black;\
borders:bottom_color black,left_color black,\
left thin,bottom thin;\
pattern: pattern solid, fore_color white; align : horiz center ;protection:cell_locked false;')

## Algo a lancer

def algo():
    P=transformationrep(ListeParrains()) #on récupère les informations des parrains

    F=transformationrep(ListeFillots()) #on récupère les informations des parrains
    M=MarriagesSimulation(P,F)
    M.set_preferences()
    M.match() #ca va tourner puis afficher les couples en premier Liste1, partenaire=Liste
    #Ajoute des parrains "fantômes" et refait des matchs dans le cas où il y ait plus de fillots que de parrains
    while M.sizew>M.size:
        nouv_fillots=[]
        a_enlever=[]
        for i in range(M.sizew):
            if M.women[i].partner==None:
                nouv_fillots.append((M.women[i]).copiage())
                a_enlever.append(i)
        for i in range(len(a_enlever)-1,-1,-1):
            inutile=M.women.pop(a_enlever[i])
            M.sizew-=1
        if nouv_fillots!=[]:
            nouv_parr,nbparr=M.ajout_p()
            M2=MarriagesSimulation(nouv_parr,nouv_fillots)
            M2.set_preferences()
            M2.match()
            M.merge(M2)
    M.ecriture() #Ecriture dans le Excel
    return(M)
    #, suivi de Liste2, partenaire= Liste1
    #Juste la première liste suffit donc
