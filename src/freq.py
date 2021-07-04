#!/usr/bin/env python3
import os
from modules import *
import sys
import string
import re
import weakref
import json

from collections import Counter, defaultdict
from pprint import pprint

class node():
    def __init__(self,parent):
        self.parent = parent
        self._pairs = Counter()
        self._cachecount = 0
        self._dirtycount = False

    def __getitem__(self,key):
        if self.parent.ignore_case and (key.islower() or key.isupper()):
            return  self._pairs[key.lower()] + self._pairs[key.upper()]
        else:
            return self._pairs[key]

    def __setitem__(self,key,value):

        # TODO: should consider using the __addr__ magic method instead
        # since the described behavior is this instead
        self._dirtycount = True
        self._pairs[key] += value

    @property
    def count(self):
        if self._dirtycount:
           self._cachecount = sum(self._pairs.values())
           self._dirtycount = False
        return self._cachecount


class FreqCounter(dict):
    
    def __init__(self, *args,**kwargs):
        self._table = defaultdict(lambda :node(self))
        self.ignore_case = False

        # TODO: consider refactoring to ignore_chars for consistency
        self.ignorechars = ""
        self.verbose = "verbose" in kwargs

    def __getitem__(self,key):
        return self._table[key]

    def __iter__(self):
        return iter(self._table)

    def __len__(self):
        return len(self._table)

    def toJSON(self):
        """
        Returns a string JSON reperesentation of the table.
        """
        serial = []
        for key,val in self._table.items():
            serial.append( (key, list(val._pairs.items())) )
        return json.dumps((self.ignore_case, self.ignorechars, serial))

    def fromJSON(self,jsondata):
        """
        Imports the table from a string JSON representation of the table

        Parameters
        ----------
        jsondata : str
            A string that represents the JSON Data

        Returns
        -------
        str
            the JSON representation of the table
        """

        # TODO: Raise an error if we get something that we didn't 
        # expect.
        args = json.loads(jsondata)
        if args:
            self.ignore_case = args[0]
            self.ignorechars = args[1]
            for outerkey,val in args[2]:
                self._table[outerkey] = node(self)
                for letter,count in val:
                   self._table[outerkey][letter] = count

    def tally_str(self,line,weight=1):
        """
        TODO: Update
        
        Parameters
        ----------
        line : string
            TODO: Update
        weight : int, optional
            the weight to be assigned to the pair (default = 1)
        """
        allpairs = re.findall(r"..", line)
        allpairs.extend(re.findall(r"..",line[1:]))
        for eachpair in allpairs:
            self[eachpair[0]][eachpair[1]] = weight

    def probability(self,line):
        """
        Calculates the probability of the word pair

        Parameters
        ----------
        line : str
            TODO: Update

        Returns
        -------
        float
            TODO: verify; the probability of the given word pair
        """
        allpairs = re.findall(r"..", line)
        allpairs.extend(re.findall(r"..",line[1:]))
        if self.verbose: 
            print(f"\n{PURPLE}{BOLD}"+"[+] All pairs: {0}\n".format(allpairs)+NONE)
        probs = []
        for eachpair in allpairs:
            pair = [eachpair[0], eachpair[1]]

            # check if any part of the pair should be ignored and alert
            # the user this was skipped
            if not all(x in self.ignorechars for x in pair):
                probs.append(self._probability(eachpair))
                if self.verbose: 
                    print (BOLD+WHITE+"[+] Probability of {0}: {1}".format(eachpair,probs))
            elif self.verbose:
                print("Pair '{}' was ignored",format(self.ignorechars))
        if probs:
            average_probability = sum(probs) / len(probs) * 100
        else:
            average_probability = 0.0
        if self.verbose:
            print(GREEN+"[+] Average Probability: {0}% \n".format(average_probability)+NONE)
        
        totl1 = 0
        totl2 = 0
        for eachpair in allpairs:
            l1 = l2 = 0
            pair = [eachpair[0], eachpair[1]]

            if not all(x in self.ignorechars for x in pair):
                l1 += self[eachpair[0]].count
                if self.ignore_case and (eachpair[0].islower() or eachpair[0].isupper()):
                    l1 += self[eachpair[0].swapcase()].count
                l2 += self[eachpair[0]][eachpair[1]]
                if self.ignore_case and (eachpair[0].islower() or eachpair[0].isupper()):
                    l2 += self[eachpair[0].swapcase()][eachpair[1]]
                totl1 += l1
                totl2 += l2
                if self.verbose: 
                    print(BOLD+WHITE+"[+] Letter1:{0} Letter2:{1}  - This pair {2}:{3} {4}:{5}".format(
                        totl1,
                        totl2, 
                        eachpair[0],
                        l1,
                        eachpair[1],
                        l2
                    )+NONE)
        if (totl1 == 0) or (totl2 == 0):
            total_word_probability = 0.0
        else:
            total_word_probability = totl2/totl1 * 100
        if self.verbose: print(GREEN+"[+] Total Word Probability: {0}/{1} = {2}\n".format(totl2, totl1, total_word_probability)+NONE)
        return average_probability,total_word_probability

    def _probability(self,twoletters):
        if self.ignore_case and (self[twoletters[0]].count == 0 and self[twoletters[0].swapcase()].count == 0):
            return 0.0
        if not self.ignore_case and self[twoletters[0]].count == 0:
            return 0.0
        if self.ignore_case and (twoletters[0].islower() or twoletters[0].isupper()):
            ignored_tot = sum([self[twoletters[0].lower()][eachlet] for eachlet in self.ignorechars]) + sum([self[twoletters[0].upper()][eachlet] for eachlet in self.ignorechars])
            let2 = self[twoletters[0].lower()][twoletters[1]] + self[twoletters[0].upper()][twoletters[1]]
            let1 = self[twoletters[0].lower()].count + self[twoletters[0].upper()].count
            if let1 - ignored_tot == 0:
                return 0.0
            return let2/(let1-ignored_tot)
        else:
            ignored_tot = sum([self[twoletters[0]][eachlet] for eachlet in self.ignorechars])
            if self[twoletters[0]].count - ignored_tot == 0:
                return 0.0
            return self[twoletters[0]][twoletters[1]] / (self[twoletters[0]].count - ignored_tot)

    def save(self,filename):
        try:
            file_handle =  open(filename, 'wb')
            file_handle.write(self.toJSON().encode("latin1"))
            file_handle.flush()
            file_handle.close()
        except Exception as e:
            print("Unable to write freq file :" + str(e))
            raise(e)

    def load(self,filename):
        try:
            file_handle =  open(filename,"rb")
            self.fromJSON(file_handle.read().decode("latin1"))
            file_handle.close()
        except Exception as e:
            print("Unable to load freq file :",str(e))
            raise(e)

    @property
    def count(self):
        return sum(map(lambda y:y.count, x._table.values()))

    def printtable(self):
        pprint(self.toJSON())

class FREQ:
    def __init__(self, filename,string):
        self.FREQ_FILE=filename
        self.CHECK_FILE()
        self.FC=None
        self.STR=string
        self.PROBABILITY=self.GET_FREQ()
        
    def CHECK_FILE(self):
        if not os.path.isfile(self.FREQ_FILE):
            if os.path.isfile("freq.txt"):
                print(f"{YELLOW}[+] Given Frequency File Does Not Exist")
                print(f"{GREEN}[+] Using Default Frequency File ")
                self.FREQ_FILE="freq.txt"
            else :
                print(f"{YELLOW}[-] Couldn't File Frequency Files!")
                print(f"{RED}[-] Exiting{NONE}")
                sys.exit(-1)
    
    def GET_FREQ(self):
        self.FC=FreqCounter(verbose=True)
        self.FC.load(self.FREQ_FILE)
        self.FC.ignore_case=False
        #self.SHOW_PROBABILITY=self.FC.probability(self.STR)
        #self.FC.save(self.FREQ_FILE)
        return self.FC.probability(self.STR)
         
            
    def SHOW_PROBABILITY(self):
        table=[["AVERAGE",self.PROBABILITY[0]],["Total",self.PROBABILITY[1]]]
        SHOW_TABLE("[+] Probability",table)
        #print(self.PROBABILITY)
        