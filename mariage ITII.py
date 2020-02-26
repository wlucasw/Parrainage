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
    def __init__(self, nom, reponses, famille):
#        self.id_number = id_number
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
        self.cop=None

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

#    def get_priority(self, other):
#        """Get the priority of a match from the perspective of the current
#        person.
#
#        Args:
#            other: The other person in the prospective match.
#
#        Returns:
#            An index indicating the priority of a match.
#            Lower numbers indicate higher priorities.
#        """
#        return self.preference_list.index(other)
#
#    def get_id_list(self, instance_list):
#        """Get a list of ID numbers corresponding to the input
#        list of from xlwt import easyxfinstances.
#
#        Args:
#            intance_list: A list of other Individual objects.
#
#        Returns:
#            A list of ID numbers.
#        """= []
#        for i in instance_list:
#            id_list.append(i.nom if i else None)
#        return id_list

        """Si ça marche pas, peut être que dé-commenter la section ci-dessus résolvera le problème
        (idem que pour la classe MarriagesSimulation, je me sers pas de tout mais je me rapelle plus si ce dont
        je me sert plus je peux le supprimer ou pas, donc je l'ai commenté au cas ou)"""

    # def __str__(self):
    #     output = ('nom={0} preference_list={1} available_proposals={2} '
    #               'partner={3}'.format(
    #                  self.nom,
    #                  self.get_id_list(self.preference_list),
    #                  self.get_id_list(self.available_proposals),
    #                  self.partner.nom if self.partner else None))
    #     return output
    def __str__(self):
        output = ('nom={0}   '
                  'partner={1}'.format(
                     self.nom,
                     self.partner.nom if self.partner else None))
        return output


ponde = [4,2,1,1,2,2,1,1,3,6,3,15,7] #A modifier selon l'ordre des questions

def moyenne(l):
    s=0
    for x in l:
        s+=x
    return(s/len(l))

def LoveScore(Romeo,Juliet,p=ponde): #On configure un tableau pour pondérer les réponses
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
    #print(Juliet.nom,"---",Romeo.nom,"->",s)
    return (max(s,0))

#Modifier la fonction LoveScore si jamais le système de notation n'est pas satsfaisant

class MarriagesSimulation():
    """A simulation of men and women being matched with the Gale-Shapley
       algorithm."""
    """Ca je l'ai pris sur internet (flemme de faire un truc qui existe déjà) du coup comme j'ai modifié
    le reste de l'algo il y a des sections de MarriagesSimulation qui servent plus, mais comme ça fait
    longtemps je me rappelle plus si je peux les supprimer sans tout faire buger ou pas, du coup je laisse"""
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

    def deletem(self,man):
        for i in range(self.size):
            if self.men[i]==man:
                a=self.men.pop(i)
                self.size-=1
                return()

    def ecremage(self):
        nb_fam=[0 for i in range(self.fmax)]
        for man in self.men:
            if nb_fam[man.famille]==2 :
                self.deletem(man)
            else:
                nb_fam[man.famille]+=1

    def merge(self,M2):
        self.men+=M2.men
        self.women+=M2.women
        self.size+=M2.size
        self.sizew+=M2.sizew
        self.fmax=max(M2.fmax,self.fmax)

    def merge_ITII(self,M2):
        self.women=M2.men
        self.sizew=M2.size

    def debut(self):
        """Pour remplir les available_proposals"""
        for i in self.men:
            #i.available_proposals=deepcopy(self.women)
            i.available_proposals=self.women

    def fam_taille(self):
        taille=[0 for i in range(self.fmax+1)]
        for man in self.men :
            taille[man.famille]+=1
        return(taille)

    def ajout_p(self):
        #for i in range(10):
        #print("###### AJOUT ######")
        taille=self.fam_taille()
        nb_ajout=0
        men=[]
        for i in range(self.fmax+1):
            if taille[i]!=7:
                k=0
                man=self.men[0]
                while man.famille!=i:
                    k+=1
                    #print(k)
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
        #women=self.random_woman_list()
        for man in self.men:
            man.preference_list =[self.women[x[0]] for x in women]
            #man.preference_list = self.random_woman_list()
            man.available_proposals =man.preference_list
        # for woman in self.women:
        #     woman.preference_list = self.random_man_list()

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

    def tri_lovesc_men(self):
        a=np.array([])
        type_men=[('pers',type(self.men[1])),('lv_sc',int)]
        men_sorted=np.array([(man,man.moy_lovesc) for man in self.men],dtype=type_men)
        men_sorted=np.sort(men_sorted,order="lv_sc")
        #men_sorted.reverse()
        return(men_sorted)

    def tri_lovesc_women(self):
        type_women=[('pers',int),('lv_sc',int)]
        women_sorted=(np.array([(i,self.women[i].moy_lovesc) for i in range(self.sizew)],dtype=type_women))
        #print(women_sorted)
        women_sorted.sort(order="lv_sc")
        women_sorted=women_sorted.tolist()
        women_sorted.reverse()
        #print(women_sorted)
        return(women_sorted)

    def poids(self):
        pds=0
        n_match=0
        for man in self.men:
            if man.partner==None:
                n_match+=1
            else:
                pds+= LoveScore(man.partner,man)
        return(pds,n_match)

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

    def is_stable_i(self):
        """Check if this simulation has reached a stable state.

        The simulation is considered stable if both members of a couple would
        not be happier with an alternative match.

        Returns:
            A boolean indicating the stability of this simulation.
        """
        for woman in self.women:
            if not woman.cop:
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
        #print ('New pair man={0} woman={1}'.format(man.nom, woman.nom))

    def free_couple(self, man, woman):
        """Free two individuals.

        Args:
            man: The first individual.
            woman: The second individual.
        """
        man.partner = None
        woman.partner = None

    def free_couple_i(self, man, woman):
        """Free two individuals.

        Args:
            man: The first individual.
            woman: The second individual.
        """
        man.cop = None
        woman.cop = None

    def match_ITII(self):
        """Perform the Gale-Shapley matching algorithm.

        Print new matches that are made and the state of the simulation
        between iterations.
        """
        iterations = 0
        flts=0
        #print(self.is_stable())
        while not self.is_stable_i() and iterations<=100:
            #for i in range(10):
                #print("###### MATCH ######")
            iterations += 1
            #print("On en est à la "+str(iterations)+" fois")
            #print ('{0}\n'.format(self))
            s=0
            for man in self.men:
                #print(man.available_proposals)
                s+=len(man.available_proposals)
                if not man.cop:
                    for woman in man.available_proposals:
                        if not woman.cop:

                            man.available_proposals.remove(woman)
                            flts+=1
                            woman.cop=man
                            man.cop=woman
                            break
                        else:

                            if LoveScore(man,woman) < LoveScore(woman.cop, woman): #juste a remplacer le get_priority par lovescore

                                self.free_couple_i(woman.cop, woman)
                                man.available_proposals.remove(woman)
                                woman.cop=man
                                man.cop=woman
                                break
                            else:
                                man.available_proposals.remove(woman)
            #print(self.poids())
            #print(s/self.size)
        #print ('Matching complete')
        #print ('iterations={0}'.format(iterations))

    def match(self):
        """Perform the Gale-Shapley matching algorithm.

        Print new matches that are made and the state of the simulation
        between iterations.
        """
        iterations = 0
        flts=0
        #print(self.is_stable())
        while not self.is_stable() and iterations<=100:
            #for i in range(10):
                #print("###### MATCH ######")
            iterations += 1
            #print("On en est à la "+str(iterations)+" fois")
            #print ('{0}\n'.format(self))
            s=0
            for man in self.men:
                #print(man.available_proposals)
                s+=len(man.available_proposals)
                if not man.partner:
                    for woman in man.available_proposals:
                        if not woman.partner:

                            self.pair_couple(man, woman)
                            self.pair_couple(man.cop,woman.cop)
                            man.available_proposals.remove(woman)
                            if woman.cop in man.cop.available_proposals:
                                man.cop.available_proposals.remove(woman.cop)
                            flts+=1
                            break
                        else:

                            if LoveScore(man,woman)+LoveScore(man.cop,woman.cop) < LoveScore(woman.partner, woman)+LoveScore(woman.partner.cop,woman.cop): #juste a remplacer le get_priority par lovescore
                                self.free_couple(woman.partner.cop,woman.cop)
                                self.free_couple(woman.partner, woman)
                                self.pair_couple(man, woman)
                                self.pair_couple(man.cop,woman.cop)
                                man.available_proposals.remove(woman)
                                if woman.cop in man.cop.available_proposals:
                                    man.cop.available_proposals.remove(woman.cop)
                                break
                            else:
                                man.available_proposals.remove(woman)
            #print(self.poids())
            #print(s/self.size)
        #print("nb fillots ----> ", flts)
        #print ('Matching complete')
        #print ('iterations={0}'.format(iterations))


    def famille_liste(self): #récupère la liste des familles inscrites
        F=[]
        for man in self.men:
            if not(man.famille in F):
                F.append(man.famille)
        return(F)

    def reduc_parrains(self):
        k=0
        for i in range(self.size):
            if self.men[i-k].partner==None:
                self.men.pop(i-k)
                self.size-=1
                k+=1

    def verif_match(self):
        bool=True
        for x in self.men:
            if x.cop==None:
                bool=False
        for y in self.women:
            if y.cop==None:
                bool=False
        return(bool)

    def reduc_fam(self):
        Corresp_fam=[[-1,0,[]] for x in range(self.fmax+1)]
        nbf=1
        k=0
        #print("debut supprésion fam : ",len(self.men))
        #print("verif",self.size)
        for i in range(self.size):
            man=self.men[i-k]
            if Corresp_fam[man.famille][0]==-1:
                Corresp_fam[man.famille][0]=nbf
                nbf+=1
            if Corresp_fam[man.famille][1]<=2:
                Corresp_fam[man.famille][1]+=1
                Corresp_fam[man.famille][2].append(man)
            if Corresp_fam[man.famille][1]>2:
                self.deletem(man)
                k+=1
        for man in self.men:
            man.famille=Corresp_fam[man.famille][0]
        n=0
        #print("fin milieu fam : ",len(self.men))
        for x in Corresp_fam:
            if x[1]==1:
                n+=1
                self.deletem(x[2][0])
        #print("fin supprésion fam : ",len(self.men))
        #print("verif",self.size)
        #print("fam seul : ",n)
        Corresp_fam=[[-1,0,[]] for x in range(self.fmax+1)]
        nbf=0
        for i in range(self.size):
            man=self.men[i-k]
            if Corresp_fam[man.famille][0]==-1:
                Corresp_fam[man.famille][0]=nbf
                nbf+=1
            if Corresp_fam[man.famille][1]<=2:
                Corresp_fam[man.famille][1]+=1
                Corresp_fam[man.famille][2].append(man)
            if Corresp_fam[man.famille][1]>2:
                self.deletem(man)
                k+=1
        for man in self.men:
            man.famille=Corresp_fam[man.famille][0]
        n=0

    def creation_fam_seul(self):
        for i in range(self.size):
            man=self.men[i]
            man.famille=i

    def match_p(self):
        compf=[[] for i in range(self.fmax)]
        #print("debut match : ",len(self.men))
        for man in self.men:
            compf[man.famille].append(man)
        for x in compf:
            #if len(x)==1:
                #print("erreur parrains seul : ",x[0].nom)
            if len(x)==2:
                x[0].cop=x[1]
                x[1].cop=x[0]
            #elif len(x)>2:
                #print("erreur parrains trop nombreux")

    def ecriture(self,membmax):
        wb = xlwt.Workbook('familles.xls') #création d'un fichier excel
        s = wb.add_sheet('A Test Sheet') #on crée une feuill de calcul
        familles=self.famille_liste()
        print(familles)
        print(len(familles))
        nbfam=len(familles)
        nb_membre_fam=[0 for x in range(self.fmax+1)] #stock le nombre de membre écrit dans chaque famille
        a_fillot=[False for x in range(self.fmax+1)]
        for man in self.men:
            if man.partner!=None:
                a_fillot[man.famille]=True
        # écriture des entêtes :
        filts=0
        for i in range((nbfam//10)):
            x=3*i
            for j in range(10):
                y=(membmax+3)*j
                print("entete 1 --> ",x," , ",y)

                #print(Familles_g[(10*i)+j])
                s.write(y,x+1,(10*i)+j+1,style_entete_d)
                s.write(y,x,"Nom de la famille : ",style_entete_g)
                s.write(y+1,x,"Parrains :",style_parrains_ent)
                s.write(y+1,x+1,"Fillots :",style_fillots_ent)
        for j in range(nbfam%10):
            y=(membmax+3)*j
            x=(nbfam//10)*3
            print("entete 2 --> ",x," , ",y)
            #print("entete -->",y)
            s.write(y,x+1,(nbfam//10)*10+j+1,style_entete_d)
            s.write(y,x,"Nom de la famille : ",style_entete_g)
            s.write(y+1,x,"Parrains :",style_parrains_ent)
            s.write(y+1,x+1,"Fillots :",style_fillots_ent)
        #print("-------fin entete--------")
        # écriture des noms :
        for man in self.men:
            famille=man.famille
            if True:
                #print("famille->",famille)
                #print("parrains :",man.nom)
                x=(famille//10)*3
                y=(membmax+3)*(famille%10)+2+nb_membre_fam[famille]
                #print("man -->",y)
                if nb_membre_fam[famille]!=membmax-1:
                    #print(x)
                    s.write(y,x,man.nom,style_parrains)
                    if man.partner!=None :
                        s.write(y,x+1,man.partner.nom,style_fillots)
                        filts+=1
                    else :
                        s.write(y,x+1," ++",style_fillots)
                else:
                    if man.partner!=None :
                        s.write(y,x,man.nom,style_parrains_fin)
                        s.write(y,x+1,man.partner.nom,style_fillots_fin)
                        filts+=1
                    else :
                        s.write(y,x+1," ",style_fillots_fin)
                nb_membre_fam[famille]+=1
        #print("-------fin man--------")
        # fin de la mise en page :
        for i in range(len(familles)):
            f=nb_membre_fam[i]
            for j in range(f,membmax):
                y=(((membmax+3)*((i)%10))+j)+2
                x=((i)//10)*3
                print("fin --> ",x," , ",y)
                if j!=membmax:
                    s.write(y,x," ",style_parrains)
                    s.write(y,x+1," ",style_fillots)
                else:
                    s.write(y,x," ",style_parrains_fin)
                    s.write(y,x+1," ",style_fillots_fin)
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

parrains=xlrd.open_workbook("Questionnaire Parrain-Fillot (Parrains ITII).xlsx")
shnp=parrains.sheet_names()
#print(len(shnp)) #Noms des feuilles
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

fillots=xlrd.open_workbook("Questionnaire Parrain-Fillot (fillots ITII) (réponses).xlsx")
shnf=fillots.sheet_names() #Noms des feuilles
shf=fillots.sheet_by_name(shnf[1]) #Feuille qui m'interresse

def ListeFillots():
    EI1=[]
    n=shf.ncols
    for k in range(1,shf.nrows):
        l=shf.row_values(k)
        EI1+=[Individual(l[1],l[3:16],CompFam)]
    return(EI1)


## Exploitation des réponses

def split(l):
    n=len(l)
    l1=[]
    l2=[]
    for i in range(n):
        if i%2==0:
            l1.append(l[i])
        else:
            l2.append(l[i])
    return(l1,l2)

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
    F1,F2=split(F)
    #print("-------F-------")
    #for x in F:
        #print(x.nom)
    #print("-------F1-------")
    #for x in F1:
        #print(x.nom)
    #print("-------F2-------")
    #for x in F2:
        #print(x.nom)
    Mf=MarriagesSimulation(F1,F2)
    Mf.creation_fam_seul()
    Mf.set_preferences()
    Mf.match_ITII()
    #print("match réussi f: ",Mf.verif_match())
    M=MarriagesSimulation(P,[])
    M.reduc_fam()
    M.ecremage()
    P1,P2=split(M.men)
    Mp=MarriagesSimulation(P1,P2)
    pers=""
    for man in Mp.men :
        if man.nom==pers:
            Mp.deletem(man)
            #print("-pierre")
    Mp.set_preferences()
    Mp.match_ITII()
    #print("----")
    pers="Marie VIOLLEAU"
    #for man in Mp.men :
    #    if man.nom==pers:
            #print(man.cop.nom)
    #for man in Mp.women :
     #   if man.nom==pers:
            #print(man.cop.nom)
    #print("match réussi p: ",M.verif_match())
    M.merge_ITII(Mf)
    M.set_preferences()
    M.match() #ca va tourner puis afficher les couples en premier Liste1, partenaire=Liste
    M.reduc_parrains()
    M.reduc_fam()
    # while M.sizew>M.size:
    #     nouv_fillots=[]
    #     a_enlever=[]
    #     print("nb_filts tot ----> ",M.sizew)
    #     print("nb filts théo ------>",len(M.women))
    #     for i in range(M.sizew):
    #         if M.women[i].partner==None:
    #             nouv_fillots.append((M.women[i]).copiage())
    #             a_enlever.append(i)
    #     for i in range(len(a_enlever)-1,-1,-1):
    #         inutile=M.women.pop(a_enlever[i])
    #         M.sizew-=1
    #     print("nb_nouv filts ----->",len(nouv_fillots))
    #     if nouv_fillots!=[]:
    #         nouv_parr,nbparr=M.ajout_p()
    #         M2=MarriagesSimulation(nouv_parr,nouv_fillots)
    #         M2.set_preferences()
    #         M2.match()
    #         M.merge(M2)
    M.ecriture(2)
    return(M)
    #, suivi de Liste2, partenaire= Liste1
    #Juste la première liste suffit donc
