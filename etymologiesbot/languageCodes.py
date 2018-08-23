from collections import OrderedDict

major_langs = ['es', 'fr', 'pt', 'it']
minor_langs = ['ca', 'gl', 'ro', 'co']
googleSupportedLangs = major_langs + minor_langs

lang_codes = ['pt','gl','fax','mwl','ast','mis_leo','ext','es','lad','an',
              'ca','oc','wa','fr','pms','lij','lmo','egl','vec','fur','lld','rm',
              'dlm','ist','it','nap','scn','co','sdn','sdc',
              'sc','src','sro',
              'ruo','ruq','ro' #,'la'
              ]

mappy = OrderedDict({
         #IBERIAN
         ##Galician-Portuguese
         'pt':'Portuguese','gl':'Galician','fax':'Fala',
         ##Astur-Leonese
         'mwl':'Mirandese','ast':'Asturian','mis_leo':'Leonese','ext':'Extremaduran',
         ##Old Spanish
         'es':'Spanish','lad':'Ladino',
         ##Aragonese
         'an':'Aragonese',
         
         #GALLIC
         ##Occitan
         'ca':'Catalan','oc':'Occitan',
         ##Langue D'Oil
         'wa':'Walloon','fr':'French',#'frm':'Middle French','fro':'Old French',
         ##Cisalpine
         'pms':'Piedmontese','lij':'Ligurian','lmo':'Lombard','egl':'Emilian','vec':'Venetian',
         ##Rhaetian
         'fur':'Friulian','lld':'Ladin','rm':'Romansh',

         #ITALO-DALMATIAN
         'dlm':'Dalmatian','ist':'Istriot','it': 'Italian','nap':'Neapolitan',
         'scn':'Sicilian','co':'Corsican','sdn':'Gallurese','sdc':'Sassarese',

         #SARDINIAN
         'sc': 'Sardinian','src':'Logudorese','sro':'Campidanese',

         #EASTERN
         'ruo':'Istro-Romanian','ruq':'Megleno-Romanian','ro':'Romanian'

         #LATIN
         #,'la':'Latin'
        })